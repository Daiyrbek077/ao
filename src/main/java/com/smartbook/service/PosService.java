package com.smartbook.service;

import com.smartbook.dto.BonusRequest;
import com.smartbook.dto.BonusResponse;
import com.smartbook.dto.SaleItemRequest;
import com.smartbook.dto.SaleResponse;
import com.smartbook.entity.Book;
import com.smartbook.entity.Customer;
import com.smartbook.entity.LoyaltyPoint;
import com.smartbook.entity.MyBook;
import com.smartbook.entity.PaymentType;
import com.smartbook.entity.Sale;
import com.smartbook.entity.SaleItem;
import com.smartbook.exception.BadRequestException;
import com.smartbook.exception.NotFoundException;
import com.smartbook.repository.BookRepository;
import com.smartbook.repository.CustomerRepository;
import com.smartbook.repository.LoyaltyPointRepository;
import com.smartbook.repository.MyBookRepository;
import com.smartbook.repository.SaleRepository;
import com.smartbook.tenant.TenantContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class PosService {
    private static final BigDecimal BONUS_RATE = new BigDecimal("0.05");

    private final BookService bookService;
    private final BookRepository bookRepository;
    private final SaleRepository saleRepository;
    private final CustomerRepository customerRepository;
    private final LoyaltyPointRepository loyaltyPointRepository;
    private final MyBookRepository myBookRepository;

    public PosService(BookService bookService,
                      BookRepository bookRepository,
                      SaleRepository saleRepository,
                      CustomerRepository customerRepository,
                      LoyaltyPointRepository loyaltyPointRepository,
                      MyBookRepository myBookRepository) {
        this.bookService = bookService;
        this.bookRepository = bookRepository;
        this.saleRepository = saleRepository;
        this.customerRepository = customerRepository;
        this.loyaltyPointRepository = loyaltyPointRepository;
        this.myBookRepository = myBookRepository;
    }

    @Transactional
    public SaleResponse createSale(Long customerId, PaymentType paymentType, List<SaleItemRequest> items) {
        Customer customer = null;
        if (customerId != null) {
            customer = customerRepository.findById(customerId)
                    .orElseThrow(() -> new NotFoundException("Customer not found"));
        }

        Sale sale = new Sale();
        sale.setPaymentType(paymentType);
        sale.setCustomer(customer);
        sale.setCreatedAt(OffsetDateTime.now());

        List<SaleItem> saleItems = new ArrayList<>();
        BigDecimal total = BigDecimal.ZERO;
        for (SaleItemRequest request : items) {
            Book book = bookService.getEntity(request.getBookId());
            if (book.getStock() < request.getQuantity()) {
                throw new BadRequestException("Insufficient stock for " + book.getTitle());
            }
            book.setStock(book.getStock() - request.getQuantity());
            bookRepository.save(book);
            SaleItem item = new SaleItem();
            item.setSale(sale);
            item.setBook(book);
            item.setQuantity(request.getQuantity());
            item.setPrice(book.getPrice());
            saleItems.add(item);
            total = total.add(book.getPrice().multiply(BigDecimal.valueOf(request.getQuantity())));
        }
        sale.setSaleItems(saleItems);
        sale.setTotalAmount(total);
        Sale saved = saleRepository.save(sale);

        int earnedBonuses = 0;
        if (customer != null && paymentType != PaymentType.BONUS) {
            earnedBonuses = total.multiply(BONUS_RATE).intValue();
            customer.setBonusBalance(customer.getBonusBalance() + earnedBonuses);
            LoyaltyPoint point = new LoyaltyPoint();
            point.setCustomer(customer);
            point.setPoints(earnedBonuses);
            point.setReason("Purchase");
            point.setCreatedAt(OffsetDateTime.now());
            point.setShopId(TenantContext.getShopId());
            loyaltyPointRepository.save(point);
            customerRepository.save(customer);
        }

        if (customer != null) {
            for (SaleItem item : saleItems) {
                MyBook myBook = new MyBook();
                myBook.setCustomer(customer);
                myBook.setBook(item.getBook());
                myBook.setStatus("PURCHASED");
                myBook.setPurchasedAt(OffsetDateTime.now());
                myBookRepository.save(myBook);
            }
        }

        SaleResponse response = new SaleResponse();
        response.setSaleId(saved.getId());
        response.setTotalAmount(total);
        response.setEarnedBonuses(earnedBonuses);
        response.setCreatedAt(saved.getCreatedAt());
        response.setItems(saved.getSaleItems().stream().map(item -> {
            SaleResponse.SaleItemSummary summary = new SaleResponse.SaleItemSummary();
            summary.setTitle(item.getBook().getTitle());
            summary.setQuantity(item.getQuantity());
            summary.setPrice(item.getPrice());
            return summary;
        }).toList());
        return response;
    }

    public BonusResponse deductBonuses(BonusRequest request) {
        Customer customer = customerRepository.findById(request.getCustomerId())
                .orElseThrow(() -> new NotFoundException("Customer not found"));
        if (customer.getBonusBalance() < request.getPoints()) {
            throw new BadRequestException("Not enough bonuses");
        }
        customer.setBonusBalance(customer.getBonusBalance() - request.getPoints());
        LoyaltyPoint point = new LoyaltyPoint();
        point.setCustomer(customer);
        point.setPoints(-request.getPoints());
        point.setReason("Redeem");
        point.setCreatedAt(OffsetDateTime.now());
        point.setShopId(TenantContext.getShopId());
        loyaltyPointRepository.save(point);
        customerRepository.save(customer);
        return new BonusResponse(customer.getId(), customer.getBonusBalance());
    }

    public BonusResponse calculateBonuses(BigDecimal total) {
        int bonus = total.multiply(BONUS_RATE).intValue();
        return new BonusResponse(null, bonus);
    }

    public SaleResponse getReceipt(Long saleId) {
        Sale sale = saleRepository.findById(saleId).orElseThrow(() -> new NotFoundException("Sale not found"));
        SaleResponse response = new SaleResponse();
        response.setSaleId(sale.getId());
        response.setTotalAmount(sale.getTotalAmount());
        response.setCreatedAt(sale.getCreatedAt());
        response.setItems(sale.getSaleItems().stream().map(item -> {
            SaleResponse.SaleItemSummary summary = new SaleResponse.SaleItemSummary();
            summary.setTitle(item.getBook().getTitle());
            summary.setQuantity(item.getQuantity());
            summary.setPrice(item.getPrice());
            return summary;
        }).toList());
        response.setEarnedBonuses(0);
        return response;
    }
}
