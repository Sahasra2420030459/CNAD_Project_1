"""
Assignment Assessment Questions for EduAdapt-AI
Contains 10 high-quality multiple choice questions per subject per level:
4 Subjects x 3 Levels = 12 Assessments x 10 Questions = 120 Questions.
Every question includes 4 options, a correct_index, and a detailed pedagogical explanation.
"""

ASSIGNMENT_QUESTIONS = {
    'python': {
        'easy': [
            {
                'id': 'py-e-1',
                'question': 'Which component of Python is responsible for converting bytecode into machine instructions during execution?',
                'options': [
                    'The CPython compiler (javac equivalent)',
                    'The Python Virtual Machine (PVM)',
                    'The OS Kernel linker',
                    'The PEP 8 linter'
                ],
                'correct_index': 1,
                'explanation': 'The Python Virtual Machine (PVM) is the runtime engine of CPython that reads compiled bytecode (.pyc) and translates it into machine instructions.'
            },
            {
                'id': 'py-e-2',
                'question': 'What is the output of the expression: type(10 / 2) in Python 3?',
                'options': [
                    "<class 'int'>",
                    "<class 'float'>",
                    "<class 'double'>",
                    "<class 'number'>"
                ],
                'correct_index': 1,
                'explanation': 'In Python 3, the standard division operator `/` always produces a floating-point number (`float`), even when the division divides evenly. To perform integer floor division, `//` is used.'
            },
            {
                'id': 'py-e-3',
                'question': 'Which of the following is an immutable data type in Python?',
                'options': [
                    'list',
                    'set',
                    'dict',
                    'tuple'
                ],
                'correct_index': 3,
                'explanation': 'Tuples (`tuple`), strings (`str`), integers (`int`), and floats are immutable in Python. Lists, dictionaries, and sets are mutable.'
            },
            {
                'id': 'py-e-4',
                'question': 'What does `bool("")` and `bool([0])` evaluate to in Python?',
                'options': [
                    'False and False',
                    'True and True',
                    'False and True',
                    'True and False'
                ],
                'correct_index': 2,
                'explanation': 'An empty string `""` is falsy (`False`), whereas a non-empty list `[0]` has length 1 and is therefore truthy (`True`), regardless of the element value inside.'
            },
            {
                'id': 'py-e-5',
                'question': 'Given `s = "EduAdapt"`, what does `s[::-1]` produce?',
                'options': [
                    '"EduAdapt"',
                    '"tpadaudE"',
                    '"tpadaud"',
                    '"tpAdAudE"'
                ],
                'correct_index': 1,
                'explanation': 'Extended slicing with a step of `-1` (`[::-1]`) reverses the string, producing `"tpadaudE"`.'
            },
            {
                'id': 'py-e-6',
                'question': 'Which keyword is used to skip the rest of the current loop iteration and jump directly to the next iteration?',
                'options': [
                    'pass',
                    'break',
                    'continue',
                    'skip'
                ],
                'correct_index': 2,
                'explanation': '`continue` halts execution of the current iteration and advances the loop counter to the next iteration. `break` terminates the loop entirely.'
            },
            {
                'id': 'py-e-7',
                'question': 'How can you retrieve the value associated with key "score" from dictionary `d` without raising a `KeyError` if the key is missing?',
                'options': [
                    'd["score"]',
                    'd.get("score", 0)',
                    'd.fetch("score")',
                    'd.search("score")'
                ],
                'correct_index': 1,
                'explanation': 'The `.get(key, default)` method safely looks up a key, returning the specified fallback default (or `None`) if the key is absent.'
            },
            {
                'id': 'py-e-8',
                'question': 'What is the output of `[1, 2] * 3` in Python?',
                'options': [
                    '[3, 6]',
                    '[1, 2, 1, 2, 1, 2]',
                    '[[1, 2], [1, 2], [1, 2]]',
                    'TypeError: unsupported operand'
                ],
                'correct_index': 1,
                'explanation': 'Multiplying a list by an integer $k$ produces a new list repeating the original sequence $k$ times: `[1, 2, 1, 2, 1, 2]`.'
            },
            {
                'id': 'py-e-9',
                'question': 'Which of the following will create an empty set in Python?',
                'options': [
                    's = {}',
                    's = set()',
                    's = []',
                    's = ()'
                ],
                'correct_index': 1,
                'explanation': '`{}` constructs an empty dictionary. An empty set must be instantiated using the constructor `set()`.'
            },
            {
                'id': 'py-e-10',
                'question': 'What does `print(17 // 4, 17 % 4)` display?',
                'options': [
                    '4.25 1',
                    '4 1',
                    '4 0.25',
                    '4.0 1'
                ],
                'correct_index': 1,
                'explanation': 'Floor division `17 // 4` yields the integer quotient `4`, and modulus `17 % 4` yields the integer remainder `1`.'
            }
        ],
        'medium': [
            {
                'id': 'py-m-1',
                'question': 'What is the danger of using a mutable object as a default argument, such as `def append_item(x, lst=[])`?',
                'options': [
                    'It raises a SyntaxError at compile time',
                    'The default list is instantiated once at function definition time and shared across all invocations',
                    'The list is automatically destroyed after the first return',
                    'It forces the function to run in a separate thread'
                ],
                'correct_index': 1,
                'explanation': 'Python default arguments are evaluated once when the function is defined. If a mutable object like a list or dictionary is used, state mutations persist across subsequent function calls.'
            },
            {
                'id': 'py-m-2',
                'question': 'Which rule determines the sequence Python follows when resolving variable names?',
                'options': [
                    'FIFO (First-In, First-Out)',
                    'LEGB (Local, Enclosing, Global, Built-in)',
                    'SOLID design principle',
                    'MRO (Method Resolution Order)'
                ],
                'correct_index': 1,
                'explanation': 'The LEGB rule dictates that Python searches for identifiers in Local scope first, then Enclosing (outer functions), then Global (module level), and lastly Built-in.'
            },
            {
                'id': 'py-m-3',
                'question': 'What does the list comprehension `[x for x in range(10) if x % 2 != 0]` produce?',
                'options': [
                    '[0, 2, 4, 6, 8]',
                    '[1, 3, 5, 7, 9]',
                    '[2, 4, 6, 8, 10]',
                    '[1, 2, 3, 4, 5]'
                ],
                'correct_index': 1,
                'explanation': '`range(10)` generates integers 0 to 9. The condition `x % 2 != 0` filters for odd numbers, producing `[1, 3, 5, 7, 9]`.'
            },
            {
                'id': 'py-m-4',
                'question': 'What is the primary benefit of using the `with` statement when opening files?',
                'options': [
                    'It speeds up hard drive disk rotation',
                    'It guarantees that the file descriptor is closed automatically, even if an exception occurs',
                    'It bypasses operating system read/write permissions',
                    'It enables automatic multi-threaded file reading'
                ],
                'correct_index': 1,
                'explanation': 'The `with` statement invokes the context manager protocol (`__enter__` and `__exit__`), guaranteeing that the file is safely closed when exiting the block.'
            },
            {
                'id': 'py-m-5',
                'question': 'What does the `else` block of a `try-except-else-finally` construct do?',
                'options': [
                    'Executes only if an unhandled exception occurred',
                    'Executes only if NO exceptions were raised in the try block',
                    'Executes before the try block starts',
                    'Executes instead of the finally block'
                ],
                'correct_index': 1,
                'explanation': 'The `else` clause in a try statement runs exclusively when the `try` block completes successfully without raising any exceptions.'
            },
            {
                'id': 'py-m-6',
                'question': 'In Python OOP, what is `self` inside an instance method?',
                'options': [
                    'A keyword that creates a copy of the class',
                    'An explicit reference to the current instance of the class',
                    'A pointer to the parent base class',
                    'A global module variable'
                ],
                'correct_index': 1,
                'explanation': '`self` is the convention representing the specific object instance invoking the method, allowing access to instance attributes and methods.'
            },
            {
                'id': 'py-m-7',
                'question': 'What function is used to invoke the parent class method or constructor from a child class?',
                'options': [
                    'parent()',
                    'super()',
                    'base()',
                    'inherit()'
                ],
                'correct_index': 1,
                'explanation': '`super()` delegates method calls to the parent superclass or cooperative MRO hierarchy.'
            },
            {
                'id': 'py-m-8',
                'question': 'What is "Duck Typing" in Python?',
                'options': [
                    'Enforcing rigid subclass inheritance checking',
                    'Checking an object suitability based on the presence of methods/attributes rather than its explicit class type',
                    'Compiling Python code into C extensions',
                    'Using duck-shaped symbols in regular expressions'
                ],
                'correct_index': 1,
                'explanation': '"If it walks like a duck and quacks like a duck, it is a duck" means Python focuses on whether an object can perform the required behavior (methods) rather than its formal class inheritance.'
            },
            {
                'id': 'py-m-9',
                'question': 'What keyword is used inside a nested function to modify a variable in the nearest enclosing non-global scope?',
                'options': [
                    'global',
                    'nonlocal',
                    'outer',
                    'enclosing'
                ],
                'correct_index': 1,
                'explanation': '`nonlocal` declares that a variable refers to a previously bound variable in the nearest enclosing scope (excluding globals).'
            },
            {
                'id': 'py-m-10',
                'question': 'What exception is raised when recursion depth exceeds the interpreter call stack limit?',
                'options': [
                    'MemoryError',
                    'StackOverflowError',
                    'RecursionError',
                    'DepthExceededException'
                ],
                'correct_index': 2,
                'explanation': 'Python raises `RecursionError: maximum recursion depth exceeded` when the maximum call stack depth (default ~1000) is exceeded.'
            }
        ],
        'complex': [
            {
                'id': 'py-c-1',
                'question': 'How does Python perform Name Mangling on class attributes declared with a double underscore (e.g. `__secret` in class `Bank`)?',
                'options': [
                    'It encrypts the value using SHA-256',
                    'It renames the attribute to `_Bank__secret` to prevent accidental namespace collisions in subclasses',
                    'It moves the attribute to an external SQLite database',
                    'It makes the attribute completely inaccessible from Python bytecode'
                ],
                'correct_index': 1,
                'explanation': 'Python name mangles attributes starting with at least two underscores and at most one trailing underscore by prefixing `_ClassName`, transforming `__secret` into `_Bank__secret`.'
            },
            {
                'id': 'py-c-2',
                'question': 'What is the key advantage of a generator function using `yield` over returning a standard list?',
                'options': [
                    'Generators execute with C-speed parallelism on multiple CPU cores',
                    'Generators evaluate lazily, consuming $O(1)$ memory by producing items on demand',
                    'Generators can only yield strings',
                    'Generators prevent all runtime exceptions'
                ],
                'correct_index': 1,
                'explanation': 'Generators produce items lazily via the iterator protocol (`__next__`), allowing massive or infinite sequences to be streamed with constant memory.'
            },
            {
                'id': 'py-c-3',
                'question': 'Why is `@functools.wraps(fn)` standard practice when authoring custom function decorators?',
                'options': [
                    'It compiles the function with Cython',
                    'It preserves the original function metadata, such as its name (`__name__`) and docstring (`__doc__`)',
                    'It automatically retries network requests on failure',
                    'It caches all function return values in memory'
                ],
                'correct_index': 1,
                'explanation': 'Without `@functools.wraps`, the decorated function assumes the name and docstring of the internal wrapper closure (`wrapper`), breaking introspection and documentation tools.'
            },
            {
                'id': 'py-c-4',
                'question': 'What magic methods must a class implement to conform to Python Context Manager protocol?',
                'options': [
                    '__start__ and __stop__',
                    '__open__ and __close__',
                    '__enter__ and __exit__',
                    '__init__ and __del__'
                ],
                'correct_index': 2,
                'explanation': 'A context manager class implements `__enter__(self)` to acquire resources and `__exit__(self, exc_type, exc_val, exc_tb)` to release them.'
            },
            {
                'id': 'py-c-5',
                'question': 'What happens if the `__exit__` method of a context manager returns `True` after an exception was raised inside the `with` block?',
                'options': [
                    'The program immediately terminates with exit code 1',
                    'The exception is suppressed and program execution continues normally after the with block',
                    'The exception is re-raised with a warning',
                    'The context manager executes a second time'
                ],
                'correct_index': 1,
                'explanation': 'Returning `True` from `__exit__` tells Python that the exception has been handled and should be suppressed.'
            },
            {
                'id': 'py-c-6',
                'question': 'In the function definition `def dispatch(*args, **kwargs):`, what are the data types of `args` and `kwargs`?',
                'options': [
                    'list and dict',
                    'tuple and dict',
                    'tuple and list',
                    'generator and dict'
                ],
                'correct_index': 1,
                'explanation': '`*args` packages positional arguments into an immutable `tuple`, while `**kwargs` packages keyword arguments into a standard `dict`.'
            },
            {
                'id': 'py-c-7',
                'question': 'Which built-in module from the Python standard library provides abstract base class definitions and the `@abstractmethod` decorator?',
                'options': [
                    'interface',
                    'typing',
                    'abc',
                    'oop'
                ],
                'correct_index': 2,
                'explanation': 'The `abc` (Abstract Base Classes) module provides `ABC` and `@abstractmethod` to enforce interface contracts.'
            },
            {
                'id': 'py-c-8',
                'question': 'What is the average time complexity of checking membership `x in s` when `s` is a Python set of size $n$?',
                'options': [
                    'O(1)',
                    'O(log n)',
                    'O(n)',
                    'O(n log n)'
                ],
                'correct_index': 0,
                'explanation': 'Python sets are implemented using hash tables, providing average $O(1)$ constant time lookup, compared to $O(n)$ for a list.'
            },
            {
                'id': 'py-c-9',
                'question': 'In the `unittest` framework, which assertion method verifies that invoking a callable raises a specific exception?',
                'options': [
                    'self.assertThrows(Exception, callable)',
                    'self.assertRaises(ExceptionType)',
                    'self.assertError(ExceptionType)',
                    'self.assertException(callable)'
                ],
                'correct_index': 1,
                'explanation': '`self.assertRaises(ExceptionType)` is used either as a context manager (`with self.assertRaises(ValueError):`) or by passing the callable and its arguments.'
            },
            {
                'id': 'py-c-10',
                'question': 'What HTTP status code should a server return when an authenticated student attempts to view a curriculum level that is currently locked?',
                'options': [
                    '401 Unauthorized',
                    '403 Forbidden',
                    '404 Not Found',
                    '409 Conflict'
                ],
                'correct_index': 1,
                'explanation': '401 Unauthorized indicates missing authentication credentials. 403 Forbidden indicates the server knows who the user is, but the user does not possess authorization to access the resource (e.g. locked level).'
            }
        ]
    },
    'java': {
        'easy': [
            {
                'id': 'java-e-1',
                'question': 'What is the role of the Java Virtual Machine (JVM)?',
                'options': [
                    'To edit Java source code',
                    'To load compiled bytecode (.class files) and execute it on native OS hardware',
                    'To act as a version control system',
                    'To package Java libraries into Docker containers'
                ],
                'correct_index': 1,
                'explanation': 'The JVM provides the runtime engine that loads, verifies, and executes compiled Java bytecode on the target platform.'
            },
            {
                'id': 'java-e-2',
                'question': 'Why is the `main` method declared as `static` in Java?',
                'options': [
                    'So it cannot be modified by subclasses',
                    'So the JVM can invoke it directly without creating an instance of the class in memory',
                    'To allocate it in CPU register cache',
                    'To allow it to return integer exit codes'
                ],
                'correct_index': 1,
                'explanation': 'Declaring `main` as `static` allows the JVM runtime to call `ClassName.main(args)` directly before any objects have been instantiated.'
            },
            {
                'id': 'java-e-3',
                'question': 'What is the size in bytes and default value of a Java `int` primitive in memory?',
                'options': [
                    '2 bytes, default 0',
                    '4 bytes, default 0',
                    '8 bytes, default null',
                    '4 bytes, default 1'
                ],
                'correct_index': 1,
                'explanation': 'A Java `int` is a signed 32-bit (4 bytes) two\'s complement integer, with a default primitive field value of 0.'
            },
            {
                'id': 'java-e-4',
                'question': 'What is the result of `int a = 7; int b = 2; double c = a / b;` in Java?',
                'options': [
                    '3.5',
                    '3.0',
                    '3',
                    'Compilation error'
                ],
                'correct_index': 1,
                'explanation': 'Because both `a` and `b` are integers, `a / b` performs integer division resulting in `3`. That integer is then widened to `3.0` upon assignment to `double c`.'
            },
            {
                'id': 'java-e-5',
                'question': 'Which operator in Java evaluates the second operand only if the first operand is insufficient to determine the result?',
                'options': [
                    '& (bitwise AND)',
                    '&& (short-circuit logical AND)',
                    '| (bitwise OR)',
                    '^ (bitwise XOR)'
                ],
                'correct_index': 1,
                'explanation': '`&&` is the short-circuit logical AND operator. If the left operand evaluates to `false`, the right operand is never executed.'
            },
            {
                'id': 'java-e-6',
                'question': 'Which loop construct in Java is guaranteed to execute its code block at least once?',
                'options': [
                    'for loop',
                    'while loop',
                    'do-while loop',
                    'enhanced for-each loop'
                ],
                'correct_index': 2,
                'explanation': 'The `do-while` loop evaluates its condition expression at the bottom of the loop body, guaranteeing at least one execution.'
            },
            {
                'id': 'java-e-7',
                'question': 'Given `int[] arr = new int[5];`, what is the valid index range for this array?',
                'options': [
                    '1 to 5',
                    '0 to 4',
                    '0 to 5',
                    '-1 to 4'
                ],
                'correct_index': 1,
                'explanation': 'Java arrays are zero-indexed. An array of length 5 has valid indices 0, 1, 2, 3, and 4. Accessing index 5 raises `ArrayIndexOutOfBoundsException`.'
            },
            {
                'id': 'java-e-8',
                'question': 'How do you check the number of elements in a Java array `int[] nums`?',
                'options': [
                    'nums.length()',
                    'nums.size()',
                    'nums.length',
                    'nums.count'
                ],
                'correct_index': 2,
                'explanation': 'On Java arrays, `length` is an immutable public field (written as `nums.length` without parentheses), whereas on `String` it is a method `str.length()`.'
            },
            {
                'id': 'java-e-9',
                'question': 'Which method on `java.util.Scanner` reads an entire line of text including spaces?',
                'options': [
                    'scanner.next()',
                    'scanner.nextLine()',
                    'scanner.readLine()',
                    'scanner.readFull()'
                ],
                'correct_index': 1,
                'explanation': '`scanner.next()` stops reading at the first whitespace character, while `scanner.nextLine()` reads until the next newline character.'
            },
            {
                'id': 'java-e-10',
                'question': 'Which utility class provides helper methods such as `.sort()`, `.binarySearch()`, and `.toString()` for Java arrays?',
                'options': [
                    'java.lang.System',
                    'java.util.Arrays',
                    'java.util.Collections',
                    'java.lang.ArrayHelper'
                ],
                'correct_index': 1,
                'explanation': '`java.util.Arrays` contains static methods for manipulating primitive and object arrays.'
            }
        ],
        'medium': [
            {
                'id': 'java-m-1',
                'question': 'Why should you compare String objects using `str1.equals(str2)` rather than `str1 == str2`?',
                'options': [
                    '== is not supported for objects in Java',
                    '== compares memory reference addresses, while .equals() compares character contents',
                    '.equals() executes faster on modern multi-core processors',
                    '== causes a NullPointerException if strings are equal'
                ],
                'correct_index': 1,
                'explanation': 'In Java, `==` tests object identity (whether both variables point to the exact same memory location), whereas `.equals()` tests semantic value equality.'
            },
            {
                'id': 'java-m-2',
                'question': 'Why is `StringBuilder` preferred over repeated `+` string concatenation inside a loop?',
                'options': [
                    'StringBuilder is thread-safe with automatic locking',
                    'Strings are immutable, so repeated concatenation creates new heap objects and copies characters in O(n^2) time',
                    'The compiler disallows + inside loops',
                    'StringBuilder writes directly to console stdout'
                ],
                'correct_index': 1,
                'explanation': 'Because `String` is immutable, each `+` creates a new String object and copies the buffer, causing $O(n^2)$ memory copying. `StringBuilder` mutates its internal buffer in amortized $O(n)$ time.'
            },
            {
                'id': 'java-m-3',
                'question': 'Is Java "Pass-by-Value" or "Pass-by-Reference"?',
                'options': [
                    'Pass-by-Reference for objects, Pass-by-Value for primitives',
                    'Strictly Pass-by-Value in all cases',
                    'Strictly Pass-by-Reference in all cases',
                    'Determined by whether the method is declared static'
                ],
                'correct_index': 1,
                'explanation': 'Java is strictly pass-by-value. When an object reference is passed to a method, a copy of the reference pointer is passed by value.'
            },
            {
                'id': 'java-m-4',
                'question': 'What must be the first statement inside a constructor body when chaining to another constructor in the same class?',
                'options': [
                    'super()',
                    'this(...)',
                    'init()',
                    'return'
                ],
                'correct_index': 1,
                'explanation': 'Constructor chaining via `this(...)` or superclass invocation via `super(...)` must be the very first statement in a constructor body.'
            },
            {
                'id': 'java-m-5',
                'question': 'What is the visibility of a class member declared without any access modifier (default / package-private)?',
                'options': [
                    'Accessible from any class in any package',
                    'Accessible only within classes in the same package',
                    'Accessible only within the enclosing class',
                    'Accessible anywhere by subclasses'
                ],
                'correct_index': 1,
                'explanation': 'Default (package-private) access restricts visibility to classes within the exact same package.'
            },
            {
                'id': 'java-m-6',
                'question': 'Can a Java class extend more than one superclass using `extends`?',
                'options': [
                    'Yes, separated by commas',
                    'No, Java supports single class inheritance only',
                    'Yes, but only if all superclasses are abstract',
                    'Yes, up to a maximum of 3 superclasses'
                ],
                'correct_index': 1,
                'explanation': 'Java does not allow multiple class inheritance to avoid ambiguity (the Diamond Problem). A class can extend only one superclass, but can implement multiple interfaces.'
            },
            {
                'id': 'java-m-7',
                'question': 'What is the difference between method overloading and method overriding?',
                'options': [
                    'Overloading happens across parent/child classes at runtime; overriding happens in the same class at compile time',
                    'Overloading has the same name with different parameter signatures (compile-time); overriding re-implements a parent method with the exact same signature (runtime)',
                    'Overloading requires the @Override annotation',
                    'Overriding applies only to static methods'
                ],
                'correct_index': 1,
                'explanation': 'Overloading occurs within the same class with different parameters (resolved at compile time). Overriding replaces a superclass method in a subclass with identical signature (resolved at runtime via dynamic dispatch).'
            },
            {
                'id': 'java-m-8',
                'question': 'Can an `abstract` class be instantiated directly using `new AbstractClass()`?',
                'options': [
                    'Yes, if all its methods are implemented',
                    'No, abstract classes cannot be instantiated directly',
                    'Yes, by passing null to the constructor',
                    'Only within the package it is defined'
                ],
                'correct_index': 1,
                'explanation': 'An abstract class cannot be directly instantiated with `new`. It serves as a base class to be extended by concrete subclasses.'
            },
            {
                'id': 'java-m-9',
                'question': 'How many interfaces can a single Java class implement?',
                'options': [
                    'Exactly one',
                    'At most two',
                    'An unlimited number of interfaces',
                    'None if it already extends a class'
                ],
                'correct_index': 2,
                'explanation': 'A class can implement any number of interfaces separated by commas: `class MyClass implements InterfaceA, InterfaceB, InterfaceC`.'
            },
            {
                'id': 'java-m-10',
                'question': 'What feature introduced in Java 8 allows interfaces to provide concrete method implementations?',
                'options': [
                    'abstract methods',
                    'default methods',
                    'native methods',
                    'synchronized methods'
                ],
                'correct_index': 1,
                'explanation': '`default` methods in interfaces provide concrete default implementations, enabling API evolution without breaking existing implementing classes.'
            }
        ],
        'complex': [
            {
                'id': 'java-c-1',
                'question': 'What is the fundamental difference between checked and unchecked exceptions in Java?',
                'options': [
                    'Checked exceptions extend RuntimeException; unchecked exceptions extend Error',
                    'Checked exceptions are verified at compile time and must be handled or declared with throws; unchecked exceptions extend RuntimeException and are not checked at compile time',
                    'Unchecked exceptions crash the JVM immediately',
                    'Checked exceptions can only be caught in static methods'
                ],
                'correct_index': 1,
                'explanation': 'Checked exceptions (subclasses of `Exception` excluding `RuntimeException`) must be caught or declared via `throws`. Unchecked exceptions (`RuntimeException`) represent programming errors and need not be declared.'
            },
            {
                'id': 'java-c-2',
                'question': 'Which interface must a resource class implement to be managed automatically inside a `try-with-resources` statement?',
                'options': [
                    'java.lang.Runnable',
                    'java.lang.AutoCloseable',
                    'java.io.Serializable',
                    'java.lang.Cloneable'
                ],
                'correct_index': 1,
                'explanation': 'The try-with-resources statement requires resources to implement `java.lang.AutoCloseable` (or its child `java.io.Closeable`), which defines the `close()` method.'
            },
            {
                'id': 'java-c-3',
                'question': 'What does the PECS mnemonic stand for in Java Generics?',
                'options': [
                    'Private Encapsulated Class Structure',
                    'Producer Extends, Consumer Super',
                    'Package Enclosing Class Scope',
                    'Parameter Evaluation Call Stack'
                ],
                'correct_index': 1,
                'explanation': 'PECS: Use `? extends T` when the collection produces data (read-only), and `? super T` when the collection consumes data (write-only).'
            },
            {
                'id': 'java-c-4',
                'question': 'What occurs internally in a Java 8+ `HashMap` when a bucket\'s linked list collisions reach 8 items and total capacity is at least 64?',
                'options': [
                    'The HashMap throws an OutOfMemoryError',
                    'The bucket converts from a linked list into a balanced Red-Black Tree, improving lookup from O(n) to O(log n)',
                    'The entire map is emptied',
                    'The extra keys are discarded'
                ],
                'correct_index': 1,
                'explanation': 'To prevent hash collision DoS attacks, Java 8 treeifies hash buckets with $\\ge 8$ colliding elements into balanced red-black trees (`TreeNode`), improving worst-case search from $O(n)$ to $O(\\log n)$.'
            },
            {
                'id': 'java-c-5',
                'question': 'What is the signature of the abstract method in Java\'s `java.util.function.Predicate<T>` interface?',
                'options': [
                    'void accept(T t)',
                    'R apply(T t)',
                    'boolean test(T t)',
                    'T get()'
                ],
                'correct_index': 2,
                'explanation': '`Predicate<T>` has the single abstract method `boolean test(T t)` used for evaluating boolean filter conditions.'
            },
            {
                'id': 'java-c-6',
                'question': 'What happens if you attempt to perform a terminal operation on a Java Stream that has already been consumed?',
                'options': [
                    'The stream resets and replays from the beginning',
                    'It throws an IllegalStateException: stream has already been operated upon or closed',
                    'It returns an empty Optional',
                    'It blocks indefinitely'
                ],
                'correct_index': 1,
                'explanation': 'Java Streams are single-use pipelines. Once a terminal operation completes, the stream is closed and cannot be reused.'
            },
            {
                'id': 'java-c-7',
                'question': 'What method must be called to actually spawn and run a new OS thread in Java?',
                'options': [
                    'thread.run()',
                    'thread.start()',
                    'thread.execute()',
                    'thread.spawn()'
                ],
                'correct_index': 1,
                'explanation': 'Calling `thread.start()` allocates OS resources and invokes the `run()` method in a new thread. Calling `thread.run()` directly merely executes it synchronously in the calling thread.'
            },
            {
                'id': 'java-c-8',
                'question': 'Why is `AtomicInteger` thread-safe without requiring traditional synchronized blocks or locks?',
                'options': [
                    'It runs on a single background worker thread',
                    'It utilizes hardware-level Compare-And-Swap (CAS) atomic CPU instructions',
                    'It copies all data into a temporary database table',
                    'It pauses all other operating system processes'
                ],
                'correct_index': 1,
                'explanation': '`AtomicInteger` relies on non-blocking Compare-And-Swap (CAS) instructions supported directly by modern CPU architectures, avoiding lock contention overhead.'
            },
            {
                'id': 'java-c-9',
                'question': 'Which modern package introduced in Java 7 provides the `Path` and `Files` utility classes for robust file I/O?',
                'options': [
                    'java.io',
                    'java.nio.file',
                    'java.util.io',
                    'java.net.file'
                ],
                'correct_index': 1,
                'explanation': 'NIO.2 (`java.nio.file`) provides `Path`, `Paths`, and `Files` with modern features like streaming, non-blocking I/O, and platform-independent file attributes.'
            },
            {
                'id': 'java-c-10',
                'question': 'Why is the `volatile` modifier necessary for the instance variable in a Double-Checked Locking Singleton implementation?',
                'options': [
                    'To serialize the instance to disk',
                    'To prevent instruction reordering by the compiler and JVM memory model during object construction',
                    'To force garbage collection every 60 seconds',
                    'To allow multiple instances to be created'
                ],
                'correct_index': 1,
                'explanation': '`volatile` ensures that writes to the instance reference are immediately visible to all threads and prevents instruction reordering where another thread might see a partially initialized object reference.'
            }
        ]
    },
    'dbms': {
        'easy': [
            {
                'id': 'dbms-e-1',
                'question': 'Which level of the ANSI/SPARC 3-schema architecture describes how data is physically stored on disk blocks?',
                'options': [
                    'External / View Level',
                    'Conceptual / Logical Level',
                    'Internal / Physical Level',
                    'Application Tier'
                ],
                'correct_index': 2,
                'explanation': 'The Internal (Physical) Level describes the physical storage structure, file organizations, block layouts, and indexing mechanisms on disk.'
            },
            {
                'id': 'dbms-e-2',
                'question': 'In the relational model, what is the formal term for a row in a database table?',
                'options': [
                    'Relation',
                    'Tuple',
                    'Attribute',
                    'Domain'
                ],
                'correct_index': 1,
                'explanation': 'In formal relational algebra and Codd model: Table = Relation, Row = Tuple, Column = Attribute.'
            },
            {
                'id': 'dbms-e-3',
                'question': 'What is the "Degree" of a relation in database theory?',
                'options': [
                    'The number of rows (tuples) in the table',
                    'The number of columns (attributes) in the table',
                    'The number of foreign keys referencing the table',
                    'The temperature of the server CPU'
                ],
                'correct_index': 1,
                'explanation': 'The Degree of a relation is the number of attributes (columns), whereas Cardinality is the number of tuples (rows).'
            },
            {
                'id': 'dbms-e-4',
                'question': 'What is a Candidate Key in relational database design?',
                'options': [
                    'Any column containing numbers',
                    'A minimal super key containing no extraneous attributes capable of uniquely identifying a tuple',
                    'A foreign key that references an external API',
                    'A key that permits duplicate NULL values'
                ],
                'correct_index': 1,
                'explanation': 'A Candidate Key is a minimal super key: it uniquely identifies any row in the relation, and removing any attribute from it destroys this uniqueness property.'
            },
            {
                'id': 'dbms-e-5',
                'question': 'Can a Primary Key column contain `NULL` values?',
                'options': [
                    'Yes, if configured with ALLOW NULL',
                    'No, by relational definition a Primary Key must be unique and non-null (Entity Integrity)',
                    'Only in the first row of the table',
                    'Yes, up to a maximum of one NULL'
                ],
                'correct_index': 1,
                'explanation': 'Entity Integrity states that no primary key value can be NULL because it is used to uniquely identify individual tuples in a relation.'
            },
            {
                'id': 'dbms-e-6',
                'question': 'How is a Many-to-Many (M:N) relationship between two entities (e.g. Students and Courses) implemented in a relational database?',
                'options': [
                    'By adding an array column to the Students table',
                    'By creating an intermediate junction / associative table containing foreign keys referencing both entities',
                    'By duplicating the database on two separate physical drives',
                    'By converting all text to uppercase'
                ],
                'correct_index': 1,
                'explanation': 'A Many-to-Many relationship cannot be represented cleanly in a single relational table without violating 1NF. It is decomposed into two One-to-Many relationships via an intermediate junction table (e.g. `enrollments`).'
            },
            {
                'id': 'dbms-e-7',
                'question': 'What referential action automatically deletes child records when the referenced parent record is deleted?',
                'options': [
                    'ON DELETE RESTRICT',
                    'ON DELETE CASCADE',
                    'ON DELETE SET NULL',
                    'ON DELETE NO ACTION'
                ],
                'correct_index': 1,
                'explanation': '`ON DELETE CASCADE` instructs the database engine to automatically delete any child rows whose foreign key matches the deleted parent row.'
            },
            {
                'id': 'dbms-e-8',
                'question': 'Which relational algebra operator corresponds to selecting specific columns (vertical filtering) while discarding duplicates?',
                'options': [
                    'Select (σ)',
                    'Project (π)',
                    'Cartesian Product (×)',
                    'Join (⨝)'
                ],
                'correct_index': 1,
                'explanation': 'The Project operator ($\\pi$) projects specified columns from a relation, discarding unmentioned columns and eliminating duplicate tuples.'
            },
            {
                'id': 'dbms-e-9',
                'question': 'Which of the following is a SQL Data Definition Language (DDL) command?',
                'options': [
                    'SELECT',
                    'INSERT',
                    'ALTER TABLE',
                    'UPDATE'
                ],
                'correct_index': 2,
                'explanation': 'DDL commands manage schema structures (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`). `SELECT`, `INSERT`, `UPDATE`, and `DELETE` are DML commands.'
            },
            {
                'id': 'dbms-e-10',
                'question': 'What does the SQL `CHECK` constraint do?',
                'options': [
                    'Validates credit card payment transactions',
                    'Enforces a boolean predicate condition that all values in the column must satisfy before insertion or update',
                    'Checks if the database hard drive is fragmented',
                    'Encrypts the column with AES'
                ],
                'correct_index': 1,
                'explanation': 'The `CHECK (condition)` constraint ensures that all values in a column satisfy a boolean condition (e.g. `CHECK (credits BETWEEN 1 AND 6)`).'
            }
        ],
        'medium': [
            {
                'id': 'dbms-m-1',
                'question': 'What happens if you execute `UPDATE students SET gpa = 4.0;` without a `WHERE` clause?',
                'options': [
                    'Only the first row in the table is updated',
                    'Every single row in the students table will have its GPA updated to 4.0',
                    'The database throws a SyntaxError requiring WHERE',
                    'The update is automatically discarded'
                ],
                'correct_index': 1,
                'explanation': 'Omitting the `WHERE` clause in an `UPDATE` statement causes the modification to be applied unconditionally to every row in the target table.'
            },
            {
                'id': 'dbms-m-2',
                'question': 'What is the correct SQL syntax to test whether a column named `email` contains no value?',
                'options': [
                    'WHERE email = NULL',
                    'WHERE email IS NULL',
                    'WHERE email == NULL',
                    'WHERE email IS EMPTY'
                ],
                'correct_index': 1,
                'explanation': 'In SQL three-valued logic, comparison with NULL using `=` evaluates to UNKNOWN. To check for missing values, the `IS NULL` or `IS NOT NULL` predicate is mandatory.'
            },
            {
                'id': 'dbms-m-3',
                'question': 'How does the SQL `AVG(score)` function treat rows where `score` is `NULL`?',
                'options': [
                    'It treats NULL as 0 and includes it in the denominator',
                    'It completely ignores NULL rows from both numerator sum and denominator count',
                    'It returns NULL for the entire query',
                    'It raises a DivideByZero error'
                ],
                'correct_index': 1,
                'explanation': 'Standard SQL aggregate functions (except `COUNT(*)`) ignore NULL values entirely when calculating results.'
            },
            {
                'id': 'dbms-m-4',
                'question': 'What is the fundamental difference between the `WHERE` clause and the `HAVING` clause?',
                'options': [
                    'WHERE is for strings; HAVING is for numbers',
                    'WHERE filters individual rows before grouping; HAVING filters aggregated groups after GROUP BY',
                    'HAVING runs before WHERE',
                    'There is no difference; they are interchangeable synonyms'
                ],
                'correct_index': 1,
                'explanation': '`WHERE` filters rows before aggregation and cannot contain aggregate functions. `HAVING` filters groups after `GROUP BY` and evaluates aggregate conditions like `HAVING COUNT(*) > 5`.'
            },
            {
                'id': 'dbms-m-5',
                'question': 'Which join type returns all records from the left table, along with matching records from the right table (filling with NULL if no match exists)?',
                'options': [
                    'INNER JOIN',
                    'LEFT OUTER JOIN',
                    'RIGHT OUTER JOIN',
                    'CROSS JOIN'
                ],
                'correct_index': 1,
                'explanation': 'A `LEFT (OUTER) JOIN` guarantees that every row from the left table appears in the result, populated with `NULL` for right-table columns if no join match exists.'
            },
            {
                'id': 'dbms-m-6',
                'question': 'What is a Correlated Subquery in SQL?',
                'options': [
                    'A subquery that runs in a background thread',
                    'A subquery that references columns from the outer query and must be re-evaluated for each candidate row of the outer query',
                    'A subquery that returns a single constant number',
                    'A subquery placed in the FROM clause'
                ],
                'correct_index': 1,
                'explanation': 'A Correlated Subquery depends on values from the outer query relation, executing iteratively for each row evaluated by the outer statement.'
            },
            {
                'id': 'dbms-m-7',
                'question': 'What is the performance difference between `UNION` and `UNION ALL`?',
                'options': [
                    'UNION is faster because it saves disk space',
                    'UNION ALL is faster because it simply concatenates result sets without performing an expensive sort/hash to remove duplicates',
                    'UNION ALL can only combine two tables',
                    'UNION is deprecated in ANSI SQL'
                ],
                'correct_index': 1,
                'explanation': '`UNION` removes duplicate rows by executing an internal sort or hash table deduplication. `UNION ALL` preserves duplicates, executing significantly faster.'
            },
            {
                'id': 'dbms-m-8',
                'question': 'What is a standard relational View?',
                'options': [
                    'A physical copy of the database stored on an external SSD',
                    'A virtual table defined by a stored SQL query that executes dynamically when queried',
                    'A graphical chart generated by the database dashboard',
                    'A specialized index for text columns'
                ],
                'correct_index': 1,
                'explanation': 'A standard view contains no data on disk; it is a stored query definition that the database engine merges into the calling query at execution time.'
            },
            {
                'id': 'dbms-m-9',
                'question': 'Which Transaction Control Language (TCL) command allows partial rollback to an intermediate checkpoint within a transaction?',
                'options': [
                    'ROLLBACK TO SAVEPOINT',
                    'PARTIAL COMMIT',
                    'CHECKPOINT REVERT',
                    'RESTORE POINT'
                ],
                'correct_index': 0,
                'explanation': '`SAVEPOINT name` sets an intermediate marker, and `ROLLBACK TO SAVEPOINT name` reverts modifications made after that savepoint without aborting the entire transaction.'
            },
            {
                'id': 'dbms-m-10',
                'question': 'Which clause controls the sorting order of records returned by a `SELECT` statement?',
                'options': [
                    'GROUP BY',
                    'SORT BY',
                    'ORDER BY',
                    'ARRANGE BY'
                ],
                'correct_index': 2,
                'explanation': 'In SQL, `ORDER BY column_name [ASC|DESC]` dictates the sorting sequence of output rows.'
            }
        ],
        'complex': [
            {
                'id': 'dbms-c-1',
                'question': 'Which Armstrong Axiom states that if $X \\rightarrow Y$ and $Y \\rightarrow Z$, then $X \\rightarrow Z$?',
                'options': [
                    'Reflexivity',
                    'Augmentation',
                    'Transitivity',
                    'Decomposition'
                ],
                'correct_index': 2,
                'explanation': 'The Transitivity axiom of functional dependencies states that if $X$ determines $Y$ and $Y$ determines $Z$, then $X$ transitively determines $Z$.'
            },
            {
                'id': 'dbms-c-2',
                'question': 'What type of dependency is eliminated when a schema is normalized from First Normal Form (1NF) to Second Normal Form (2NF)?',
                'options': [
                    'Transitive Dependency',
                    'Partial Dependency (where a non-prime attribute depends on a proper subset of a composite candidate key)',
                    'Multivalued Dependency',
                    'Join Dependency'
                ],
                'correct_index': 1,
                'explanation': '2NF requires relations to be in 1NF with zero partial functional dependencies of non-prime attributes on composite candidate keys.'
            },
            {
                'id': 'dbms-c-3',
                'question': 'What is the defining condition for a relation to be in Boyce-Codd Normal Form (BCNF)?',
                'options': [
                    'All attributes must be integers',
                    'For every non-trivial functional dependency X -> Y, X must be a Super Key',
                    'The table must not have more than 10 columns',
                    'Every column must be a foreign key'
                ],
                'correct_index': 1,
                'explanation': 'A relation is in BCNF if and only if for every non-trivial dependency $X \\rightarrow Y$, the determinant $X$ is a super key.'
            },
            {
                'id': 'dbms-c-4',
                'question': 'Which ACID property guarantees that once a transaction commits, its modifications survive server crashes and power failures?',
                'options': [
                    'Atomicity',
                    'Consistency',
                    'Isolation',
                    'Durability'
                ],
                'correct_index': 3,
                'explanation': 'Durability ensures that the effects of committed transactions are permanently recorded in non-volatile storage via Write-Ahead Logs before confirmation.'
            },
            {
                'id': 'dbms-c-5',
                'question': 'What structural property of a Precedence (Serialization) Graph proves that a concurrent schedule is Conflict Serializable?',
                'options': [
                    'The graph must be fully connected',
                    'The graph must contain no directed cycles (it must be a Directed Acyclic Graph / DAG)',
                    'The graph must have an even number of vertices',
                    'The graph must be a binary tree'
                ],
                'correct_index': 1,
                'explanation': 'A concurrent schedule is conflict serializable if and only if its precedence graph contains no directed cycles, allowing a topological sort of transactions.'
            },
            {
                'id': 'dbms-c-6',
                'question': 'What rule does the Two-Phase Locking (2PL) protocol impose on transactions to guarantee serializability?',
                'options': [
                    'Transactions can only access 2 tables at a time',
                    'A transaction cannot acquire any new lock once it releases its first lock (Growing Phase followed by Shrinking Phase)',
                    'Transactions must commit within 2 seconds',
                    'All locks must be shared locks'
                ],
                'correct_index': 1,
                'explanation': '2PL requires two distinct phases: Growing Phase (locks acquired, none released) and Shrinking Phase (locks released, none acquired). Once a lock is released, no more can be obtained.'
            },
            {
                'id': 'dbms-c-7',
                'question': 'What is the distinguishing requirement of Strict 2PL compared to basic 2PL?',
                'options': [
                    'All Shared locks must be converted to Exclusive locks',
                    'All Exclusive (write) locks must be held until the transaction formally commits or aborts',
                    'Deadlocks are mathematically impossible in Strict 2PL',
                    'Only read operations are permitted'
                ],
                'correct_index': 1,
                'explanation': 'Strict 2PL requires all exclusive locks to be held until transaction termination (COMMIT or ABORT), preventing cascading rollbacks.'
            },
            {
                'id': 'dbms-c-8',
                'question': 'In the Wait-Die deadlock prevention protocol based on timestamps, what happens if an older transaction requests a lock held by a younger transaction?',
                'options': [
                    'The older transaction dies (aborts)',
                    'The older transaction is allowed to wait for the younger transaction',
                    'The younger transaction is killed immediately',
                    'Both transactions are aborted'
                ],
                'correct_index': 1,
                'explanation': 'In Wait-Die: Older waits for younger; younger requesting from older immediately dies (aborts).'
            },
            {
                'id': 'dbms-c-9',
                'question': 'Why are B+ Trees predominantly preferred over standard Binary Search Trees for database indexes on disk?',
                'options': [
                    'B+ Trees store data in text format',
                    'High fanout minimizes tree height, dramatically reducing the number of expensive disk page I/O reads required to locate records',
                    'B+ Trees use no RAM',
                    'Binary trees cannot store string keys'
                ],
                'correct_index': 1,
                'explanation': 'B+ Trees have hundreds of keys per node (high fanout), keeping tree depth small (typically 3-4 levels for millions of rows), minimizing disk head seeks.'
            },
            {
                'id': 'dbms-c-10',
                'question': 'What fundamental rule does Write-Ahead Logging (WAL) enforce in relational database storage engines?',
                'options': [
                    'Data must be written to disk before log records are generated',
                    'Log records describing a data page update must be flushed to non-volatile disk BEFORE the dirty data page itself can be written to disk',
                    'Logs are written only once per month',
                    'Logs are kept strictly in volatile RAM'
                ],
                'correct_index': 1,
                'explanation': 'Write-Ahead Logging dictates that undo/redo log records must precede dirty buffer pool page flushes to non-volatile disk to guarantee atomicity and durability in the event of an untimely crash.'
            }
        ]
    },
    'dsa': {
        'easy': [
            {
                'id': 'dsa-e-1',
                'question': 'What is the time complexity of accessing an element in an array by its index $i$?',
                'options': [
                    'O(1)',
                    'O(log n)',
                    'O(n)',
                    'O(n^2)'
                ],
                'correct_index': 0,
                'explanation': 'Because array elements reside contiguously in RAM, calculating memory address $\\text{Base} + (i \\times \\text{size})$ executes in $O(1)$ constant time.'
            },
            {
                'id': 'dsa-e-2',
                'question': 'What is the amortized time complexity of appending an element to the end of a dynamic array?',
                'options': [
                    'O(n)',
                    'O(log n)',
                    'O(1)',
                    'O(n log n)'
                ],
                'correct_index': 2,
                'explanation': 'Although resizing copies $n$ elements when capacity is exhausted, geometric doubling ($2\\times$) ensures that resizing happens infrequently, yielding an amortized cost of $O(1)$ per append.'
            },
            {
                'id': 'dsa-e-3',
                'question': 'What is the time complexity of checking whether a string of length $n$ is a palindrome using two opposing pointers?',
                'options': [
                    'O(n^2) time, O(n) space',
                    'O(n) time, O(1) auxiliary space',
                    'O(log n) time, O(1) space',
                    'O(n!) time, O(n) space'
                ],
                'correct_index': 1,
                'explanation': 'Opposing pointers start at opposite ends and advance toward the center, performing at most $n/2$ comparisons in $O(n)$ time and using $O(1)$ auxiliary space.'
            },
            {
                'id': 'dsa-e-4',
                'question': 'What is the time complexity to insert a new node at the head of a Singly Linked List?',
                'options': [
                    'O(1)',
                    'O(n)',
                    'O(log n)',
                    'O(n^2)'
                ],
                'correct_index': 0,
                'explanation': 'Inserting at the head requires creating a node, setting `node.next = head`, and updating `head = node`. This involves a fixed number of pointer assignments in $O(1)$ time.'
            },
            {
                'id': 'dsa-e-5',
                'question': 'Which abstract data structure operates on a Last-In, First-Out (LIFO) discipline?',
                'options': [
                    'Queue',
                    'Stack',
                    'Binary Heap',
                    'Linked List'
                ],
                'correct_index': 1,
                'explanation': 'A Stack operates strictly on LIFO (Last-In, First-Out), where push and pop occur at the top of the stack.'
            },
            {
                'id': 'dsa-e-6',
                'question': 'What mathematical operator enables index wrap-around in a circular queue buffer?',
                'options': [
                    'Exponentiation (**)',
                    'Modulo (%)',
                    'Floor division (//)',
                    'Bitwise AND (&)'
                ],
                'correct_index': 1,
                'explanation': 'The modulo operator `(index + 1) % capacity` wraps the pointer back to index 0 when it reaches the end of the fixed-size array.'
            },
            {
                'id': 'dsa-e-7',
                'question': 'What prerequisite must a collection satisfy before Binary Search can be applied?',
                'options': [
                    'All elements must be prime numbers',
                    'The collection must be sorted in ascending or descending order',
                    'The collection must be a linked list',
                    'The size must be an exact power of 2'
                ],
                'correct_index': 1,
                'explanation': 'Binary search eliminates half the remaining elements each step by comparing the target to the median element, which requires the elements to be sorted.'
            },
            {
                'id': 'dsa-e-8',
                'question': 'What is the worst-case time complexity of Binary Search on a sorted array of size $n$?',
                'options': [
                    'O(1)',
                    'O(log n)',
                    'O(n)',
                    'O(n log n)'
                ],
                'correct_index': 1,
                'explanation': 'Each comparison halves the search interval ($n, n/2, n/4, \\dots, 1$), requiring at most $\\lfloor \\log_2 n \\rfloor + 1$ comparisons in $O(\\log n)$ time.'
            },
            {
                'id': 'dsa-e-9',
                'question': 'What is the best-case time complexity of Insertion Sort when the input array is already sorted?',
                'options': [
                    'O(n)',
                    'O(n log n)',
                    'O(n^2)',
                    'O(1)'
                ],
                'correct_index': 0,
                'explanation': 'On an already-sorted array, Insertion Sort\'s inner while-loop condition fails on the very first comparison, requiring only $n-1$ comparisons in $O(n)$ linear time.'
            },
            {
                'id': 'dsa-e-10',
                'question': 'Which sorting algorithm repeatedly finds the minimum element from the unsorted sub-array and places it at the beginning?',
                'options': [
                    'Bubble Sort',
                    'Selection Sort',
                    'Merge Sort',
                    'Radix Sort'
                ],
                'correct_index': 1,
                'explanation': 'Selection Sort scans the unsorted portion of the array to select the minimum element and swaps it with the first unsorted position.'
            }
        ],
        'medium': [
            {
                'id': 'dsa-m-1',
                'question': 'What is the time complexity to delete a node from a Doubly Linked List when a direct pointer to that node is provided?',
                'options': [
                    'O(n)',
                    'O(1)',
                    'O(log n)',
                    'O(n^2)'
                ],
                'correct_index': 1,
                'explanation': 'Because each node in a DLL stores pointers to both its predecessor (`prev`) and successor (`next`), detaching the node (`node.prev.next = node.next`) takes $O(1)$ time without traversing from the head.'
            },
            {
                'id': 'dsa-m-2',
                'question': 'Which data structure is typically used to validate balanced brackets like `{[()]}` in code?',
                'options': [
                    'Queue',
                    'Stack',
                    'Binary Search Tree',
                    'Graph'
                ],
                'correct_index': 1,
                'explanation': 'Opening brackets are pushed onto a LIFO Stack; when a closing bracket is encountered, popping from the stack must match the opening symbol.'
            },
            {
                'id': 'dsa-m-3',
                'question': 'What is the average time complexity of key lookup in a hash table with a good hash function?',
                'options': [
                    'O(1)',
                    'O(log n)',
                    'O(n)',
                    'O(n log n)'
                ],
                'correct_index': 0,
                'explanation': 'Assuming a uniform hash distribution and reasonable load factor ($\\alpha < 0.75$), hash table key lookups execute in average $O(1)$ constant time.'
            },
            {
                'id': 'dsa-m-4',
                'question': 'According to the Master Theorem, what is the asymptotic complexity of $T(n) = 2T(n/2) + O(n)$?',
                'options': [
                    'O(n)',
                    'O(n log n)',
                    'O(n^2)',
                    'O(log n)'
                ],
                'correct_index': 1,
                'explanation': 'Here $a = 2, b = 2, f(n) = O(n^1)$. Since $\\log_b a = \\log_2 2 = 1 = c$, this matches Case 2 of the Master Theorem: $\\Theta(n^{\\log_b a} \\log n) = \\Theta(n \\log n)$ (Merge Sort recurrence).'
            },
            {
                'id': 'dsa-m-5',
                'question': 'What is the auxiliary space complexity of standard top-down array Merge Sort of $n$ elements?',
                'options': [
                    'O(1)',
                    'O(log n)',
                    'O(n)',
                    'O(n^2)'
                ],
                'correct_index': 2,
                'explanation': 'Merge Sort requires an auxiliary array of size $O(n)$ to merge elements safely without overwriting input elements.'
            },
            {
                'id': 'dsa-m-6',
                'question': 'What causes naive Quick Sort to degrade to its worst-case $O(n^2)$ time complexity?',
                'options': [
                    'Selecting random pivots',
                    'Consistently selecting the smallest or largest element as the pivot (e.g. on already-sorted input with first/last pivot selection)',
                    'Having too many duplicate elements',
                    'Sorting strings instead of numbers'
                ],
                'correct_index': 1,
                'explanation': 'When the pivot is consistently extreme, partition sizes are $0$ and $n-1$, creating a degenerate recursion tree of height $n$, yielding $\\sum_{i=1}^n i = O(n^2)$ work.'
            },
            {
                'id': 'dsa-m-7',
                'question': 'Which tree traversal of a Binary Search Tree (BST) produces node values in ascending sorted order?',
                'options': [
                    'Preorder Traversal',
                    'Inorder Traversal (Left, Root, Right)',
                    'Postorder Traversal',
                    'Level-order Traversal'
                ],
                'correct_index': 1,
                'explanation': 'In a BST, all left descendants are smaller than the node, and all right descendants are larger. Traversing Inorder (Left, Root, Right) processes keys in non-decreasing sorted order.'
            },
            {
                'id': 'dsa-m-8',
                'question': 'When deleting a node with two children from a BST, what node can replace it to preserve the BST invariant?',
                'options': [
                    'The root node',
                    'Its Inorder Successor (smallest node in its right subtree) or Inorder Predecessor',
                    'Any leaf node chosen at random',
                    'Its parent node'
                ],
                'correct_index': 1,
                'explanation': 'The Inorder Successor (minimum value in right subtree) is strictly greater than all left descendants and strictly less than all other right descendants, preserving the BST property.'
            },
            {
                'id': 'dsa-m-9',
                'question': 'What is the time complexity to build a binary heap of $n$ elements from an arbitrary array using Floyd\'s bottom-up `heapify` algorithm?',
                'options': [
                    'O(n log n)',
                    'O(n)',
                    'O(log n)',
                    'O(n^2)'
                ],
                'correct_index': 1,
                'explanation': 'Although inserting $n$ elements individually takes $O(n \\log n)$, Floyd\'s bottom-up `heapify` takes linear $O(n)$ time because the majority of nodes are near the bottom of the tree where sift-down height is small.'
            },
            {
                'id': 'dsa-m-10',
                'question': 'In a zero-indexed array representation of a binary heap, what is the index of the parent of the node at index $i$?',
                'options': [
                    '2 * i',
                    'floor((i - 1) / 2)',
                    '2 * i + 1',
                    'i / 2'
                ],
                'correct_index': 1,
                'explanation': 'For a zero-indexed binary heap array, the parent of index $i$ is located at $\\lfloor (i - 1) / 2 \\rfloor$, the left child at $2i + 1$, and right child at $2i + 2$.'
            }
        ],
        'complex': [
            {
                'id': 'dsa-c-1',
                'question': 'What are the permissible Balance Factor values for every node in an AVL balanced search tree?',
                'options': [
                    'Any integer between -5 and 5',
                    '{-1, 0, 1}',
                    '{0, 1, 2}',
                    'Strictly 0'
                ],
                'correct_index': 1,
                'explanation': 'An AVL tree enforces that for every node, the height difference between its left and right subtrees (Balance Factor) must be strictly $-1$, $0$, or $1$.'
            },
            {
                'id': 'dsa-c-2',
                'question': 'What is the space complexity of an Adjacency List representation of a graph with $V$ vertices and $E$ edges?',
                'options': [
                    'O(V^2)',
                    'O(V + E)',
                    'O(E^2)',
                    'O(V * E)'
                ],
                'correct_index': 1,
                'explanation': 'An Adjacency List stores $V$ vertex list headers and a total of $2E$ edge entries (for undirected graphs), consuming optimal $O(V + E)$ memory.'
            },
            {
                'id': 'dsa-c-3',
                'question': 'Which graph traversal algorithm guarantees finding the shortest path (minimum number of edges) in an unweighted graph?',
                'options': [
                    'Depth-First Search (DFS)',
                    'Breadth-First Search (BFS)',
                    'Inorder Tree Traversal',
                    'Kruskal\'s Algorithm'
                ],
                'correct_index': 1,
                'explanation': 'Because BFS visits nodes in order of their edge distance from the root (level by level), the first time a target vertex is reached, the path is guaranteed to be the shortest in an unweighted graph.'
            },
            {
                'id': 'dsa-c-4',
                'question': 'What is the time complexity of Dijkstra\'s Single-Source Shortest Path algorithm implemented with a binary min-heap priority queue?',
                'options': [
                    'O(V^2)',
                    'O((V + E) log V)',
                    'O(V * E)',
                    'O(V^3)'
                ],
                'correct_index': 1,
                'explanation': 'Each vertex is extracted from the min-heap once ($V \\log V$) and each edge relaxation updates the heap ($E \\log V$), yielding $O((V + E) \\log V)$.'
            },
            {
                'id': 'dsa-c-5',
                'question': 'Why does Dijkstra\'s algorithm fail on graphs containing negative edge weights?',
                'options': [
                    'Because min-heaps cannot store negative numbers',
                    'Dijkstra\'s greedy assumption assumes visiting a node via the shortest path permanently fixes its distance, which can be invalidated by later negative edges',
                    'It causes an infinite loop in all graphs',
                    'Negative weights cause integer overflow'
                ],
                'correct_index': 1,
                'explanation': 'Dijkstra\'s greedy choice property assumes adding an edge only increases path distance. Negative weights can decrease a previously finalized path cost, invalidating the greedy invariant. Bellman-Ford must be used instead.'
            },
            {
                'id': 'dsa-c-6',
                'question': 'Which data structure allows Kruskal\'s Minimum Spanning Tree algorithm to perform near O(1) cycle detection?',
                'options': [
                    'Binary Search Tree',
                    'Disjoint-Set Union (Union-Find) with path compression',
                    'Adjacency Matrix',
                    'Doubly Linked List'
                ],
                'correct_index': 1,
                'explanation': 'The Disjoint-Set Union (DSU / Union-Find) data structure with path compression and rank heuristics checks and merges connected components in $O(\\alpha(V))$ nearly constant time.'
            },
            {
                'id': 'dsa-c-7',
                'question': 'By what attribute must time intervals be sorted to solve the Activity Selection problem using a greedy algorithm?',
                'options': [
                    'Start time',
                    'Finish / End time',
                    'Duration (Finish - Start)',
                    'Alphabetical title'
                ],
                'correct_index': 1,
                'explanation': 'Sorting intervals by earliest finish time leaves the maximum possible remaining time for subsequent non-overlapping activities, guaranteeing a globally optimal count.'
            },
            {
                'id': 'dsa-c-8',
                'question': 'Can the 0/1 Knapsack problem (where items cannot be subdivided) be solved optimally using a greedy approach?',
                'options': [
                    'Yes, by sorting by value-to-weight ratio',
                    'No, 0/1 Knapsack lacks the greedy-choice property and requires Dynamic Programming',
                    'Yes, by picking the heaviest items first',
                    'Yes, in O(n log n) time'
                ],
                'correct_index': 1,
                'explanation': 'Greedy heuristics fail on 0/1 Knapsack because an item selected greedily can block multiple smaller items whose combined value is higher. Dynamic Programming ($O(n \\cdot W)$) is required.'
            },
            {
                'id': 'dsa-c-9',
                'question': 'What is the time complexity to compute the Longest Common Subsequence (LCS) of two strings of lengths $m$ and $n$ using Dynamic Programming?',
                'options': [
                    'O(m + n)',
                    'O(m * n)',
                    'O(2^(m+n))',
                    'O(log(m + n))'
                ],
                'correct_index': 1,
                'explanation': 'The bottom-up DP table of dimensions $(m + 1) \\times (n + 1)$ fills each cell in $O(1)$ time, yielding overall $O(m \\cdot n)$ time and space complexity.'
            },
            {
                'id': 'dsa-c-10',
                'question': 'How does Backtracking improve upon brute-force exhaustive search in problems like the N-Queens constraint puzzle?',
                'options': [
                    'It translates the problem into machine code',
                    'It prunes invalid branches of the state-space search tree as soon as a constraint is violated, abandoning hopeless paths early',
                    'It solves the puzzle using quantum annealing',
                    'It uses a neural network to guess queen placements'
                ],
                'correct_index': 1,
                'explanation': 'Backtracking evaluates constraints at each step: if placing a queen attacks another, the entire subtree below that choice is abandoned (pruned) immediately without checking remaining positions.'
            }
        ]
    }
}
