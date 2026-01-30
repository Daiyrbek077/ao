package com.smartbook.service;

import com.smartbook.dto.BookDto;
import com.smartbook.entity.Book;
import com.smartbook.exception.NotFoundException;
import com.smartbook.repository.BookRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookService {
    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public BookDto create(BookDto dto) {
        Book book = new Book();
        mapToEntity(dto, book);
        Book saved = bookRepository.save(book);
        return mapToDto(saved);
    }

    public BookDto update(Long id, BookDto dto) {
        Book book = bookRepository.findById(id).orElseThrow(() -> new NotFoundException("Book not found"));
        mapToEntity(dto, book);
        Book saved = bookRepository.save(book);
        return mapToDto(saved);
    }

    public void delete(Long id) {
        Book book = bookRepository.findById(id).orElseThrow(() -> new NotFoundException("Book not found"));
        bookRepository.delete(book);
    }

    public List<BookDto> list() {
        return bookRepository.findAll().stream().map(this::mapToDto).toList();
    }

    public BookDto get(Long id) {
        return bookRepository.findById(id).map(this::mapToDto)
                .orElseThrow(() -> new NotFoundException("Book not found"));
    }

    public Book getEntity(Long id) {
        return bookRepository.findById(id).orElseThrow(() -> new NotFoundException("Book not found"));
    }

    public BookDto updateStock(Long id, int stock) {
        Book book = getEntity(id);
        book.setStock(stock);
        return mapToDto(bookRepository.save(book));
    }

    private void mapToEntity(BookDto dto, Book book) {
        book.setIsbn(dto.getIsbn());
        book.setTitle(dto.getTitle());
        book.setAuthor(dto.getAuthor());
        book.setImageUrl(dto.getImageUrl());
        book.setPrice(dto.getPrice());
        book.setStock(dto.getStock());
    }

    private BookDto mapToDto(Book book) {
        BookDto dto = new BookDto();
        dto.setId(book.getId());
        dto.setIsbn(book.getIsbn());
        dto.setTitle(book.getTitle());
        dto.setAuthor(book.getAuthor());
        dto.setImageUrl(book.getImageUrl());
        dto.setPrice(book.getPrice());
        dto.setStock(book.getStock());
        return dto;
    }
}
