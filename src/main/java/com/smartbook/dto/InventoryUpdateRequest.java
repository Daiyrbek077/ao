package com.smartbook.dto;

import jakarta.validation.constraints.NotNull;

public class InventoryUpdateRequest {
    @NotNull
    private Integer stock;

    public Integer getStock() {
        return stock;
    }

    public void setStock(Integer stock) {
        this.stock = stock;
    }
}
