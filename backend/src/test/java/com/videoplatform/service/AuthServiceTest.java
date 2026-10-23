package com.videoplatform.service;

import com.videoplatform.dto.AuthRequest;
import com.videoplatform.dto.AuthResponse;
import com.videoplatform.dto.RegisterRequest;
import com.videoplatform.entity.Role;
import com.videoplatform.entity.User;
import com.videoplatform.exception.InvalidFileException;
import com.videoplatform.repository.RoleRepository;
import com.videoplatform.repository.UserRepository;
import com.videoplatform.security.JwtTokenProvider;
import com.videoplatform.security.UserPrincipal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Collections;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class AuthServiceTest {

    @Mock
    private AuthenticationManager authenticationManager;

    @Mock
    private UserRepository userRepository;

    @Mock
    private RoleRepository roleRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenProvider tokenProvider;

    private AuthService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthService(authenticationManager, userRepository, roleRepository, passwordEncoder, tokenProvider);
    }

    @Test
    void testRegisterSuccess() {
        RegisterRequest request = new RegisterRequest("student@college.edu", "secret123", "Jane Doe");

        when(userRepository.existsByEmail("student@college.edu")).thenReturn(false);
        when(roleRepository.findByName("ROLE_USER")).thenReturn(Optional.of(new Role("ROLE_USER")));
        when(passwordEncoder.encode("secret123")).thenReturn("encodedPassword");

        User savedUser = new User("student@college.edu", "encodedPassword", "Jane Doe");
        savedUser.setId(1L);
        savedUser.setRoles(Collections.singleton(new Role("ROLE_USER")));
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        Authentication auth = mock(Authentication.class);
        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class))).thenReturn(auth);
        when(tokenProvider.generateToken(auth)).thenReturn("mocked.jwt.token");

        AuthResponse response = authService.register(request);

        assertNotNull(response);
        assertEquals("mocked.jwt.token", response.getToken());
        assertEquals("student@college.edu", response.getEmail());
        assertEquals("Jane Doe", response.getFullName());
        assertTrue(response.getRoles().contains("ROLE_USER"));
    }

    @Test
    void testRegisterDuplicateEmailThrowsException() {
        RegisterRequest request = new RegisterRequest("existing@college.edu", "secret123", "John Doe");
        when(userRepository.existsByEmail("existing@college.edu")).thenReturn(true);

        assertThrows(InvalidFileException.class, () -> authService.register(request));
        verify(userRepository, never()).save(any());
    }

    @Test
    void testLoginSuccess() {
        AuthRequest request = new AuthRequest("student@college.edu", "secret123");

        User user = new User("student@college.edu", "encodedPassword", "Jane Doe");
        user.setId(5L);
        user.setRoles(Collections.singleton(new Role("ROLE_USER")));
        UserPrincipal principal = UserPrincipal.create(user);

        Authentication auth = mock(Authentication.class);
        when(auth.getPrincipal()).thenReturn(principal);
        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class))).thenReturn(auth);
        when(tokenProvider.generateToken(auth)).thenReturn("login.jwt.token");

        AuthResponse response = authService.login(request);

        assertNotNull(response);
        assertEquals("login.jwt.token", response.getToken());
        assertEquals(5L, response.getId());
        assertEquals("student@college.edu", response.getEmail());
    }
}
