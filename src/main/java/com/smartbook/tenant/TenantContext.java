package com.smartbook.tenant;

public final class TenantContext {
    private static final ThreadLocal<Long> CURRENT_SHOP = new ThreadLocal<>();

    private TenantContext() {
    }

    public static void setShopId(Long shopId) {
        CURRENT_SHOP.set(shopId);
    }

    public static Long getShopId() {
        return CURRENT_SHOP.get();
    }

    public static void clear() {
        CURRENT_SHOP.remove();
    }
}
