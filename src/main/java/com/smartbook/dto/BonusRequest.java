package com.smartbook.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class BonusRequest {
    @NotNull
    private Long customerId;

    @Min(1)
    private int points;

    public Long getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Long customerId) {
        this.customerId = customerId;
    }

    public int getPoints() {
        return points;
    }

    public void setPoints(int points) {
        this.points = points;
    }
}
