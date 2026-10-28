"""
Java Programming Curriculum for EduAdapt-AI
Contains full structured content for Easy, Medium, and Complex levels.
"""

JAVA_DATA = {
    'id': 'java',
    'title': 'Java Programming',
    'badge_color': 'danger',
    'icon': 'bi-filetype-java',
    'short_summary': 'Master modern Java from object-oriented basics to multithreading, Streams, and JVM internals.',
    'description': 'A rigorous curriculum spanning JVM architecture, object-oriented software engineering, collections, generics, Java 8 functional streams, and concurrent programming.',
    'difficulty': 'Beginner to Advanced',
    'levels': {
        'easy': {
            'level_number': 1,
            'name': 'Easy (Level 1 - Core Foundations)',
            'description': 'JVM ecosystem, strongly-typed variables, console I/O, operators, control flow, loops, and arrays.',
            'topics': [
                {
                    'id': 'java-jvm-architecture',
                    'title': '1. Java Architecture: JDK, JRE, JVM & Bytecode',
                    'read_time': '9 min',
                    'summary': 'Understand the "Write Once, Run Anywhere" paradigm and the roles of JDK, JRE, JVM, and JIT Compiler.',
                    'concept': """Java is a statically typed, class-based, object-oriented language created by James Gosling. Its hallmark capability is platform independence through the slogan: "Write Once, Run Anywhere" (WORA).

Components of the Java Ecosystem:
- **JDK (Java Development Kit)**: Complete development environment containing the compiler (`javac`), archiver (`jar`), debugger, and the JRE.
- **JRE (Java Runtime Environment)**: Provides the minimum libraries and JVM required to run compiled Java applications.
- **JVM (Java Virtual Machine)**: The abstract execution machine that loads compiled bytecode (`.class` files), verifies bytecode integrity, and translates instructions into native machine code.
- **JIT (Just-In-Time) Compiler**: High-performance engine within the JVM that compiles frequently executed bytecode hotspots directly into native CPU machine instructions at runtime.""",
                    'syntax': """// Source code in Example.java
// Compile: javac Example.java  -> generates Example.class (bytecode)
// Execute: java Example        -> executed by JVM
""",
                    'code_example': """public class ArchitectureDemo {
    public static void main(String[] args) {
        System.out.println("Java Virtual Machine Architecture Demo");
        System.out.println("Java Vendor: " + System.getProperty("java.vendor"));
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("OS Architecture: " + System.getProperty("os.arch"));
    }
}
""",
                    'expected_output': """Java Virtual Machine Architecture Demo
Java Vendor: Oracle Corporation (or OpenJDK)
Java Version: 21.0.2
OS Architecture: amd64
""",
                    'common_mistakes': 'Confusing JDK with JRE. You cannot compile `.java` source code using only a JRE; you must have the full JDK installed.',
                    'practice_question': 'What component within the JVM compiles bytecode into native machine instructions at runtime for performance optimization? (Answer: The JIT / Just-In-Time Compiler).'
                },
                {
                    'id': 'java-program-structure',
                    'title': '2. Structure of a Java Program & the main Method',
                    'read_time': '8 min',
                    'summary': 'Deconstruct the standard Java class skeleton and dissect public static void main(String[] args).',
                    'concept': """Every line of executable code in Java must reside inside a class. Furthermore, the name of the public class must exactly match the source filename (e.g. `public class MainApp` must be saved in `MainApp.java`).

The entry point of every standalone Java program is:
`public static void main(String[] args)`
- `public`: Access modifier allowing the JVM to invoke the method from outside the class.
- `static`: Allows the JVM to invoke the method without creating an instance of the class in memory.
- `void`: The method returns no value to the operating system.
- `main`: The designated entry point method name recognized by the JVM.
- `String[] args`: Command-line arguments passed into the program as an array of strings.""",
                    'syntax': """public class ClassName {
    public static void main(String[] args) {
        // Statements terminate with a semicolon ;
        System.out.println("Message");
    }
}
""",
                    'code_example': """public class HelloEduAdapt {
    public static void main(String[] args) {
        System.out.println("Welcome to EduAdapt-AI Java Curriculum!");
        System.out.print("This prints on one line, ");
        System.out.println("while println appends a newline.");
    }
}
""",
                    'expected_output': """Welcome to EduAdapt-AI Java Curriculum!
This prints on one line, while println appends a newline.
""",
                    'common_mistakes': 'Omitting the `static` keyword on `main`, causing the JVM to throw `Error: Main method is not static in class...`.',
                    'practice_question': 'Why is the main method in Java declared as static? (Answer: So the JVM can execute it without having to instantiate an object of the enclosing class).'
                },
                {
                    'id': 'java-types-variables',
                    'title': '3. Primitive Data Types, Variables & Type Casting',
                    'read_time': '10 min',
                    'summary': 'Learn Java 8 primitive types, memory sizes, automatic widening vs explicit narrowing conversions.',
                    'concept': """Java is a strongly typed language. Variables must be declared with an explicit data type before they can store values.

Java has 8 primitive data types:
1. `byte` (8-bit, -128 to 127)
2. `short` (16-bit, -32,768 to 32,767)
3. `int` (32-bit, default integer type)
4. `long` (64-bit, appended with `L`, e.g. `10000000000L`)
5. `float` (32-bit single-precision, appended with `f`, e.g. `3.14f`)
6. `double` (64-bit double-precision, default float type)
7. `char` (16-bit Unicode character, single quotes `'A'`)
8. `boolean` (`true` or `false`)

Type Casting:
- **Widening (Implicit)**: Converting smaller to larger type (e.g. `int` to `double`). Safe, automatic.
- **Narrowing (Explicit)**: Converting larger to smaller type (e.g. `double` to `int`). Potential data loss, requires cast operator `(int) value`.""",
                    'syntax': """int studentScore = 85;
double preciseAverage = 85.75;
int truncated = (int) preciseAverage; // Explicit narrowing cast to 85
""",
                    'code_example': """public class PrimitiveDemo {
    public static void main(String[] args) {
        int questionsAnswered = 10;
        int questionsCorrect = 8;
        
        // Division without casting causes integer truncation!
        double rawRatio = questionsCorrect / questionsAnswered; // 0.0
        double accuratePct = ((double) questionsCorrect / questionsAnswered) * 100.0; // 80.0
        
        System.out.println("Raw integer division result: " + rawRatio);
        System.out.println("Accurate Percentage: " + accuratePct + "%");
    }
}
""",
                    'expected_output': """Raw integer division result: 0.0
Accurate Percentage: 80.0%
""",
                    'common_mistakes': 'Performing division between two `int` variables and expecting a `double`. `8 / 10` produces `0` because integer division truncates fractions before assignment.',
                    'practice_question': 'How many bytes of memory does a Java `int` occupy? (Answer: 4 bytes / 32 bits).'
                },
                {
                    'id': 'java-operators',
                    'title': '4. Operators & Expressions',
                    'read_time': '9 min',
                    'summary': 'Master arithmetic, relational, boolean logical (&&, ||, !), unary increment, and compound assignments.',
                    'concept': """Java operators evaluate expressions following strict precedence rules.
- **Arithmetic**: `+`, `-`, `*`, `/`, `%` (modulus).
- **Unary**: `++` (prefix/postfix increment), `--`. Prefix `++x` increments before value evaluation; postfix `x++` evaluates the current value first, then increments.
- **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- **Logical**: `&&` (short-circuit AND), `||` (short-circuit OR), `!` (NOT).
- **Ternary**: `condition ? valueIfTrue : valueIfFalse`.""",
                    'syntax': """int count = 5;
int a = ++count; // count becomes 6, a is 6
int b = count++; // b is 6, count becomes 7
""",
                    'code_example': """public class OperatorDemo {
    public static void main(String[] args) {
        int score = 74;
        boolean passedAttendance = true;
        
        // Ternary operator with compound logic
        boolean isEligible = (score >= 70) && passedAttendance;
        String status = isEligible ? "Level Unlocked" : "Locked";
        
        System.out.println("Assessment Passed: " + (score >= 70));
        System.out.println("Final Progression Status: " + status);
    }
}
""",
                    'expected_output': """Assessment Passed: true
Final Progression Status: Level Unlocked
""",
                    'common_mistakes': 'Confusing the bitwise operator `&` with the short-circuit logical operator `&&`. `&&` halts evaluation if the left operand is false, preventing potential `NullPointerException`s.',
                    'practice_question': 'Given `int x = 5; int y = x++;`, what are the values of `x` and `y` after execution? (Answer: `x` is 6, `y` is 5).'
                },
                {
                    'id': 'java-scanner-io',
                    'title': '5. Console Input with Scanner & System.out Formatting',
                    'read_time': '9 min',
                    'summary': 'Read user input from standard in using java.util.Scanner and format output using printf.',
                    'concept': """To capture interactive console input, Java provides the `java.util.Scanner` class. It tokenizes input using whitespace delimiters and parses primitive types using methods such as `.nextInt()`, `.nextDouble()`, and `.nextLine()`.

Formatted output is achieved via `System.out.printf(formatString, args...)` using standard conversion specifiers:
- `%d`: Integer
- `%.2f`: Floating point with 2 decimals
- `%s`: String
- `%n`: Platform-independent newline separator.""",
                    'syntax': """import java.util.Scanner;

Scanner sc = new Scanner(System.in);
String name = sc.nextLine();
int score = sc.nextInt();
sc.close();
""",
                    'code_example': """import java.util.Scanner;

public class ConsoleIODemo {
    public static void main(String[] args) {
        // Simulating input stream via string
        String mockInput = "Sahasra\\n88\\n";
        Scanner scanner = new Scanner(mockInput);
        
        String studentName = scanner.nextLine();
        int score = scanner.nextInt();
        
        System.out.printf("Student: %-10s | Score: %3d/100 | Result: %s%n", 
                          studentName, score, score >= 70 ? "PASS" : "FAIL");
        scanner.close();
    }
}
""",
                    'expected_output': """Student: Sahasra    | Score:  88/100 | Result: PASS
""",
                    'common_mistakes': 'Calling `scanner.nextLine()` immediately after `scanner.nextInt()`. The leftover newline character from pressing Enter is consumed immediately by `nextLine()`, resulting in an empty string.',
                    'practice_question': 'What method on `Scanner` consumes an entire remaining line including whitespace? (Answer: `nextLine()`).'
                },
                {
                    'id': 'java-control-flow',
                    'title': '6. Control Flow: if, else-if, else & Modern switch',
                    'read_time': '10 min',
                    'summary': 'Implement branching logic using conditional ladders and modern Java 14+ enhanced switch expressions.',
                    'concept': """Control flow directs execution paths based on runtime booleans.
- `if-else` statement: Standard conditional branch.
- Modern `switch` expression (Java 14+): Eliminates fall-through bugs by using the arrow `->` syntax. Can return a value directly and does not require manual `break` statements.""",
                    'syntax': """// Enhanced switch expression
String levelTitle = switch (level) {
    case 1 -> "Easy";
    case 2 -> "Medium";
    case 3 -> "Complex";
    default -> "Unknown";
};
""",
                    'code_example': """public class ControlFlowDemo {
    public static void main(String[] args) {
        int levelCode = 2;
        
        String difficulty = switch (levelCode) {
            case 1 -> "Level 1: Beginner Foundations";
            case 2 -> "Level 2: Intermediate Problem Solving";
            case 3 -> "Level 3: Advanced Optimization";
            default -> "Invalid Level Code";
        };
        
        System.out.println("Configured Track: " + difficulty);
    }
}
""",
                    'expected_output': """Configured Track: Level 2: Intermediate Problem Solving
""",
                    'common_mistakes': 'In traditional `switch` statements, omitting the `break;` statement causes case fall-through, executing subsequent cases unintentionally.',
                    'practice_question': 'Does the modern Java arrow `->` switch syntax require an explicit `break;` statement to prevent fall-through? (Answer: No).'
                },
                {
                    'id': 'java-loops',
                    'title': '7. Loops: for, enhanced for-each, while & do-while',
                    'read_time': '10 min',
                    'summary': 'Iterate through data using standard index loops, enhanced for-each iteration, while, and do-while loops.',
                    'concept': """Java provides four looping structures:
1. Standard `for` loop: Ideal when the iteration count is known beforehand (`for(int i = 0; i < n; i++)`).
2. Enhanced `for-each` loop: Clean syntax for traversing arrays and collections (`for(String item : items)`).
3. `while` loop: Evaluates the test condition at the top before executing the body.
4. `do-while` loop: Guarantees that the loop body executes at least once because the test condition is evaluated at the bottom.""",
                    'syntax': """for (int i = 0; i < 5; i++) { }
for (int val : arr) { }
while (condition) { }
do { } while (condition);
""",
                    'code_example': """public class LoopDemo {
    public static void main(String[] args) {
        int[] scores = {85, 92, 68, 74, 99};
        
        int total = 0;
        int passCount = 0;
        
        // Enhanced for-each traversal
        for (int s : scores) {
            total += s;
            if (s >= 70) {
                passCount++;
            }
        }
        
        double average = (double) total / scores.length;
        System.out.println("Total Assessments: " + scores.length);
        System.out.println("Pass Count: " + passCount);
        System.out.printf("Cohort Average: %.2f%n", average);
    }
}
""",
                    'expected_output': """Total Assessments: 5
Pass Count: 4
Cohort Average: 83.60
""",
                    'common_mistakes': 'Modifying the loop index variable inside the body of an enhanced for-each loop, expecting to change the underlying collection element.',
                    'practice_question': 'Which loop construct guarantees that its body will execute at least once? (Answer: The `do-while` loop).'
                },
                {
                    'id': 'java-arrays-1d',
                    'title': '8. One-Dimensional Arrays & java.util.Arrays',
                    'read_time': '10 min',
                    'summary': 'Allocate fixed-size sequential memory, avoid ArrayIndexOutOfBoundsException, and use Arrays utilities.',
                    'concept': """An array is a container object that holds a fixed number of values of a single type. Array length is established when the array is created in heap memory and cannot be altered dynamically.

Key Attributes:
- Zero-indexed: Elements range from index `0` to `length - 1`.
- `array.length`: An immutable public field (not a method) containing the element count.
- `java.util.Arrays`: Standard library utility offering helper methods like `Arrays.sort()`, `Arrays.binarySearch()`, `Arrays.toString()`, and `Arrays.equals()`.""",
                    'syntax': """int[] numbers = new int[5]; // Allocated with default values (0)
String[] subjects = {"Python", "Java", "DBMS", "DSA"};
""",
                    'code_example': """import java.util.Arrays;

public class ArrayDemo {
    public static void main(String[] args) {
        int[] quizScores = {94, 72, 88, 65, 99};
        
        System.out.println("Original: " + Arrays.toString(quizScores));
        Arrays.sort(quizScores);
        System.out.println("Sorted: " + Arrays.toString(quizScores));
        
        int min = quizScores[0];
        int max = quizScores[quizScores.length - 1];
        System.out.println("Lowest Score: " + min + " | Highest Score: " + max);
    }
}
""",
                    'expected_output': """Original: [94, 72, 88, 65, 99]
Sorted: [65, 72, 88, 94, 99]
Lowest Score: 65 | Highest Score: 99
""",
                    'common_mistakes': 'Accessing `arr[arr.length]`, which throws `ArrayIndexOutOfBoundsException`. The last valid index is always `arr.length - 1`.',
                    'practice_question': 'Is `length` an instance method or a field on Java arrays? (Answer: It is an immutable public field, written as `arr.length` without parentheses).'
                },
                {
                    'id': 'java-arrays-2d',
                    'title': '9. 2D Arrays & Jagged Array Structures',
                    'read_time': '10 min',
                    'summary': 'Model matrix structures, nested row-column iterations, and non-rectangular jagged arrays.',
                    'concept': """In Java, a multidimensional array is represented as an "array of arrays". A 2D array can be visualized as a grid of rows and columns.

Because Java treats 2D arrays as arrays of array references, rows do not need to be of uniform length. Arrays with variable row lengths are known as **Jagged Arrays**.""",
                    'syntax': """// Standard rectangular matrix (3 rows, 4 columns)
int[][] grid = new int[3][4];

// Jagged array declaration
int[][] jagged = new int[3][];
jagged[0] = new int[2];
jagged[1] = new int[4];
jagged[2] = new int[1];
""",
                    'code_example': """public class MatrixDemo {
    public static void main(String[] args) {
        // Student grades per subject: [student_idx][subject_score]
        int[][] studentGrades = {
            {85, 90, 78}, // Student 0
            {92, 88, 96}, // Student 1
            {70, 75, 80}  // Student 2
        };
        
        for (int i = 0; i < studentGrades.length; i++) {
            int rowSum = 0;
            for (int j = 0; j < studentGrades[i].length; j++) {
                rowSum += studentGrades[i][j];
            }
            double avg = (double) rowSum / studentGrades[i].length;
            System.out.printf("Student #%d Average: %.2f%n", i, avg);
        }
    }
}
""",
                    'expected_output': """Student #0 Average: 84.33
Student #1 Average: 92.00
Student #2 Average: 75.00
""",
                    'common_mistakes': 'Printing a 2D array with `System.out.println(grid)` produces hashcode memory markers like `[[I@15db9742`. Use `Arrays.deepToString(grid)` instead.',
                    'practice_question': 'Which utility method converts a multidimensional array to a readable string representation? (Answer: `Arrays.deepToString()`).'
                }
            ]
        },
        'medium': {
            'level_number': 2,
            'name': 'Medium (Level 2 - Object-Oriented Engineering)',
            'description': 'Strings, OOP encapsulation, inheritance, polymorphism, abstract classes, interfaces, and methods.',
            'topics': [
                {
                    'id': 'java-strings-builder',
                    'title': '1. String Immutability, String Pool & StringBuilder',
                    'read_time': '10 min',
                    'summary': 'Understand heap string pooling, thread-safe memory sharing, and efficient mutable StringBuilder.',
                    'concept': """In Java, `String` objects are immutable. Any operation that appears to modify a string actually creates a brand new string on the heap.
- **String Constant Pool**: A special memory region in the JVM heap. When string literals are created (`String s = "Java"`), the JVM checks the pool and reuses the existing instance.
- **StringBuilder**: A mutable sequence of characters. It avoids the $O(n^2)$ memory copying penalty of repeated `+` string concatenations in loops.
- `StringBuffer`: Thread-safe, synchronized alternative to StringBuilder (slightly slower due to lock overhead).""",
                    'syntax': """String s1 = "Hello"; // Pooled
String s2 = new String("Hello"); // Explicit heap allocation
s1 == s2; // false! Different memory references
s1.equals(s2); // true! Value comparison
""",
                    'code_example': """public class StringPoolDemo {
    public static void main(String[] args) {
        String literal1 = "EduAdapt";
        String literal2 = "EduAdapt";
        String created = new String("EduAdapt");
        
        System.out.println("literal1 == literal2: " + (literal1 == literal2)); // true (shared pool)
        System.out.println("literal1 == created: " + (literal1 == created));   // false (new object)
        System.out.println("literal1.equals(created): " + literal1.equals(created)); // true
        
        // Efficient concatenation using StringBuilder
        StringBuilder sb = new StringBuilder();
        sb.append("Course: ").append("Java").append(" | Level: ").append("Medium");
        System.out.println("Result: " + sb.toString());
    }
}
""",
                    'expected_output': """literal1 == literal2: true
literal1 == created: false
literal1.equals(created): true
Result: Course: Java | Level: Medium
""",
                    'common_mistakes': 'Comparing strings using `==` instead of `.equals()`. `==` compares reference addresses, while `.equals()` checks character content.',
                    'practice_question': 'Why should `StringBuilder` be preferred over repeated string concatenation (`+`) inside loops? (Answer: Because String is immutable, concatenation creates new temporary objects each iteration, causing $O(n^2)$ memory churn).'
                },
                {
                    'id': 'java-methods-scope',
                    'title': '2. Methods & Pass-by-Value Semantics',
                    'read_time': '9 min',
                    'summary': 'Master method signatures, return values, variable scope, and understand that Java is strictly pass-by-value.',
                    'concept': """A method is a collection of statements grouped together to perform a discrete operation.
Every Java method has a signature: `access_modifier return_type methodName(parameter_list)`

Crucial Principle: **Java is strictly Pass-by-Value**:
- When passing primitive variables, a copy of the primitive value is passed. Changes inside the method do not affect the original variable.
- When passing object references, a copy of the reference pointer is passed! Both pointers point to the exact same object in the heap. Therefore, mutating object fields inside the method modifies the caller's object, but reassigning the reference variable itself does not affect the caller's reference.""",
                    'syntax': """public static int computeSum(int a, int b) {
    return a + b;
}
""",
                    'code_example': """public class PassByValueDemo {
    static void modifyPrimitive(int x) {
        x = 999;
    }
    
    static void modifyArray(int[] arr) {
        arr[0] = 999; // Mutates heap contents
    }

    public static void main(String[] args) {
        int num = 10;
        int[] data = {10, 20, 30};
        
        modifyPrimitive(num);
        modifyArray(data);
        
        System.out.println("Primitive after method: " + num);
        System.out.println("Array[0] after method: " + data[0]);
    }
}
""",
                    'expected_output': """Primitive after method: 10
Array[0] after method: 999
""",
                    'common_mistakes': 'Assuming Java passes objects by reference. If you reassign the object parameter inside a method (`obj = new Object()`), the caller\'s reference remains unchanged.',
                    'practice_question': 'Is Java "pass-by-reference" or "pass-by-value"? (Answer: Java is strictly pass-by-value in all cases).'
                },
                {
                    'id': 'java-classes-constructors',
                    'title': '3. Classes, Objects & Constructor Overloading',
                    'read_time': '11 min',
                    'summary': 'Model domain entities with private state, public constructors, constructor chaining via this(), and GC.',
                    'concept': """A class is a blueprint from which individual objects are instantiated.
- **Constructors**: Special methods invoked when an object is created with `new`. They carry the exact name of the class and have no return type.
- **Default Constructor**: If no constructor is defined in a class, the compiler automatically injects a no-argument default constructor.
- **Constructor Chaining (`this(...)`)**: Allows one constructor to invoke another constructor within the same class, eliminating duplicated initialization code.""",
                    'syntax': """public class Course {
    private String name;
    private int hours;
    
    public Course(String name) {
        this(name, 40); // Chains to two-arg constructor
    }
    
    public Course(String name, int hours) {
        this.name = name;
        this.hours = hours;
    }
}
""",
                    'code_example': """public class StudentAccount {
    private String studentId;
    private String name;
    private double gpa;

    public StudentAccount(String studentId, String name) {
        this(studentId, name, 0.0);
    }

    public StudentAccount(String studentId, String name, double gpa) {
        this.studentId = studentId;
        this.name = name;
        this.gpa = gpa;
    }

    public void display() {
        System.out.println("Student: " + name + " [ID: " + studentId + "] GPA: " + gpa);
    }

    public static void main(String[] args) {
        StudentAccount s1 = new StudentAccount("STU-1", "Maya");
        StudentAccount s2 = new StudentAccount("STU-2", "Dev", 3.85);
        s1.display();
        s2.display();
    }
}
""",
                    'expected_output': """Student: Maya [ID: STU-1] GPA: 0.0
Student: Dev [ID: STU-2] GPA: 3.85
""",
                    'common_mistakes': 'Calling `this(...)` anywhere other than the very first statement of a constructor body, which causes a compiler error.',
                    'practice_question': 'What must be the very first line of code inside a constructor when performing constructor chaining? (Answer: The call to `this(...)` or `super(...)`).'
                },
                {
                    'id': 'java-access-modifiers',
                    'title': '4. Access Modifiers & Package Organization',
                    'read_time': '9 min',
                    'summary': 'Control visibility across packages using public, protected, package-private (default), and private.',
                    'concept': """Access modifiers enforce information hiding and architectural boundaries:
- `private`: Accessible only within the enclosing class.
- *package-private* (no keyword): Accessible by any class within the same package.
- `protected`: Accessible within the same package, plus subclasses in other packages.
- `public`: Accessible from any other class in any package.

Packages (`package com.eduadapt.models;`) group related classes and prevent naming collisions.""",
                    'syntax': """package com.eduadapt.core;

public class SecurityAudit {
    private String secretKey;      // Enclosing class only
    protected String role;         // Package + subclasses
    public String publicStatus;    // Anywhere
}
""",
                    'code_example': """public class AccessDemo {
    private int privateVal = 10;
    protected int protectedVal = 20;
    public int publicVal = 30;

    public void printValues() {
        System.out.printf("Private: %d, Protected: %d, Public: %d%n", 
                          privateVal, protectedVal, publicVal);
    }

    public static void main(String[] args) {
        AccessDemo demo = new AccessDemo();
        demo.printValues();
    }
}
""",
                    'expected_output': """Private: 10, Protected: 20, Public: 30
""",
                    'common_mistakes': 'Declaring entity instance variables as `public`, breaking encapsulation and allowing external classes to put the object into an inconsistent state.',
                    'practice_question': 'What is the visibility of a member declared without any access modifier in Java? (Answer: Package-private / default visibility, accessible only within the same package).'
                },
                {
                    'id': 'java-encapsulation',
                    'title': '5. Encapsulation & JavaBean Standards',
                    'read_time': '10 min',
                    'summary': 'Protect internal state with private fields, validated getters/setters, and immutable object patterns.',
                    'concept': """Encapsulation is the OOP pillar that restricts direct access to an object's internal representation while exposing safe methods to inspect and mutate state.

Best Practices:
1. Declare instance fields as `private`.
2. Provide public accessor (getter) methods: `getFieldName()`.
3. Provide public mutator (setter) methods with strict boundary validation: `setFieldName(value)`.
4. Return defensive copies of mutable internal objects (e.g. `Date` or `List`) to prevent external tampering.""",
                    'syntax': """public class ModuleScore {
    private int score;

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("Score must be between 0 and 100.");
        }
        this.score = score;
    }
}
""",
                    'code_example': """public class EncapsulationDemo {
    public static void main(String[] args) {
        ModuleScore ms = new ModuleScore();
        ms.setScore(85);
        System.out.println("Valid score set: " + ms.getScore());
        
        try {
            ms.setScore(150);
        } catch (IllegalArgumentException e) {
            System.out.println("Caught validation error: " + e.getMessage());
        }
    }
}
""",
                    'expected_output': """Valid score set: 85
Caught validation error: Score must be between 0 and 100.
""",
                    'common_mistakes': 'Writing setters that directly assign mutable references without validation or defensive copying.',
                    'practice_question': 'What design principle requires making fields private and mediating access through public getters and setters? (Answer: Encapsulation).'
                },
                {
                    'id': 'java-inheritance-super',
                    'title': '6. Inheritance with extends & the super Keyword',
                    'read_time': '11 min',
                    'summary': 'Construct class hierarchies using extends, call parent constructors with super(), and inherit java.lang.Object.',
                    'concept': """Inheritance models an "IS-A" relationship between a generalized superclass and a specialized subclass.
- In Java, a class can extend at most one superclass (Single Class Inheritance).
- Every class in Java implicitly subclasses `java.lang.Object`, inheriting methods like `toString()`, `equals()`, `hashCode()`, and `getClass()`.
- The `super` keyword refers directly to the immediate parent class, allowing invocation of superclass constructors (`super(args)`) and overridden methods (`super.method()`).""",
                    'syntax': """public class SubClass extends SuperClass {
    public SubClass(String name) {
        super(name); // Call superclass constructor
    }
}
""",
                    'code_example': """class Assessment {
    protected String title;
    protected int totalMarks;

    public Assessment(String title, int totalMarks) {
        this.title = title;
        this.totalMarks = totalMarks;
    }

    public void display() {
        System.out.println("Assessment: " + title + " (Max: " + totalMarks + ")");
    }
}

class CodingAssignment extends Assessment {
    private String language;

    public CodingAssignment(String title, int totalMarks, String language) {
        super(title, totalMarks);
        this.language = language;
    }

    @Override
    public void display() {
        super.display();
        System.out.println("Environment: " + language);
    }
}

public class InheritanceDemo {
    public static void main(String[] args) {
        CodingAssignment ca = new CodingAssignment("Java Algorithms", 100, "Java 21");
        ca.display();
    }
}
""",
                    'expected_output': """Assessment: Java Algorithms (Max: 100)
Environment: Java 21
""",
                    'common_mistakes': 'Attempting multiple class inheritance (`class C extends A, B`). Java does not support multiple class inheritance to avoid the Diamond Problem. Use interfaces instead.',
                    'practice_question': 'Does Java support multiple class inheritance? (Answer: No, Java allows a class to extend only one superclass).'
                },
                {
                    'id': 'java-polymorphism',
                    'title': '7. Polymorphism: Overloading vs Overriding',
                    'read_time': '11 min',
                    'summary': 'Distinguish compile-time method overloading from runtime dynamic method dispatch (overriding).',
                    'concept': """Polymorphism allows objects to be treated as instances of their parent class or interface while executing subclass-specific behavior at runtime.
1. **Compile-time Polymorphism (Method Overloading)**: Multiple methods in the same class share the same name but have different parameter lists (different types, count, or order). Resolved at compile time.
2. **Runtime Polymorphism (Method Overriding)**: A subclass provides a specific implementation of a method declared in its parent class. The method signature must match exactly. Resolved at runtime via **Dynamic Method Dispatch**.""",
                    'syntax': """// Overloading (Compile-time)
int add(int a, int b);
double add(double a, double b);

// Overriding (Runtime)
@Override
public void execute();
""",
                    'code_example': """class ContentNode {
    public void render() {
        System.out.println("Rendering generic content node.");
    }
}

class VideoNode extends ContentNode {
    @Override
    public void render() {
        System.out.println("Rendering interactive video player.");
    }
}

class QuizNode extends ContentNode {
    @Override
    public void render() {
        System.out.println("Rendering interactive assessment quiz.");
    }
}

public class PolyDemo {
    public static void main(String[] args) {
        ContentNode[] curriculum = { new VideoNode(), new QuizNode() };
        
        for (ContentNode node : curriculum) {
            node.render(); // Dynamic method dispatch invokes specific version
        }
    }
}
""",
                    'expected_output': """Rendering interactive video player.
Rendering interactive assessment quiz.
""",
                    'common_mistakes': 'Typoing an overridden method name without using the `@Override` annotation. Without `@Override`, the compiler treats it as a new method instead of flagging the mismatch.',
                    'practice_question': 'What Java annotation ensures that a method is correctly overriding a superclass method? (Answer: `@Override`).'
                },
                {
                    'id': 'java-abstract-classes',
                    'title': '8. Abstract Classes & Template Method Pattern',
                    'read_time': '10 min',
                    'summary': 'Create incomplete base classes using abstract, define template algorithm workflows, and defer details to subclasses.',
                    'concept': """An **Abstract Class** is a class declared with the `abstract` keyword that cannot be instantiated directly. It can contain:
- Concrete methods with full implementations.
- Abstract methods (`public abstract void solve()`) that have no body and MUST be overridden by concrete subclasses.
- Instance variables and constructors (called via `super()` by subclasses).

Abstract classes are ideal for the **Template Method Pattern**, where a parent class outlines the fixed skeleton of an algorithm while letting subclasses override specific steps.""",
                    'syntax': """public abstract class LearningEngine {
    // Template method
    public final void learn() {
        readMaterial();
        takeQuiz();
    }
    
    protected abstract void readMaterial();
    protected abstract void takeQuiz();
}
""",
                    'code_example': """abstract class CourseModule {
    protected String title;

    public CourseModule(String title) {
        this.title = title;
    }

    public void startModule() {
        System.out.println(">> Commencing: " + title);
        presentContent();
        verifyCompletion();
    }

    protected abstract void presentContent();
    protected abstract void verifyCompletion();
}

class JavaModule extends CourseModule {
    public JavaModule() { super("Java OOP Masterclass"); }

    @Override
    protected void presentContent() {
        System.out.println("Reading OOP inheritance and polymorphism notes.");
    }

    @Override
    protected void verifyCompletion() {
        System.out.println("Submitting Level 2 assessment with 85% score.");
    }
}

public class AbstractDemo {
    public static void main(String[] args) {
        CourseModule m = new JavaModule();
        m.startModule();
    }
}
""",
                    'expected_output': """>> Commencing: Java OOP Masterclass
Reading OOP inheritance and polymorphism notes.
Submitting Level 2 assessment with 85% score.
""",
                    'common_mistakes': 'Declaring an abstract method as `private` or `final`. Abstract methods must be overridden by subclasses, so they can never be private or final.',
                    'practice_question': 'Can an abstract class have constructors in Java? (Answer: Yes, which are invoked by subclass constructors via `super()`).'
                },
                {
                    'id': 'java-interfaces',
                    'title': '9. Interfaces, Multiple Inheritance & Default Methods',
                    'read_time': '11 min',
                    'summary': 'Declare behavioral contracts using interface, implement multiple interfaces, and leverage Java 8 default methods.',
                    'concept': """An `interface` in Java is a reference type representing a contract of behavior. Classes declare adherence to an interface using the `implements` keyword. A class can implement multiple interfaces!

Modern Java Interfaces (Java 8+):
- **Abstract Methods**: Public methods without a body (implicitly `public abstract`).
- **Default Methods (`default`)**: Interface methods with default concrete implementations, allowing API evolution without breaking existing implementing classes.
- **Static Methods**: Utility methods scoped to the interface namespace.
- **Fields**: Implicitly `public static final` (constants).""",
                    'syntax': """public interface Evaluatable {
    double calculateScore();
    
    default boolean isPassing() {
        return calculateScore() >= 70.0;
    }
}
""",
                    'code_example': """interface Trackable {
    void trackProgress(int topicIndex);
}

interface Certifiable {
    String generateCertificate();
}

class StudentJourney implements Trackable, Certifiable {
    @Override
    public void trackProgress(int topicIndex) {
        System.out.println("Tracked topic completion: #" + topicIndex);
    }

    @Override
    public String generateCertificate() {
        return "CERT-JAVA-MEDIUM-2026";
    }
}

public class InterfaceDemo {
    public static void main(String[] args) {
        StudentJourney journey = new StudentJourney();
        journey.trackProgress(5);
        System.out.println("Credential Issued: " + journey.generateCertificate());
    }
}
""",
                    'expected_output': """Tracked topic completion: #5
Credential Issued: CERT-JAVA-MEDIUM-2026
""",
                    'common_mistakes': 'Assuming interface fields can be re-assigned. Interface variables are implicitly `public static final` constants.',
                    'practice_question': 'How many interfaces can a single Java class implement? (Answer: An unlimited number / multiple interfaces).'
                }
            ]
        },
        'complex': {
            'level_number': 3,
            'name': 'Complex (Level 3 - Enterprise Engineering & Concurrency)',
            'description': 'Exception propagation, generics, collections, streams, lambdas, multithreading, synchronization, and modern file NIO.',
            'topics': [
                {
                    'id': 'java-exceptions-advanced',
                    'title': '1. Advanced Exception Handling: Checked vs Unchecked & AutoCloseable',
                    'read_time': '12 min',
                    'summary': 'Master try-with-resources, checked vs unchecked exceptions, custom exception hierarchies, and multi-catch.',
                    'concept': """Java exceptions inherit from `java.lang.Throwable`:
1. **Checked Exceptions** (subclasses of `Exception` excluding `RuntimeException`): Verified at compile time. Methods must declare them via `throws` or handle them in a `try-catch` block (e.g. `IOException`, `SQLException`).
2. **Unchecked Exceptions** (subclasses of `RuntimeException`): Occur during execution due to programming flaws (e.g. `NullPointerException`, `IndexOutOfBoundsException`). Compile-time declaration is optional.
3. **Errors** (subclasses of `Error`): Serious system issues (e.g. `OutOfMemoryError`, `StackOverflowError`) that normal applications should not attempt to handle.

**Try-with-Resources**: Any class implementing `java.lang.AutoCloseable` can be instantiated inside `try (Resource r = ...)` and will be closed automatically when exiting the block.""",
                    'syntax': """try (AutoCloseableResource res = new AutoCloseableResource()) {
    res.operate();
} catch (IOException | SQLException e) { // Multi-catch
    logger.error("Operation failed", e);
}
""",
                    'code_example': """class LevelLockedException extends Exception {
    private final String level;
    public LevelLockedException(String level, String msg) {
        super(msg);
        this.level = level;
    }
    public String getLevel() { return level; }
}

public class ExceptionArchitectureDemo {
    static void checkEligibility(int previousScore) throws LevelLockedException {
        if (previousScore < 70) {
            throw new LevelLockedException("Complex", "Score " + previousScore + "% < 70% threshold.");
        }
    }

    public static void main(String[] args) {
        try {
            checkEligibility(65);
            System.out.println("Access granted.");
        } catch (LevelLockedException e) {
            System.out.println("Caught Checked Exception: " + e.getMessage() + " for Level " + e.getLevel());
        }
    }
}
""",
                    'expected_output': """Caught Checked Exception: Score 65% < 70% threshold. for Level Complex
""",
                    'common_mistakes': 'Catching `Throwable` or `Exception` indiscriminately, which hides programming errors and interrupts proper thread termination.',
                    'practice_question': 'Which interface must a class implement to be safely managed inside a Java try-with-resources statement? (Answer: `java.lang.AutoCloseable`).'
                },
                {
                    'id': 'java-generics',
                    'title': '2. Java Generics: Type Parameters & Bounded Wildcards',
                    'read_time': '12 min',
                    'summary': 'Enforce compile-time type safety with generic classes, methods, type erasure, and PECS wildcards.',
                    'concept': """Generics enable types (classes and interfaces) to be parameters when defining classes, interfaces, and methods. Generics eliminate runtime `ClassCastException`s by providing compile-time type checking.

Key Concepts:
- **Type Parameters**: `<T>`, `<E>`, `<K, V>`.
- **Type Erasure**: The JVM removes all generic type information at compile time, replacing parameters with their bounds (or `Object`) and inserting casts. This ensures backward compatibility with pre-Java 5 code.
- **PECS Principle (Producer Extends, Consumer Super)**:
  - Use `<? extends T>` when the collection produces items (reading from collection).
  - Use `<? super T>` when the collection consumes items (writing into collection).""",
                    'syntax': """public class Response<T> {
    private T payload;
    public Response(T payload) { this.payload = payload; }
    public T getPayload() { return payload; }
}
""",
                    'code_example': """import java.util.List;

public class GenericsDemo {
    // Producer Extends: Read numbers from producer
    public static double sumOfList(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number n : numbers) {
            sum += n.doubleValue();
        }
        return sum;
    }

    public static void main(String[] args) {
        List<Integer> intScores = List.of(80, 90, 85);
        List<Double> doubleScores = List.of(88.5, 92.0, 79.5);
        
        System.out.println("Integer Sum: " + sumOfList(intScores));
        System.out.println("Double Sum: " + sumOfList(doubleScores));
    }
}
""",
                    'expected_output': """Integer Sum: 255.0
Double Sum: 260.0
""",
                    'common_mistakes': 'Trying to instantiate a generic array like `new T[10]`. Type erasure makes this illegal at compile time because the runtime type is unknown.',
                    'practice_question': 'What rule governs the choice between `<? extends T>` and `<? super T>` in Java Generics? (Answer: PECS: Producer Extends, Consumer Super).'
                },
                {
                    'id': 'java-collections',
                    'title': '3. Java Collections Framework: List, Set & Map Internals',
                    'read_time': '13 min',
                    'summary': 'Examine ArrayList resizing, LinkedList pointers, HashSet hashing, and HashMap hash table buckets.',
                    'concept': """The Collections Framework provides high-performance data structures:
- **`List`**: Ordered collections.
  - `ArrayList`: Dynamic array with $O(1)$ random access, $O(1)$ amortized append, $O(n)$ insertion/deletion.
  - `LinkedList`: Doubly linked list with $O(1)$ insertion at head/tail, $O(n)$ random lookup.
- **`Set`**: Unique collections.
  - `HashSet`: Backed by a `HashMap`. $O(1)$ operations assuming uniform hash distribution.
  - `TreeSet`: Red-Black tree providing $O(\\log n)$ sorted order.
- **`Map`**: Key-value pairings.
  - `HashMap`: Array of buckets (linked lists transitioning to Red-Black trees when collision count >= 8).""",
                    'syntax': """Map<String, Integer> scoreMap = new HashMap<>();
scoreMap.put("Python", 95);
scoreMap.getOrDefault("Java", 0);
""",
                    'code_example': """import java.util.*;

public class CollectionsInternalDemo {
    public static void main(String[] args) {
        Map<String, Integer> studentGrades = new HashMap<>();
        studentGrades.put("Alex", 92);
        studentGrades.put("Sam", 84);
        studentGrades.put("Taylor", 78);
        
        // Safe retrieval with fallback
        System.out.println("Alex Score: " + studentGrades.getOrDefault("Alex", 0));
        System.out.println("Jordan Score: " + studentGrades.getOrDefault("Jordan", -1));
        
        // Iterating map entries
        for (Map.Entry<String, Integer> entry : studentGrades.entrySet()) {
            System.out.println(" - " + entry.getKey() + ": " + entry.getValue());
        }
    }
}
""",
                    'expected_output': """Alex Score: 92
Jordan Score: -1
 - Alex: 92
 - Sam: 84
 - Taylor: 78
""",
                    'common_mistakes': 'Using custom objects as `HashMap` keys without overriding both `equals()` and `hashCode()`. Inconsistent implementations cause keys to be lost in the map.',
                    'practice_question': 'When does a Java HashMap bucket change from a linked list into a balanced red-black tree? (Answer: When bucket collisions reach the threshold of 8 items and total table capacity is at least 64).'
                },
                {
                    'id': 'java-lambdas-functional',
                    'title': '4. Java Lambdas & Built-in Functional Interfaces',
                    'read_time': '11 min',
                    'summary': 'Express anonymous behaviors concisely with lambdas, method references (::), and standard functional types.',
                    'concept': """Introduced in Java 8, lambdas allow treating functionality as method arguments or code as data.
A **Functional Interface** is an interface having exactly one abstract method (annotated with `@FunctionalInterface`).

Standard Java Functional Interfaces in `java.util.function`:
- `Predicate<T>`: `boolean test(T t)` — boolean conditions.
- `Function<T, R>`: `R apply(T t)` — transforms input to output.
- `Consumer<T>`: `void accept(T t)` — side effects, produces no output.
- `Supplier<T>`: `T get()` — factory, takes no input and produces output.
- Method references `ClassName::methodName` provide clean shorthand for invoking existing methods.""",
                    'syntax': """// Lambda
Predicate<Integer> isPassing = score -> score >= 70;

// Method reference
Consumer<String> printer = System.out::println;
""",
                    'code_example': """import java.util.function.Function;
import java.util.function.Predicate;

public class LambdaDemo {
    public static void main(String[] args) {
        Predicate<Integer> isPassing = score -> score >= 70;
        Function<Integer, String> gradeLetter = score -> {
            if (score >= 90) return "A";
            if (score >= 80) return "B";
            if (score >= 70) return "C";
            return "F";
        };
        
        int sample = 88;
        System.out.println("Score: " + sample);
        System.out.println("Passed? " + isPassing.test(sample));
        System.out.println("Letter Grade: " + gradeLetter.apply(sample));
    }
}
""",
                    'expected_output': """Score: 88
Passed? true
Letter Grade: B
""",
                    'common_mistakes': 'Attempting to modify a non-final local variable inside a lambda. Local variables referenced by lambdas must be "effectively final".',
                    'practice_question': 'What is the signature of the single abstract method in Java\'s `Predicate<T>` interface? (Answer: `boolean test(T t)`).'
                },
                {
                    'id': 'java-streams-api',
                    'title': '5. Java Stream API: Filter, Map, Reduce & Collectors',
                    'read_time': '12 min',
                    'summary': 'Process collections declaratively with lazy evaluation, intermediate filters/maps, and terminal collectors.',
                    'concept': """The Stream API (`java.util.stream.Stream`) provides a declarative, functional approach to processing sequences of elements.
- **Not a Data Structure**: Streams do not store data; they convey elements from a source (collection, array, I/O channel) through a computational pipeline.
- **Intermediate Operations**: Return a new stream and evaluate **lazily** (e.g. `filter()`, `map()`, `sorted()`, `distinct()`). No processing happens until a terminal operation is called!
- **Terminal Operations**: Produce a non-stream result or side-effect, closing the stream (e.g. `collect()`, `reduce()`, `forEach()`, `count()`, `findFirst()`).""",
                    'syntax': """List<String> honors = students.stream()
    .filter(s -> s.getScore() >= 90)
    .map(Student::getName)
    .sorted()
    .collect(Collectors.toList());
""",
                    'code_example': """import java.util.List;
import java.util.stream.Collectors;

public class StreamDemo {
    public static void main(String[] args) {
        List<Integer> quizScores = List.of(65, 88, 92, 70, 54, 99, 81);
        
        // Filter passing scores, calculate average
        double passingAvg = quizScores.stream()
            .filter(s -> s >= 70)
            .mapToInt(Integer::intValue)
            .average()
            .orElse(0.0);
            
        List<Integer> sortedPassing = quizScores.stream()
            .filter(s -> s >= 70)
            .sorted()
            .collect(Collectors.toList());
            
        System.out.println("Passing Scores: " + sortedPassing);
        System.out.printf("Passing Average: %.2f%n", passingAvg);
    }
}
""",
                    'expected_output': """Passing Scores: [70, 81, 88, 92, 99]
Passing Average: 86.00
""",
                    'common_mistakes': 'Attempting to reuse a stream after a terminal operation has already been executed. Streams are one-shot and throw `IllegalStateException: stream has already been operated upon or closed`.',
                    'practice_question': 'Are intermediate operations like `.filter()` and `.map()` on Java Streams evaluated eagerly or lazily? (Answer: Lazily, executing only when a terminal operation is invoked).'
                },
                {
                    'id': 'java-multithreading',
                    'title': '6. Multithreading: Thread Lifecycle & Runnable Interface',
                    'read_time': '12 min',
                    'summary': 'Spawn concurrent threads of execution, implement Runnable, and understand Thread lifecycle states.',
                    'concept': """Multithreading allows concurrent execution of multiple parts of a program, utilizing multi-core CPU architecture.
A thread is a lightweight unit of process execution.

Thread Creation Methods:
1. Implementing `java.lang.Runnable` (preferred): Decouples the task from thread execution, allowing the class to extend another class.
2. Extending `java.lang.Thread`.

Thread Lifecycle States:
`NEW` -> `RUNNABLE` -> `BLOCKED` / `WAITING` / `TIMED_WAITING` -> `TERMINATED`.""",
                    'syntax': """Thread t = new Thread(() -> {
    System.out.println("Concurrent task executing in: " + Thread.currentThread().getName());
});
t.start(); // Spawns OS thread
t.join();  // Awaits termination
""",
                    'code_example': """public class ThreadingDemo {
    public static void main(String[] args) throws InterruptedException {
        Runnable backgroundTask = () -> {
            System.out.println("Worker thread starting: " + Thread.currentThread().getName());
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Worker thread finished: " + Thread.currentThread().getName());
        };
        
        Thread worker = new Thread(backgroundTask, "TutorBot-Worker-1");
        worker.start();
        
        System.out.println("Main thread awaiting worker...");
        worker.join();
        System.out.println("Main thread resumed. All tasks complete.");
    }
}
""",
                    'expected_output': """Main thread awaiting worker...
Worker thread starting: TutorBot-Worker-1
Worker thread finished: TutorBot-Worker-1
Main thread resumed. All tasks complete.
""",
                    'common_mistakes': 'Calling `thread.run()` instead of `thread.start()`. `run()` simply executes the method synchronously in the caller\'s thread without spawning a new thread!',
                    'practice_question': 'What method must be called to actually spawn a new operating system thread in Java? (Answer: `thread.start()`).'
                },
                {
                    'id': 'java-synchronization',
                    'title': '7. Synchronization, Locks & Concurrency Hazards',
                    'read_time': '12 min',
                    'summary': 'Prevent race conditions using synchronized blocks, ReentrantLock, and atomic variables (AtomicInteger).',
                    'concept': """When multiple threads read and write shared mutable state simultaneously, a **Race Condition** occurs, leading to corrupted data.

Concurrency Solutions:
1. `synchronized` keyword: Acquires the intrinsic monitor lock on the target object. Only one thread can enter the synchronized block or method at any given moment.
2. `java.util.concurrent.atomic.AtomicInteger`: Lock-free, thread-safe counter using hardware-level Compare-And-Swap (CAS) CPU instructions.
3. `ReentrantLock`: Explicit lock offering try-lock capabilities with timeouts and interruptible lock acquisition.""",
                    'syntax': """// Synchronized block
synchronized (lockObject) {
    criticalCounter++;
}

// Atomic variable
AtomicInteger atomicCounter = new AtomicInteger(0);
atomicCounter.incrementAndGet();
""",
                    'code_example': """import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrencyDemo {
    private static final AtomicInteger totalSubmissions = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 500; i++) totalSubmissions.incrementAndGet();
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 500; i++) totalSubmissions.incrementAndGet();
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Expected Submissions: 1000");
        System.out.println("Actual Atomic Count: " + totalSubmissions.get());
    }
}
""",
                    'expected_output': """Expected Submissions: 1000
Actual Atomic Count: 1000
""",
                    'common_mistakes': 'Synchronizing on different lock objects across threads or synchronizing on boxed primitive wrappers that change identity.',
                    'practice_question': 'What CPU-level mechanism allows `AtomicInteger` to be thread-safe without traditional locks? (Answer: Compare-And-Swap / CAS).'
                },
                {
                    'id': 'java-nio-files',
                    'title': '8. Modern File I/O with java.nio.file.Files & Path',
                    'read_time': '11 min',
                    'summary': 'Read and write disk resources cleanly using java.nio.file.Files, Path, and Stream-based line reading.',
                    'concept': """Java 7 introduced NIO.2 (`java.nio.file`), replacing the legacy `java.io.File` API with modern abstractions:
- `Path`: Represents a hierarchical path to a file or directory. Created via `Path.of("dir", "file.txt")`.
- `Files`: Utility class providing static methods for disk operations: `Files.readString()`, `Files.writeString()`, `Files.lines()`, `Files.exists()`, `Files.createDirectories()`.
- `Files.lines(Path)` returns a lazy `Stream<String>` that streams lines from disk without loading the entire multi-gigabyte file into memory at once.""",
                    'syntax': """Path path = Path.of("curriculum.txt");
Files.writeString(path, "Java Complex Curriculum\\n");
String content = Files.readString(path);
""",
                    'code_example': """import java.nio.file.Path;

public class ModernNioDemo {
    public static void main(String[] args) {
        Path projectRoot = Path.of("eduadapt", "java", "curriculum.json");
        
        System.out.println("File Name: " + projectRoot.getFileName());
        System.out.println("Parent Dir: " + projectRoot.getParent());
        System.out.println("Is Absolute: " + projectRoot.isAbsolute());
        System.out.println("Normalized Path: " + projectRoot.normalize());
    }
}
""",
                    'expected_output': """File Name: curriculum.json
Parent Dir: eduadapt\\java
Is Absolute: false
Normalized Path: eduadapt\\java\\curriculum.json
""",
                    'common_mistakes': 'Not closing streams returned by `Files.lines(Path)`, which keeps open file handles on the underlying operating system.',
                    'practice_question': 'Which package introduced in Java 7 provides modern, robust file handling via `Path` and `Files`? (Answer: `java.nio.file`).'
                },
                {
                    'id': 'java-design-patterns',
                    'title': '9. Enterprise Design Patterns: Singleton, Factory & DI',
                    'read_time': '12 min',
                    'summary': 'Structure clean enterprise architectures using Double-Checked Locking Singleton, Factory, and Inversion of Control.',
                    'concept': """Design patterns are battle-tested solutions to recurring software architecture challenges:
1. **Singleton Pattern**: Ensures a class has only one instance and provides a global access point. Implemented via private constructor and `volatile` double-checked locking.
2. **Factory Method Pattern**: Defines an interface for creating an object, but lets subclasses decide which class to instantiate.
3. **Dependency Injection (DI)**: Inversion of Control technique where an object receives its dependencies from an external assembler rather than creating them itself with `new`.""",
                    'syntax': """public class ConfigurationService {
    private static volatile ConfigurationService instance;
    private ConfigurationService() {}
    
    public static ConfigurationService getInstance() {
        if (instance == null) {
            synchronized (ConfigurationService.class) {
                if (instance == null) instance = new ConfigurationService();
            }
        }
        return instance;
    }
}
""",
                    'code_example': """interface TutorService {
    String provideHint(String topic);
}

class JavaTutorService implements TutorService {
    @Override
    public String provideHint(String topic) {
        return "Java Hint: Remember to check interface contracts for " + topic;
    }
}

class TutorFactory {
    public static TutorService getTutor(String language) {
        if ("java".equalsIgnoreCase(language)) {
            return new JavaTutorService();
        }
        throw new IllegalArgumentException("Unsupported language: " + language);
    }
}

public class PatternDemo {
    public static void main(String[] args) {
        TutorService tutor = TutorFactory.getTutor("java");
        System.out.println(tutor.provideHint("Collections"));
    }
}
""",
                    'expected_output': """Java Hint: Remember to check interface contracts for Collections
""",
                    'common_mistakes': 'Omitting the `volatile` modifier on the singleton instance field when using double-checked locking, allowing instruction reordering bugs.',
                    'practice_question': 'Why is the `volatile` keyword mandatory for thread-safe Double-Checked Locking in the Singleton pattern? (Answer: To prevent the JVM compiler from reordering instruction writes before object initialization is complete).'
                }
            ]
        }
    }
}
