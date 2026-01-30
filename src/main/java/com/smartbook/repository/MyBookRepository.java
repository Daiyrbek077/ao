package com.smartbook.repository;

import com.smartbook.entity.MyBook;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MyBookRepository extends JpaRepository<MyBook, Long> {
    List<MyBook> findByCustomerId(Long customerId);
}
