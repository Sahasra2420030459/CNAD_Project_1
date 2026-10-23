package com.videoplatform;

import com.videoplatform.service.AuthServiceTest;
import com.videoplatform.service.VideoJobServiceTest;
import com.videoplatform.storage.LocalStorageServiceTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockitoAnnotations;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

public class RunAllUnitTests {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println(" RUNNING ALL AUTOMATED UNIT TESTS");
        System.out.println("=================================================");

        Class<?>[] testClasses = new Class<?>[] {
            LocalStorageServiceTest.class,
            VideoJobServiceTest.class,
            AuthServiceTest.class
        };

        int total = 0;
        int passed = 0;
        int failed = 0;
        List<String> failures = new ArrayList<>();

        for (Class<?> testClass : testClasses) {
            System.out.println("\nExecuting Test Suite: " + testClass.getSimpleName());

            Method beforeEach = findMethodByAnnotation(testClass, BeforeEach.class);
            Method afterEach = findMethodByAnnotation(testClass, AfterEach.class);

            for (Method method : testClass.getDeclaredMethods()) {
                if (method.isAnnotationPresent(Test.class)) {
                    total++;
                    String testName = testClass.getSimpleName() + "." + method.getName();
                    try {
                        Object instance = testClass.getDeclaredConstructor().newInstance();

                        // Initialize Mockito mocks if present
                        AutoCloseable mocks = MockitoAnnotations.openMocks(instance);

                        if (beforeEach != null) {
                            beforeEach.setAccessible(true);
                            beforeEach.invoke(instance);
                        }

                        method.setAccessible(true);
                        method.invoke(instance);

                        if (afterEach != null) {
                            afterEach.setAccessible(true);
                            afterEach.invoke(instance);
                        }

                        if (mocks != null) {
                            mocks.close();
                        }

                        System.out.println("  [PASS] " + method.getName());
                        passed++;
                    } catch (Throwable t) {
                        Throwable cause = t.getCause() != null ? t.getCause() : t;
                        System.err.println("  [FAIL] " + method.getName() + " -> " + cause.getMessage());
                        failures.add(testName + ": " + cause.getMessage());
                        failed++;
                    }
                }
            }
        }

        System.out.println("\n=================================================");
        System.out.println(String.format("TEST RESULTS: Total: %d | Passed: %d | Failed: %d", total, passed, failed));
        System.out.println("=================================================");

        if (failed > 0) {
            System.err.println("Failures:\n" + String.join("\n", failures));
            System.exit(1);
        } else {
            System.out.println("ALL TESTS PASSED SUCCESSFULLY! (Verified)");
            System.exit(0);
        }
    }

    private static Method findMethodByAnnotation(Class<?> clazz, Class<? extends java.lang.annotation.Annotation> annotation) {
        for (Method m : clazz.getDeclaredMethods()) {
            if (m.isAnnotationPresent(annotation)) {
                return m;
            }
        }
        return null;
    }
}
