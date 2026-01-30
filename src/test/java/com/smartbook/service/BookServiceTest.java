package com.smartbook.service;

import com.smartbook.dto.BookDto;
import com.smartbook.entity.Book;
import com.smartbook.repository.BookRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BookServiceTest {
    @Mock
    private BookRepository bookRepository;

    @InjectMocks
    private BookService bookService;

    @Test
    void createBookMapsFields() {
        BookDto request = new BookDto();
        request.setIsbn("123");
        request.setTitle("Test");
        request.setAuthor("Author");
        request.setPrice(new BigDecimal("10.00"));
        request.setStock(5);

        Book saved = new Book();
        saved.setId(1L);
        saved.setIsbn("123");
        saved.setTitle("Test");
        saved.setAuthor("Author");
        saved.setPrice(new BigDecimal("10.00"));
        saved.setStock(5);

        when(bookRepository.save(any(Book.class))).thenReturn(saved);

        BookDto result = bookService.create(request);

        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getTitle()).isEqualTo("Test");
    }
}
