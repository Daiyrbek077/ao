package com.smartbook.service;

import com.smartbook.dto.AnalyticsResponse;
import com.smartbook.entity.Sale;
import com.smartbook.repository.SaleRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;

@Service
public class AnalyticsService {
    private final SaleRepository saleRepository;

    public AnalyticsService(SaleRepository saleRepository) {
        this.saleRepository = saleRepository;
    }

    public AnalyticsResponse getAnalytics() {
        long totalSales = saleRepository.count();
        BigDecimal revenue = saleRepository.findAll().stream()
                .map(Sale::getTotalAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        long totalBooksSold = saleRepository.findAll().stream()
                .flatMap(sale -> sale.getSaleItems().stream())
                .mapToLong(item -> item.getQuantity())
                .sum();
        return new AnalyticsResponse(totalSales, revenue, totalBooksSold);
    }
}
