package com.smartbook.dto;

import java.math.BigDecimal;

public class AnalyticsResponse {
    private long totalSales;
    private BigDecimal totalRevenue;
    private long totalBooksSold;

    public AnalyticsResponse() {
    }

    public AnalyticsResponse(long totalSales, BigDecimal totalRevenue, long totalBooksSold) {
        this.totalSales = totalSales;
        this.totalRevenue = totalRevenue;
        this.totalBooksSold = totalBooksSold;
    }

    public long getTotalSales() {
        return totalSales;
    }

    public void setTotalSales(long totalSales) {
        this.totalSales = totalSales;
    }

    public BigDecimal getTotalRevenue() {
        return totalRevenue;
    }

    public void setTotalRevenue(BigDecimal totalRevenue) {
        this.totalRevenue = totalRevenue;
    }

    public long getTotalBooksSold() {
        return totalBooksSold;
    }

    public void setTotalBooksSold(long totalBooksSold) {
        this.totalBooksSold = totalBooksSold;
    }
}
