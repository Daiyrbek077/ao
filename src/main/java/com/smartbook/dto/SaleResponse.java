package com.smartbook.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.List;

public class SaleResponse {
    private Long saleId;
    private BigDecimal totalAmount;
    private int earnedBonuses;
    private OffsetDateTime createdAt;
    private List<SaleItemSummary> items;

    public Long getSaleId() {
        return saleId;
    }

    public void setSaleId(Long saleId) {
        this.saleId = saleId;
    }

    public BigDecimal getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(BigDecimal totalAmount) {
        this.totalAmount = totalAmount;
    }

    public int getEarnedBonuses() {
        return earnedBonuses;
    }

    public void setEarnedBonuses(int earnedBonuses) {
        this.earnedBonuses = earnedBonuses;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public List<SaleItemSummary> getItems() {
        return items;
    }

    public void setItems(List<SaleItemSummary> items) {
        this.items = items;
    }

    public static class SaleItemSummary {
        private String title;
        private int quantity;
        private BigDecimal price;

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public int getQuantity() {
            return quantity;
        }

        public void setQuantity(int quantity) {
            this.quantity = quantity;
        }

        public BigDecimal getPrice() {
            return price;
        }

        public void setPrice(BigDecimal price) {
            this.price = price;
        }
    }
}
