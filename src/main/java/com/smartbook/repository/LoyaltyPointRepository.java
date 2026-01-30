package com.smartbook.repository;

import com.smartbook.entity.LoyaltyPoint;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface LoyaltyPointRepository extends JpaRepository<LoyaltyPoint, Long> {
    List<LoyaltyPoint> findByCustomerId(Long customerId);
}
