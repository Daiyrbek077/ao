package com.smartbook.exception;

import java.time.OffsetDateTime;

public class ApiError {
    private String message;
    private OffsetDateTime timestamp;

    public ApiError(String message) {
        this.message = message;
        this.timestamp = OffsetDateTime.now();
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public OffsetDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(OffsetDateTime timestamp) {
        this.timestamp = timestamp;
    }
}
