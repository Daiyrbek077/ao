package com.smartbook.service;

import com.smartbook.dto.BonusResponse;
import com.smartbook.dto.CustomerDto;
import com.smartbook.dto.MyBookDto;
import com.smartbook.dto.UpdateMyBookStatusRequest;
import com.smartbook.entity.Customer;
import com.smartbook.entity.MyBook;
import com.smartbook.exception.NotFoundException;
import com.smartbook.repository.CustomerRepository;
import com.smartbook.repository.MyBookRepository;
import com.smartbook.util.QrCodeUtil;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CustomerService {
    private final MyBookRepository myBookRepository;
    private final CustomerRepository customerRepository;

    public CustomerService(MyBookRepository myBookRepository, CustomerRepository customerRepository) {
        this.myBookRepository = myBookRepository;
        this.customerRepository = customerRepository;
    }

    public CustomerDto create(CustomerDto dto) {
        Customer customer = new Customer();
        customer.setName(dto.getName());
        customer.setTelegramId(dto.getTelegramId());
        customer.setPhone(dto.getPhone());
        customer.setBonusBalance(0);
        Customer saved = customerRepository.save(customer);
        return mapToDto(saved);
    }

    public List<CustomerDto> list() {
        return customerRepository.findAll().stream().map(this::mapToDto).toList();
    }

    public List<MyBookDto> getMyBooks(Long customerId) {
        return myBookRepository.findByCustomerId(customerId).stream().map(this::mapToDto).toList();
    }

    public MyBookDto updateStatus(UpdateMyBookStatusRequest request) {
        MyBook myBook = myBookRepository.findById(request.getMyBookId())
                .orElseThrow(() -> new NotFoundException("MyBook not found"));
        myBook.setStatus(request.getStatus());
        return mapToDto(myBookRepository.save(myBook));
    }

    public BonusResponse getBonuses(Long customerId) {
        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new NotFoundException("Customer not found"));
        return new BonusResponse(customer.getId(), customer.getBonusBalance());
    }

    public String getQrCode(Long customerId) {
        Customer customer = customerRepository.findById(customerId)
                .orElseThrow(() -> new NotFoundException("Customer not found"));
        return QrCodeUtil.generateBase64Png("customer:" + customer.getId());
    }

    private MyBookDto mapToDto(MyBook myBook) {
        MyBookDto dto = new MyBookDto();
        dto.setId(myBook.getId());
        dto.setTitle(myBook.getBook().getTitle());
        dto.setAuthor(myBook.getBook().getAuthor());
        dto.setStatus(myBook.getStatus());
        dto.setPurchasedAt(myBook.getPurchasedAt());
        return dto;
    }

    private CustomerDto mapToDto(Customer customer) {
        CustomerDto dto = new CustomerDto();
        dto.setId(customer.getId());
        dto.setName(customer.getName());
        dto.setTelegramId(customer.getTelegramId());
        dto.setPhone(customer.getPhone());
        dto.setBonusBalance(customer.getBonusBalance());
        return dto;
    }
}
