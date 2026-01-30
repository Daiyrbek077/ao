package com.smartbook.service;

import com.smartbook.dto.AuthRequest;
import com.smartbook.dto.AuthResponse;
import com.smartbook.dto.RefreshTokenRequest;
import com.smartbook.dto.RegisterRequest;
import com.smartbook.entity.Role;
import com.smartbook.entity.Shop;
import com.smartbook.entity.User;
import com.smartbook.exception.BadRequestException;
import com.smartbook.repository.ShopRepository;
import com.smartbook.repository.UserRepository;
import com.smartbook.security.JwtUtil;
import io.jsonwebtoken.Claims;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    private final ShopRepository shopRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;

    public AuthService(ShopRepository shopRepository,
                       UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       AuthenticationManager authenticationManager,
                       JwtUtil jwtUtil) {
        this.shopRepository = shopRepository;
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
    }

    public AuthResponse register(RegisterRequest request) {
        if (userRepository.findByUsername(request.getUsername()).isPresent()) {
            throw new BadRequestException("Username already exists");
        }
        Shop shop = new Shop();
        shop.setName(request.getShopName());
        shop.setAddress(request.getShopAddress());
        shop.setShopId(0L);
        shop = shopRepository.save(shop);
        shop.setShopId(shop.getId());
        shopRepository.save(shop);

        User admin = new User();
        admin.setUsername(request.getUsername());
        admin.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        admin.setRole(Role.ADMIN);
        admin.setShopId(shop.getId());
        userRepository.save(admin);

        String access = jwtUtil.generateAccessToken(admin.getUsername(), admin.getRole(), admin.getShopId());
        String refresh = jwtUtil.generateRefreshToken(admin.getUsername(), admin.getRole(), admin.getShopId());
        return new AuthResponse(access, refresh, admin.getRole(), admin.getShopId());
    }

    public AuthResponse login(AuthRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword()));
        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new BadRequestException("Invalid credentials"));
        String access = jwtUtil.generateAccessToken(user.getUsername(), user.getRole(), user.getShopId());
        String refresh = jwtUtil.generateRefreshToken(user.getUsername(), user.getRole(), user.getShopId());
        return new AuthResponse(access, refresh, user.getRole(), user.getShopId());
    }

    public AuthResponse refresh(RefreshTokenRequest request) {
        Claims claims = jwtUtil.parseClaims(request.getRefreshToken());
        String username = claims.getSubject();
        String role = claims.get("role", String.class);
        Long shopId = claims.get("shopId", Long.class);
        String access = jwtUtil.generateAccessToken(username, Role.valueOf(role), shopId);
        String refresh = jwtUtil.generateRefreshToken(username, Role.valueOf(role), shopId);
        return new AuthResponse(access, refresh, Role.valueOf(role), shopId);
    }
}
