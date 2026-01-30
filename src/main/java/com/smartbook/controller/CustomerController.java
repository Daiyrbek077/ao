package com.smartbook.controller;

import com.smartbook.dto.BonusResponse;
import com.smartbook.dto.MyBookDto;
import com.smartbook.dto.UpdateMyBookStatusRequest;
import com.smartbook.service.CustomerService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/customer")
public class CustomerController {
    private final CustomerService customerService;

    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }

    @GetMapping("/mybooks/{customerId}")
    public ResponseEntity<List<MyBookDto>> myBooks(@PathVariable Long customerId) {
        return ResponseEntity.ok(customerService.getMyBooks(customerId));
    }

    @PostMapping("/mybooks/status")
    public ResponseEntity<MyBookDto> updateStatus(@Valid @RequestBody UpdateMyBookStatusRequest request) {
        return ResponseEntity.ok(customerService.updateStatus(request));
    }

    @GetMapping("/bonuses/{customerId}")
    public ResponseEntity<BonusResponse> bonuses(@PathVariable Long customerId) {
        return ResponseEntity.ok(customerService.getBonuses(customerId));
    }

    @GetMapping("/qr/{customerId}")
    public ResponseEntity<String> qr(@PathVariable Long customerId) {
        return ResponseEntity.ok(customerService.getQrCode(customerId));
    }
}
