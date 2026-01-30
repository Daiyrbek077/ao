package com.smartbook.controller;

import com.smartbook.dto.BonusRequest;
import com.smartbook.dto.BonusResponse;
import com.smartbook.dto.GoogleBookDto;
import com.smartbook.dto.SaleRequest;
import com.smartbook.dto.SaleResponse;
import com.smartbook.integration.GoogleBooksService;
import com.smartbook.service.PosService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/pos")
public class PosController {
    private final GoogleBooksService googleBooksService;
    private final PosService posService;

    public PosController(GoogleBooksService googleBooksService, PosService posService) {
        this.googleBooksService = googleBooksService;
        this.posService = posService;
    }

    @GetMapping("/scan/{isbn}")
    public ResponseEntity<GoogleBookDto> scanIsbn(@PathVariable String isbn) {
        return ResponseEntity.ok(googleBooksService.fetchByIsbn(isbn));
    }

    @PostMapping("/sales")
    public ResponseEntity<SaleResponse> createSale(@Valid @RequestBody SaleRequest request) {
        return ResponseEntity.ok(posService.createSale(request.getCustomerId(), request.getPaymentType(), request.getItems()));
    }

    @PostMapping("/bonuses/calculate")
    public ResponseEntity<BonusResponse> calculateBonuses(@RequestBody Map<String, BigDecimal> payload) {
        BigDecimal total = payload.getOrDefault("total", BigDecimal.ZERO);
        return ResponseEntity.ok(posService.calculateBonuses(total));
    }

    @PostMapping("/bonuses/deduct")
    public ResponseEntity<BonusResponse> deductBonuses(@Valid @RequestBody BonusRequest request) {
        return ResponseEntity.ok(posService.deductBonuses(request));
    }

    @GetMapping("/receipt/{saleId}")
    public ResponseEntity<SaleResponse> receipt(@PathVariable Long saleId) {
        return ResponseEntity.ok(posService.getReceipt(saleId));
    }
}
