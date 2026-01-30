package com.smartbook.controller;

import com.smartbook.dto.AnalyticsResponse;
import com.smartbook.dto.BookDto;
import com.smartbook.dto.CashierDto;
import com.smartbook.dto.CustomerDto;
import com.smartbook.dto.InventoryUpdateRequest;
import com.smartbook.service.AnalyticsService;
import com.smartbook.service.BookService;
import com.smartbook.service.CashierService;
import com.smartbook.service.CustomerService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
public class AdminController {
    private final BookService bookService;
    private final CashierService cashierService;
    private final AnalyticsService analyticsService;
    private final CustomerService customerService;

    public AdminController(BookService bookService,
                           CashierService cashierService,
                           AnalyticsService analyticsService,
                           CustomerService customerService) {
        this.bookService = bookService;
        this.cashierService = cashierService;
        this.analyticsService = analyticsService;
        this.customerService = customerService;
    }

    @PostMapping("/books")
    public ResponseEntity<BookDto> createBook(@Valid @RequestBody BookDto dto) {
        return ResponseEntity.ok(bookService.create(dto));
    }

    @GetMapping("/books")
    public ResponseEntity<List<BookDto>> listBooks() {
        return ResponseEntity.ok(bookService.list());
    }

    @GetMapping("/books/{id}")
    public ResponseEntity<BookDto> getBook(@PathVariable Long id) {
        return ResponseEntity.ok(bookService.get(id));
    }

    @PutMapping("/books/{id}")
    public ResponseEntity<BookDto> updateBook(@PathVariable Long id, @Valid @RequestBody BookDto dto) {
        return ResponseEntity.ok(bookService.update(id, dto));
    }

    @DeleteMapping("/books/{id}")
    public ResponseEntity<Void> deleteBook(@PathVariable Long id) {
        bookService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/inventory/{id}")
    public ResponseEntity<BookDto> updateInventory(@PathVariable Long id, @Valid @RequestBody InventoryUpdateRequest request) {
        return ResponseEntity.ok(bookService.updateStock(id, request.getStock()));
    }

    @PostMapping("/cashiers")
    public ResponseEntity<CashierDto> createCashier(@Valid @RequestBody CashierDto dto) {
        return ResponseEntity.ok(cashierService.create(dto));
    }

    @GetMapping("/cashiers")
    public ResponseEntity<List<CashierDto>> listCashiers() {
        return ResponseEntity.ok(cashierService.list());
    }

    @PutMapping("/cashiers/{id}")
    public ResponseEntity<CashierDto> updateCashier(@PathVariable Long id, @Valid @RequestBody CashierDto dto) {
        return ResponseEntity.ok(cashierService.update(id, dto));
    }

    @DeleteMapping("/cashiers/{id}")
    public ResponseEntity<Void> deleteCashier(@PathVariable Long id) {
        cashierService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/analytics")
    public ResponseEntity<AnalyticsResponse> analytics() {
        return ResponseEntity.ok(analyticsService.getAnalytics());
    }

    @PostMapping("/customers")
    public ResponseEntity<CustomerDto> createCustomer(@Valid @RequestBody CustomerDto dto) {
        return ResponseEntity.ok(customerService.create(dto));
    }

    @GetMapping("/customers")
    public ResponseEntity<List<CustomerDto>> listCustomers() {
        return ResponseEntity.ok(customerService.list());
    }
}
