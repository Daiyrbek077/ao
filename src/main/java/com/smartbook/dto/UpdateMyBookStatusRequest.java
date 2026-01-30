package com.smartbook.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class UpdateMyBookStatusRequest {
    @NotNull
    private Long myBookId;

    @NotBlank
    private String status;

    public Long getMyBookId() {
        return myBookId;
    }

    public void setMyBookId(Long myBookId) {
        this.myBookId = myBookId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
