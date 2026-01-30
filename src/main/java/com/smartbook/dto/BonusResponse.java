package com.smartbook.dto;

public class BonusResponse {
    private Long customerId;
    private int bonusBalance;

    public BonusResponse() {
    }

    public BonusResponse(Long customerId, int bonusBalance) {
        this.customerId = customerId;
        this.bonusBalance = bonusBalance;
    }

    public Long getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Long customerId) {
        this.customerId = customerId;
    }

    public int getBonusBalance() {
        return bonusBalance;
    }

    public void setBonusBalance(int bonusBalance) {
        this.bonusBalance = bonusBalance;
    }
}
