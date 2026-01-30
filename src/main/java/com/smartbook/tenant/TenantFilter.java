package com.smartbook.tenant;

import com.smartbook.security.JwtUtil;
import io.jsonwebtoken.Claims;
import jakarta.persistence.EntityManager;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.hibernate.Filter;
import org.hibernate.Session;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class TenantFilter extends OncePerRequestFilter {
    private final EntityManager entityManager;
    private final JwtUtil jwtUtil;

    public TenantFilter(EntityManager entityManager, JwtUtil jwtUtil) {
        this.entityManager = entityManager;
        this.jwtUtil = jwtUtil;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        try {
            Long shopId = TenantContext.getShopId();
            if (shopId == null) {
                String authHeader = request.getHeader(HttpHeaders.AUTHORIZATION);
                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    try {
                        Claims claims = jwtUtil.parseClaims(authHeader.substring(7));
                        shopId = claims.get("shopId", Long.class);
                        TenantContext.setShopId(shopId);
                    } catch (Exception ignored) {
                        // ignore invalid tokens for tenant resolution
                    }
                }
            }
            if (shopId != null) {
                Session session = entityManager.unwrap(Session.class);
                Filter filter = session.enableFilter("shopFilter");
                filter.setParameter("shopId", shopId);
            }
            filterChain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }
}
