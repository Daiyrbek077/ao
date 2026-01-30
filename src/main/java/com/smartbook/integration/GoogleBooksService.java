package com.smartbook.integration;

import com.smartbook.dto.GoogleBookDto;
import com.smartbook.exception.NotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Service
public class GoogleBooksService {
    private final RestTemplate restTemplate;

    public GoogleBooksService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public GoogleBookDto fetchByIsbn(String isbn) {
        String url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn;
        GoogleBooksResponse response = restTemplate.getForObject(url, GoogleBooksResponse.class);
        if (response == null || response.items() == null || response.items().isEmpty()) {
            throw new NotFoundException("Book not found by ISBN");
        }
        GoogleBooksResponse.VolumeInfo info = response.items().get(0).volumeInfo();
        GoogleBookDto dto = new GoogleBookDto();
        dto.setTitle(info.title());
        dto.setAuthor(Optional.ofNullable(info.authors()).orElse(List.of("Unknown")).get(0));
        dto.setCategories(Optional.ofNullable(info.categories()).orElse(Collections.emptyList()));
        dto.setDescription(info.description());
        if (info.imageLinks() != null) {
            dto.setImageUrl(info.imageLinks().thumbnail());
        }
        return dto;
    }
}
