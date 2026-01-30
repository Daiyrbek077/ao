package com.smartbook.security;

import com.smartbook.entity.Role;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.time.Instant;
import java.util.Date;

@Component
public class JwtUtil {
    private final Key key;
    private final long accessTokenMinutes;
    private final long refreshTokenMinutes;

    public JwtUtil(@Value("${security.jwt.secret}") String secret,
                   @Value("${security.jwt.accessTokenMinutes:60}") long accessTokenMinutes,
                   @Value("${security.jwt.refreshTokenMinutes:43200}") long refreshTokenMinutes) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes());
        this.accessTokenMinutes = accessTokenMinutes;
        this.refreshTokenMinutes = refreshTokenMinutes;
    }

    public String generateAccessToken(String username, Role role, Long shopId) {
        return buildToken(username, role, shopId, accessTokenMinutes);
    }

    public String generateRefreshToken(String username, Role role, Long shopId) {
        return buildToken(username, role, shopId, refreshTokenMinutes);
    }

    private String buildToken(String username, Role role, Long shopId, long minutes) {
        Instant now = Instant.now();
        return Jwts.builder()
                .setSubject(username)
                .claim("role", role.name())
                .claim("shopId", shopId)
                .setIssuedAt(Date.from(now))
                .setExpiration(Date.from(now.plusSeconds(minutes * 60)))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    public Claims parseClaims(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
