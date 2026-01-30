package com.smartbook.service;

import com.smartbook.dto.CashierDto;
import com.smartbook.entity.Role;
import com.smartbook.entity.User;
import com.smartbook.exception.NotFoundException;
import com.smartbook.repository.UserRepository;
import com.smartbook.tenant.TenantContext;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CashierService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public CashierService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public CashierDto create(CashierDto dto) {
        User user = new User();
        user.setUsername(dto.getUsername());
        user.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        user.setRole(Role.CASHIER);
        user.setActive(dto.isActive());
        user.setShopId(TenantContext.getShopId());
        User saved = userRepository.save(user);
        return mapToDto(saved);
    }

    public CashierDto update(Long id, CashierDto dto) {
        User user = userRepository.findById(id).orElseThrow(() -> new NotFoundException("Cashier not found"));
        user.setUsername(dto.getUsername());
        if (dto.getPassword() != null && !dto.getPassword().isBlank()) {
            user.setPasswordHash(passwordEncoder.encode(dto.getPassword()));
        }
        user.setActive(dto.isActive());
        return mapToDto(userRepository.save(user));
    }

    public List<CashierDto> list() {
        return userRepository.findByRole(Role.CASHIER).stream().map(this::mapToDto).toList();
    }

    public void delete(Long id) {
        User user = userRepository.findById(id).orElseThrow(() -> new NotFoundException("Cashier not found"));
        userRepository.delete(user);
    }

    private CashierDto mapToDto(User user) {
        CashierDto dto = new CashierDto();
        dto.setId(user.getId());
        dto.setUsername(user.getUsername());
        dto.setActive(user.isActive());
        dto.setPassword("***");
        return dto;
    }
}
