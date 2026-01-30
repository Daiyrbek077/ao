package com.smartbook.tenant;

import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;

public class ShopEntityListener {
    @PrePersist
    @PreUpdate
    public void applyShopId(Object entity) {
        if (entity instanceof ShopAware shopAware) {
            if (shopAware.getShopId() == null) {
                shopAware.setShopId(TenantContext.getShopId());
            }
        }
    }
}
