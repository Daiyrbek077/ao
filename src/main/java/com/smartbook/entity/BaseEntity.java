package com.smartbook.entity;

import com.smartbook.tenant.ShopAware;
import com.smartbook.tenant.ShopEntityListener;
import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import org.hibernate.annotations.Filter;
import org.hibernate.annotations.FilterDef;
import org.hibernate.annotations.ParamDef;

@MappedSuperclass
@EntityListeners(ShopEntityListener.class)
@FilterDef(name = "shopFilter", parameters = @ParamDef(name = "shopId", type = Long.class))
@Filter(name = "shopFilter", condition = "shop_id = :shopId")
public abstract class BaseEntity implements ShopAware {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "shop_id", nullable = false)
    private Long shopId;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    @Override
    public Long getShopId() {
        return shopId;
    }

    @Override
    public void setShopId(Long shopId) {
        this.shopId = shopId;
    }
}
