"""
Python Programming Curriculum for EduAdapt-AI
Contains full structured content for Easy, Medium, and Complex levels.
"""

PYTHON_DATA = {
    'id': 'python',
    'title': 'Python Programming',
    'badge_color': 'primary',
    'icon': 'bi-filetype-py',
    'short_summary': 'Master Python from fundamentals to advanced metaprogramming, OOP, and algorithms.',
    'description': 'A comprehensive learning track covering Python syntax, data structures, functional paradigms, object-oriented software engineering, generators, decorators, and production testing.',
    'difficulty': 'Beginner to Advanced',
    'levels': {
        'easy': {
            'level_number': 1,
            'name': 'Easy (Level 1 - Foundational)',
            'description': 'Core syntax, variables, primitive types, operators, conditional branching, loops, strings, and standard collections.',
            'topics': [
                {
                    'id': 'py-intro-syntax',
                    'title': '1. Introduction, Execution Model & Python Syntax',
                    'read_time': '8 min',
                    'summary': 'Understand how the CPython interpreter executes bytecode and write clean, PEP-8 compliant Python code.',
                    'concept': """Python is a high-level, interpreted, dynamically typed programming language created by Guido van Rossum. Unlike compiled languages such as C++ or Java that produce machine code before execution, Python source code (`.py`) is compiled into intermediate bytecode (`.pyc`), which is then executed line-by-line by the CPython Virtual Machine (PVM).

Python emphasizes readable, expressive code with significant whitespace (indentation) rather than curly braces `{}` or semicolons `;`. Comments are written using `#` for single-line notes and triple quotes `'''` or `\"\"\"` for multi-line docstrings.""",
                    'syntax': """# Single line comment
variable_name = value

# Statement indentation defines code blocks (4 spaces recommended)
if condition:
    indented_statement_1
    indented_statement_2
""",
                    'code_example': """# First Python Script
print("Welcome to EduAdapt-AI!")

student_name = "Alex"
course = "Python Fundamentals"

print(f"Student: {student_name}")
print(f"Enrolled Course: {course}")
print("CPython translates this file into bytecode and runs it on the PVM.")
""",
                    'expected_output': """Welcome to EduAdapt-AI!
Student: Alex
Enrolled Course: Python Fundamentals
CPython translates this file into bytecode and runs it on the PVM.
""",
                    'common_mistakes': 'Mixing tabs and spaces for indentation leads to `IndentationError: unindent does not match any outer indentation level`. Always use 4 consistent spaces.',
                    'practice_question': 'What component of Python is responsible for converting bytecode instructions into native OS instructions at runtime? (Answer: The Python Virtual Machine / PVM).'
                },
                {
                    'id': 'py-vars-types',
                    'title': '2. Variables, Dynamic Typing & Primitive Data Types',
                    'read_time': '10 min',
                    'summary': 'Explore Python dynamic typing, memory references, integers, floats, booleans, and type casting.',
                    'concept': """In Python, variables are not typed storage boxes; they are named references (pointers) to objects in memory. When you write `x = 42`, Python allocates an integer object `42` in heap memory and binds the name `x` to it.

Python provides core primitive types:
- `int`: Arbitrary-precision integers (e.g. `10`, `-500`, `10**50`).
- `float`: IEEE 754 double-precision floating-point numbers (e.g. `3.14159`).
- `bool`: Subclass of integer (`True` evaluating to 1, `False` evaluating to 0).
- `str`: Immutable sequences of Unicode code points.
- `NoneType`: Represented by the singleton `None`, indicating the absence of a value.

Type casting is achieved using constructor functions: `int()`, `float()`, `str()`, and `bool()`.""",
                    'syntax': """var_int = 100
var_float = 99.95
var_bool = True
var_str = "Adaptive Learning"
var_none = None

# Checking type and memory identity
type(var_int)
id(var_int)
""",
                    'code_example': """score_raw = "85"
# Convert string to integer for arithmetic
score = int(score_raw)
max_score = 100
percentage = (score / max_score) * 100
is_passing = percentage >= 70.0

print("Data Type of score:", type(score))
print(f"Calculated: {percentage:.1f}%")
print("Has student passed?", is_passing)
""",
                    'expected_output': """Data Type of score: <class 'int'>
Calculated: 85.0%
Has student passed? True
""",
                    'common_mistakes': 'Attempting string concatenation with numbers without casting: `"Score: " + 85` raises `TypeError: can only concatenate str (not "int") to str`. Use formatted string literals (`f"Score: {85}"`).',
                    'practice_question': 'What does `bool("")`, `bool(0)`, and `bool(None)` evaluate to in Python? (Answer: All evaluate to `False` as they represent falsy values).'
                },
                {
                    'id': 'py-io-formatting',
                    'title': '3. Input/Output and String Formatting',
                    'read_time': '9 min',
                    'summary': 'Master the `input()` function, type coercion, and Python 3.6+ f-string interpolation.',
                    'concept': """The standard input function `input(prompt)` pauses execution, displays the optional prompt to stdout, and reads a line from stdin as a string (`str`). If you expect numerical input, you must explicitly wrap it in `int()` or `float()`.

String formatting in Python has evolved through three iterations:
1. `%` formatting (legacy C-style printf)
2. `str.format()` method
3. Formatted string literals (f-strings, introduced in Python 3.6)

F-strings are prefixed with `f` or `F` and allow inline Python expressions, arithmetic, and format specifiers like precision, padding, and alignments inside curly braces `{}`.""",
                    'syntax': """# Input casting
age = int(input("Enter age: "))

# Modern f-string specifiers
f"{value:width.precisionf}"
f"{number:>10}"    # Right align in 10 spaces
f"{number:05d}"    # Zero-padded integer
""",
                    'code_example': """item_name = "Algorithmic Textbook"
unit_price = 49.9975
quantity = 3
total = unit_price * quantity

# Formatted currency string with 2 decimal places
report = f"Receipt: {quantity}x '{item_name}' @ ${unit_price:.2f} each = ${total:.2f}"
print(report)

# Width alignment demonstration
print(f"{'Subject':<15} | {'Score':>5}")
print("-" * 23)
print(f"{'Python':<15} | {92:>5}")
print(f"{'DBMS':<15} | {88:>5}")
""",
                    'expected_output': """Receipt: 3x 'Algorithmic Textbook' @ $50.00 each = $149.99
Subject         | Score
-----------------------
Python          |    92
DBMS            |    88
""",
                    'common_mistakes': 'Forgetting that `input()` always returns a string. Doing `val = input(); val + 5` causes a `TypeError`.',
                    'practice_question': 'How do you print a floating point number `val = 12.34567` rounded to 3 decimal places using an f-string? (Answer: `f"{val:.3f}"`).'
                },
                {
                    'id': 'py-operators',
                    'title': '4. Arithmetic, Comparison & Logical Operators',
                    'read_time': '8 min',
                    'summary': 'Understand operator precedence, integer vs float division, and short-circuit boolean logic.',
                    'concept': """Python operators perform operations on variables and literal values:
- **Arithmetic**: `+`, `-`, `*`, `/` (always produces float), `//` (floor/integer division), `%` (modulus), `**` (exponentiation).
- **Comparison**: `==` (value equality), `!=`, `<`, `>`, `<=`, `>=`.
- **Identity & Membership**: `is` (checks exact object identity in memory), `is not`, `in` (checks membership in a collection), `not in`.
- **Logical**: `and`, `or`, `not`.

Python uses short-circuit evaluation for logical operators:
- In `A and B`, if `A` is falsy, Python returns `A` immediately without evaluating `B`.
- In `A or B`, if `A` is truthy, Python returns `A` immediately without evaluating `B`.""",
                    'syntax': """floor_div = 17 // 3   # 5
true_div = 17 / 3     # 5.6666...
mod = 17 % 3          # 2
power = 2 ** 8        # 256

# Identity vs Equality
a = [1, 2]
b = [1, 2]
a == b   # True (same contents)
a is b   # False (different heap objects)
""",
                    'code_example': """hours_studied = 25
assignment_passed = True
attendance_rate = 0.85

# Complex conditional logic with short-circuiting
eligible_for_cert = (hours_studied >= 20 and assignment_passed) or (attendance_rate >= 0.95)

print(f"Eligible for Certificate: {eligible_for_cert}")

# Modulus check for parity
number = 48
is_even = (number % 2 == 0)
print(f"Is {number} even? {is_even}")
""",
                    'expected_output': """Eligible for Certificate: True
Is 48 even? True
""",
                    'common_mistakes': 'Confusing `==` with `is`. `==` tests whether two values are equal, while `is` tests whether two references point to the exact same object in memory (`id(a) == id(b)`).',
                    'practice_question': 'What is the result of `14 // 4` versus `14 / 4` in Python 3? (Answer: `3` and `3.5`).'
                },
                {
                    'id': 'py-conditionals',
                    'title': '5. Control Flow: Conditional Branching (if, elif, else)',
                    'read_time': '9 min',
                    'summary': 'Implement decision-making logic using if-elif-else ladders and ternary conditional expressions.',
                    'concept': """Conditional execution allows your software to choose different paths based on runtime boolean checks. The `if` statement evaluates a condition: if true, the block executes; if false, optional `elif` (else if) clauses are evaluated in sequential order until one succeeds. The `else` block serves as the default fallback.

Python also supports the single-line ternary conditional expression:
`value_if_true if condition else value_if_false`

Conditions in Python do not require parentheses around the test expression, keeping the syntax clean and readable.""",
                    'syntax': """if condition_1:
    execute_branch_1()
elif condition_2:
    execute_branch_2()
else:
    execute_fallback()

# Ternary expression
status = "Pass" if score >= 70 else "Retake"
""",
                    'code_example': """def evaluate_student(grade_pct):
    if grade_pct < 0 or grade_pct > 100:
        return "Invalid Grade"
    elif grade_pct >= 90:
        return "Distinction (Level 3 Ready)"
    elif grade_pct >= 70:
        return "Proficient (Level 2 Unlocked)"
    elif grade_pct >= 50:
        return "Needs Review (Study Material Recommended)"
    else:
        return "Fail (Mandatory Retake)"

test_scores = [95, 78, 62, 45]
for s in test_scores:
    print(f"Score {s}% -> {evaluate_student(s)}")
""",
                    'expected_output': """Score 95% -> Distinction (Level 3 Ready)
Score 78% -> Proficient (Level 2 Unlocked)
Score 62% -> Needs Review (Study Material Recommended)
Score 45% -> Fail (Mandatory Retake)
""",
                    'common_mistakes': 'Using single `=` instead of `==` inside conditional statements. Python will raise `SyntaxError: invalid syntax` because assignment is disallowed inside an `if` expression.',
                    'practice_question': 'How can you write `if x > 10: res = "High" else: res = "Low"` in one line? (Answer: `res = "High" if x > 10 else "Low"`).'
                },
                {
                    'id': 'py-loops',
                    'title': '6. Loops and Iteration (for, while, range, break, continue)',
                    'read_time': '10 min',
                    'summary': 'Iterate through data using for-in loops, while loops, range generator, and loop control statements.',
                    'concept': """Python provides two primary looping constructs:
1. `for` loop: Iterates over items of any iterable sequence (lists, tuples, strings, ranges, dictionaries).
2. `while` loop: Executes repeatedly as long as a boolean test condition evaluates to `True`.

Loop Control Statements:
- `break`: Terminates the innermost loop immediately.
- `continue`: Skips the remainder of the current iteration and advances to the next step.
- `else` on loops: Executes only if the loop completes normally without encountering a `break` statement!

The `range([start], stop[, step])` built-in generates an arithmetic sequence on demand without storing all values in memory.""",
                    'syntax': """for item in iterable:
    if condition:
        continue
    if exit_condition:
        break
else:
    # Runs only if no break was hit
    pass

while condition:
    # repeat statements
    pass
""",
                    'code_example': """# Finding a target score with for-else
scores = [65, 72, 88, 94, 58]
target = 94

print("Searching for honors score...")
for idx, s in enumerate(scores):
    if s == target:
        print(f"Target score {target} found at student index #{idx}!")
        break
else:
    print("Target score not found.")

# Accumulation using while loop
counter = 1
sum_cubes = 0
while counter <= 4:
    sum_cubes += counter ** 3
    counter += 1

print(f"Sum of first 4 cubes: {sum_cubes}")
""",
                    'expected_output': """Searching for honors score...
Target score 94 found at student index #3!
Sum of first 4 cubes: 100
""",
                    'common_mistakes': 'Creating accidental infinite while-loops by forgetting to update the loop termination variable inside the loop body.',
                    'practice_question': 'What will `for i in range(1, 10, 2):` yield? (Answer: `1, 3, 5, 7, 9`).'
                },
                {
                    'id': 'py-strings',
                    'title': '7. String Manipulation, Methods & Slicing',
                    'read_time': '10 min',
                    'summary': 'Master immutable string operations, indexing, extended slicing [start:stop:step], and built-in methods.',
                    'concept': """Strings in Python are immutable sequences of Unicode characters. Once created, individual characters cannot be modified in place (`s[0] = 'a'` raises a `TypeError`). Any manipulation returns a brand-new string object.

Indexing and Slicing:
- Positive indexing starts from `0` at the beginning; negative indexing starts from `-1` at the end.
- Slicing syntax: `sequence[start:stop:step]`. Omitted `start` defaults to `0`, `stop` defaults to `len`, and `step` defaults to `1`.
- Reversing a string is cleanly expressed as `sequence[::-1]`.

Common string methods: `.strip()`, `.lower()`, `.upper()`, `.split()`, `.join()`, `.replace()`, `.startswith()`, `.find()`.""",
                    'syntax': """text = "EduAdapt AI Learning"
char = text[0]          # 'E'
last = text[-1]         # 'g'
slice_sub = text[0:8]   # 'EduAdapt'
reversed_s = text[::-1]

words = text.split(" ")
joined = "-".join(words)
""",
                    'code_example': """raw_topic = "  data structures and algorithms: binary trees  \\n"
# Clean and normalize text
clean_topic = raw_topic.strip().title()
print(f"Normalized: '{clean_topic}'")

# Split and filter
components = clean_topic.split(":")
subject_area = components[0]
subtopic = components[1].strip()

print(f"Domain: {subject_area}")
print(f"Subtopic: {subtopic}")
print(f"Is DSA related? {clean_topic.startswith('Data Structures')}")
""",
                    'expected_output': """Normalized: 'Data Structures And Algorithms: Binary Trees'
Domain: Data Structures And Algorithms
Subtopic: Binary Trees
Is DSA related? True
""",
                    'common_mistakes': 'Expecting string methods like `s.strip()` or `s.upper()` to mutate `s` in place. You must assign the returned result: `s = s.strip()`.',
                    'practice_question': 'What is the slice syntax to extract every second character of a string from index 1 to 7? (Answer: `s[1:8:2]`).'
                },
                {
                    'id': 'py-lists-tuples',
                    'title': '8. Lists and Tuples (Ordered Collections)',
                    'read_time': '10 min',
                    'summary': 'Differentiate between mutable lists and immutable tuples, unpacking, and in-place list sorting.',
                    'concept': """Python provides two primary sequence types for ordered data:
1. `list`: Mutable sequence enclosed in square brackets `[]`. Elements can be inserted, appended, removed, or modified in place.
2. `tuple`: Immutable sequence enclosed in parentheses `()`. Once constructed, its elements and length cannot change. Tuples are faster, use less memory, and can serve as dictionary keys if all their elements are hashable.

Tuple unpacking allows multiple variables to be assigned simultaneously from a sequence: `x, y = (10, 20)`.

Common list methods:
- `.append(x)`: Adds item to end ($O(1)$ amortized).
- `.insert(i, x)`: Inserts item at index $i$ ($O(n)$).
- `.pop([i])`: Removes and returns item at index $i$ (defaults to last item, $O(1)$).
- `.sort()`: In-place Timsort ($O(n \\log n)$).
- `sorted(iterable)`: Returns a new sorted list without modifying the original.""",
                    'syntax': """# List operations
topics = ["Python", "Java"]
topics.append("DBMS")
topics[0] = "Python 3"

# Tuple operations
coords = (12.9716, 77.5946)
lat, lon = coords   # Unpacking
""",
                    'code_example': """modules = ["Loops", "Functions", "OOP", "Recursion"]
modules.append("Decorators")
modules.insert(1, "Conditionals")
print("Updated Curriculum:", modules)

# Sorting by length of name
modules.sort(key=len)
print("Sorted by title length:", modules)

# Tuple demonstration
student_record = ("STU-1029", "Sahasra", 94.5)
student_id, name, final_score = student_record
print(f"ID: {student_id} | Name: {name} | Score: {final_score}")
""",
                    'expected_output': """Updated Curriculum: ['Loops', 'Conditionals', 'Functions', 'OOP', 'Recursion', 'Decorators']
Sorted by title length: ['OOP', 'Loops', 'Recursion', 'Functions', 'Decorators', 'Conditionals']
ID: STU-1029 | Name: Sahasra | Score: 94.5
""",
                    'common_mistakes': 'Attempting to modify a tuple (`t[0] = 5`), which throws `TypeError: "tuple" object does not support item assignment`.',
                    'practice_question': 'How can you swap two variables `a` and `b` in Python without a temporary variable? (Answer: `a, b = b, a`).'
                },
                {
                    'id': 'py-dicts-sets',
                    'title': '9. Dictionaries and Sets (Hash-Based Collections)',
                    'read_time': '11 min',
                    'summary': 'Explore key-value mapping with hash tables, O(1) lookups, set union/intersection, and uniqueness constraints.',
                    'concept': """Dictionaries (`dict`) and Sets (`set`) are hash-table backed data structures offering average $O(1)$ time complexity for insertions, deletions, and membership tests.

- **Dictionary**: Stores key-value mappings `{key: value}`. Keys must be hashable and unique. Since Python 3.7+, standard dictionaries preserve insertion order.
- **Set**: An unordered collection of unique, hashable items `{item1, item2}`. Duplicate elements are automatically discarded. Supports mathematical set operations like union (`|`), intersection (`&`), difference (`-`), and symmetric difference (`^`).

Dictionary retrieval using `.get(key, default)` safely returns a fallback value if the key does not exist, avoiding a `KeyError`.""",
                    'syntax': """# Dictionary
student = {"id": 101, "name": "Elena", "score": 92}
name = student.get("name")
bonus = student.get("bonus", 0)  # Safe default

# Set
registered_ids = {101, 102, 103, 101}  # Duplicate 101 is dropped
completed_ids = {101, 103, 105}
both = registered_ids & completed_ids    # Intersection
""",
                    'code_example': """# Gradebook mapping
gradebook = {
    "Python": 95,
    "Java": 84,
    "DBMS": 89
}

gradebook["DSA"] = 91

print("Subject Performance:")
for subject, marks in gradebook.items():
    print(f" - {subject}: {marks}/100")

# Set operations for prerequisites
passed_courses = {"Python", "Math", "Algorithms"}
degree_requirements = {"Python", "Java", "DBMS", "Algorithms", "Operating Systems"}

remaining = degree_requirements - passed_courses
print("Courses still required:", sorted(list(remaining)))
""",
                    'expected_output': """Subject Performance:
 - Python: 95/100
 - Java: 84/100
 - DBMS: 89/100
 - DSA: 91/100
Courses still required: ['DBMS', 'Java', 'Operating Systems']
""",
                    'common_mistakes': 'Using a mutable type like a `list` as a dictionary key or set item. This triggers `TypeError: unhashable type: "list"`. Use a `tuple` instead.',
                    'practice_question': 'How do you check whether a key `"email"` exists in `user_dict` without raising an exception? (Answer: `"email" in user_dict` or `user_dict.get("email") is not None`).'
                }
            ]
        },
        'medium': {
            'level_number': 2,
            'name': 'Medium (Level 2 - Practical & Problem Solving)',
            'description': 'Functions, scoping, recursion, comprehensions, file I/O, modular architecture, exceptions, and object-oriented programming.',
            'topics': [
                {
                    'id': 'py-functions-scope',
                    'title': '1. Functions, Scope & the LEGB Rule',
                    'read_time': '10 min',
                    'summary': 'Define modular functions, default parameters, keyword arguments, and understand Python scope resolution.',
                    'concept': """Functions are reusable blocks of logic defined with the `def` keyword. In Python, functions are first-class citizens, meaning they can be assigned to variables, passed as arguments, and returned from other functions.

Parameter passing in Python is "Call by Object Reference" (or Call by Sharing). If an argument is mutable (like a list), changes made inside the function affect the caller's object unless a copy is made.

Variable scope is resolved following the **LEGB Rule**:
1. **L**ocal: Inside the current function.
2. **E**nclosing: In any enclosing nested function scopes (`nonlocal`).
3. **G**lobal: At the top level of the module (`global`).
4. **B**uilt-in: Python built-in namespace (`len`, `range`, `int`, etc.).""",
                    'syntax': """def calculate_grade(score, max_possible=100, curve=0):
    adjusted = score + curve
    return (adjusted / max_possible) * 100

# Positional and keyword invocation
pct = calculate_grade(75, curve=5)
""",
                    'code_example': """def create_accumulator():
    total = 0
    def add(value):
        nonlocal total  # Modifies enclosing scope variable
        total += value
        return total
    return add

acc = create_accumulator()
print("Accumulator 1:", acc(10))
print("Accumulator 2:", acc(25))
print("Accumulator 3:", acc(15))
""",
                    'expected_output': """Accumulator 1: 10
Accumulator 2: 35
Accumulator 3: 50
""",
                    'common_mistakes': 'Using mutable default arguments such as `def append_to(item, target_list=[])`. The list is created once at function definition time and shared across subsequent calls! Use `target_list=None` instead.',
                    'practice_question': 'What keyword is used inside a nested function to modify a variable in the enclosing non-global scope? (Answer: `nonlocal`).'
                },
                {
                    'id': 'py-recursion',
                    'title': '2. Recursion & Recursive Problem Solving',
                    'read_time': '11 min',
                    'summary': 'Master recursive definitions, call stack anatomy, base conditions, and memoization techniques.',
                    'concept': """Recursion is a technique where a function solves a problem by calling itself with smaller instances of the same problem. Every recursive implementation requires:
1. **Base Case**: One or more stopping conditions that return a concrete value without making further recursive calls.
2. **Recursive Step**: Progress towards the base case by breaking down input data.

Each recursive call creates a new stack frame on the call stack. If the recursion depth exceeds Python default limit (usually 1000), Python raises `RecursionError: maximum recursion depth exceeded`. For overlapping subproblems, memoization or dynamic programming reduces exponential time to linear time.""",
                    'syntax': """def recursive_func(n):
    # 1. Base case
    if n <= 1:
        return n
    # 2. Recursive step
    return recursive_func(n - 1) + recursive_func(n - 2)
""",
                    'code_example': """# Factorial and Binary Search recursion
def factorial(n):
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers.")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)

def recursive_binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return recursive_binary_search(arr, target, low, mid - 1)
    else:
        return recursive_binary_search(arr, target, mid + 1, high)

data = [12, 24, 37, 49, 58, 67, 85, 99]
print("5! =", factorial(5))
idx = recursive_binary_search(data, 58, 0, len(data) - 1)
print("Index of 58 in array:", idx)
""",
                    'expected_output': """5! = 120
Index of 58 in array: 4
""",
                    'common_mistakes': 'Omitting the base case, causing infinite recursion leading to `RecursionError: maximum recursion depth exceeded in comparison`.',
                    'practice_question': 'What is the time complexity of a naive recursive Fibonacci calculation without memoization? (Answer: $O(2^n)$).'
                },
                {
                    'id': 'py-comprehensions',
                    'title': '3. List, Dict & Set Comprehensions',
                    'read_time': '9 min',
                    'summary': 'Write concise, idiomatic Python transformations using single-line comprehensions.',
                    'concept': """Comprehensions provide a concise syntax for constructing new sequences from existing iterables. They are not only more readable than explicit for-loops with accumulator lists, but they are also faster because the loop executes in C at the CPython bytecode level.

Forms:
- **List Comprehension**: `[expr for item in iterable if condition]`
- **Set Comprehension**: `{expr for item in iterable if condition}`
- **Dict Comprehension**: `{key_expr: val_expr for item in iterable if condition}`
- **Generator Expression**: `(expr for item in iterable if condition)` (evaluates lazily).""",
                    'syntax': """# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
score_map = {name: score for name, score in student_data if score >= 70}
""",
                    'code_example': """raw_scores = [("Alice", 88), ("Bob", 64), ("Charlie", 92), ("Diana", 79), ("Ethan", 58)]

# Pass list (>= 70)
passing_names = [name for name, score in raw_scores if score >= 70]
print("Passing Students:", passing_names)

# Dictionary of letter grades
grade_scale = {
    name: "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
    for name, score in raw_scores
}
print("Grade Scale Mapping:", grade_scale)
""",
                    'expected_output': """Passing Students: ['Alice', 'Charlie', 'Diana']
Grade Scale Mapping: {'Alice': 'B', 'Bob': 'F', 'Charlie': 'A', 'Diana': 'C', 'Ethan': 'F'}
""",
                    'common_mistakes': 'Over-complicating nested comprehensions to the point where code readability degrades. If a comprehension requires multiple nested loops and conditions, write a regular loop.',
                    'practice_question': 'How do you create a set of all unique word lengths from a list of words `["cat", "apple", "dog", "banana"]`? (Answer: `{len(w) for w in words}`).'
                },
                {
                    'id': 'py-file-io',
                    'title': '4. File Handling & the Context Manager (with Statement)',
                    'read_time': '10 min',
                    'summary': 'Safely open, read, write, and append to files using the with statement and standard file modes.',
                    'concept': """File operations interact with the underlying OS file descriptors. Always access files using the `with` statement (a context manager). The context manager guarantees that the file descriptor is closed automatically when leaving the block, even if an unhandled exception or return statement occurs.

Standard Modes:
- `'r'`: Read (default). Raises `FileNotFoundError` if the file does not exist.
- `'w'`: Write. Creates the file or truncates (overwrites) existing contents.
- `'a'`: Append. Writes new data at the end of the file.
- `'r+'`: Read and write.
- `'b'`: Binary mode (e.g., `'rb'`, `'wb'`) for images or raw bytes.""",
                    'syntax': """with open("filename.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\\n")

with open("filename.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
""",
                    'code_example': """import io

# Simulating file I/O using StringIO memory stream
virtual_file = io.StringIO()

# Writing data
virtual_file.write("Python,95\\n")
virtual_file.write("Java,88\\n")
virtual_file.write("DBMS,92\\n")

# Reading back line by line
virtual_file.seek(0)  # Rewind pointer to beginning
subject_records = []
for line in virtual_file:
    subj, mark = line.strip().split(",")
    subject_records.append((subj, int(mark)))

print("Parsed File Records:", subject_records)
avg_score = sum(mark for _, mark in subject_records) / len(subject_records)
print(f"Curriculum Average: {avg_score:.2f}")
""",
                    'expected_output': """Parsed File Records: [('Python', 95), ('Java', 88), ('DBMS', 92)]
Curriculum Average: 91.67
""",
                    'common_mistakes': 'Opening files with bare `f = open(...)` without a `finally: f.close()` or `with` block. If an error occurs, the file descriptor remains open, causing memory and handle leaks.',
                    'practice_question': 'Which file mode opens a file for appending without truncating existing data? (Answer: `"a"` or `"a+"`).'
                },
                {
                    'id': 'py-modules-packages',
                    'title': '5. Modules, Packages & the Python Standard Library',
                    'read_time': '9 min',
                    'summary': 'Organize code into reusable modules, `__init__.py` packages, and explore sys, os, and math modules.',
                    'concept': """A module is simply a Python file (`.py`) containing definitions, functions, and runnable code. A package is a directory containing multiple modules and an optional `__init__.py` file (which marks the directory as an importable Python package and can execute initialization code).

The special variable `__name__` is set to `"__main__"` when the script is run directly from the command line, but is set to the module name when imported. This allows a file to act as both an importable library and a standalone executable script.""",
                    'syntax': """import math
from datetime import datetime, timezone
import os.path

if __name__ == "__main__":
    # Code runs only when executed directly
    pass
""",
                    'code_example': """import math
import json

# Utility calculation
radius = 4.5
area = math.pi * (radius ** 2)
print(f"Circle Area with r={radius}: {area:.2f}")

# Serializing structured data
report_dict = {
    "module": "EduAdapt Analytics",
    "version": "2.0.0",
    "active_students": 1420,
    "pass_rate": 0.895
}
json_payload = json.dumps(report_dict, indent=2)
print("Standard Library JSON output:\\n" + json_payload)
""",
                    'expected_output': """Circle Area with r=4.5: 63.62
Standard Library JSON output:
{
  "module": "EduAdapt Analytics",
  "version": "2.0.0",
  "active_students": 1420,
  "pass_rate": 0.895
}
""",
                    'common_mistakes': 'Using wildcard imports `from module import *`. This pollutes the current namespace, masks variable names, and obscures which library functions originate from.',
                    'practice_question': 'What does `if __name__ == "__main__":` do in a Python script? (Answer: It prevents code inside that block from running when the script is imported as a module by another file).'
                },
                {
                    'id': 'py-exceptions',
                    'title': '6. Exception Handling (try, except, else, finally, raise)',
                    'read_time': '10 min',
                    'summary': 'Build resilient programs using structured exception handling, custom exception classes, and cleanup blocks.',
                    'concept': """Exceptions are runtime error events that disrupt normal program execution. Python handles errors using `try`, `except`, `else`, and `finally` blocks:
- `try`: Code that might raise an exception.
- `except ExceptionType as err`: Catches and handles specific exceptions.
- `else`: Executes only if NO exceptions were raised in the `try` block.
- `finally`: Guaranteed to execute regardless of whether an exception occurred or was handled (ideal for resource cleanup).

Custom exceptions can be created by subclassing `Exception`.""",
                    'syntax': """try:
    risky_operation()
except SpecificError as e:
    handle_error(e)
else:
    celebrate_success()
finally:
    cleanup_resources()
""",
                    'code_example': """class LevelLockedError(Exception):
    \"\"\"Raised when a student attempts to access a locked curriculum level.\"\"\"
    def __init__(self, level, required_score):
        super().__init__(f"Level '{level}' is locked! Requires passing prior assignment with >={required_score}%.")
        self.level = level

def access_complex_module(student_score):
    if student_score < 70:
        raise LevelLockedError("Complex", 70)
    return "Access Granted to Complex Curriculum!"

for score in [55, 82]:
    try:
        status = access_complex_module(score)
        print(f"Score {score}%: {status}")
    except LevelLockedError as exc:
        print(f"Score {score}% Caught Error: {exc}")
    finally:
        print("Verification audit complete.")
""",
                    'expected_output': """Score 55% Caught Error: Level 'Complex' is locked! Requires passing prior assignment with >=70%.
Verification audit complete.
Score 82%: Access Granted to Complex Curriculum!
Verification audit complete.
""",
                    'common_mistakes': 'Using a bare `except:` without specifying the exception type. This catches `KeyboardInterrupt` and `SystemExit`, making it impossible to stop the script gracefully with Ctrl+C.',
                    'practice_question': 'When does the `else` block of a `try-except-else-finally` construct execute? (Answer: Only when the `try` block completes successfully without raising any exceptions).'
                },
                {
                    'id': 'py-oop-classes',
                    'title': '7. OOP Fundamentals: Classes, Objects & Methods',
                    'read_time': '11 min',
                    'summary': 'Construct custom objects with attributes, the __init__ initializer, self reference, and instance methods.',
                    'concept': """Object-Oriented Programming (OOP) is a paradigm that bundles data (attributes) and operations (methods) into reusable blueprints called **Classes**.

Key Components:
- `class`: Keyword defining a class blueprint.
- `__init__(self, ...)`: The instance initializer method called automatically when creating a new object.
- `self`: An explicit reference to the current instance of the class. It allows methods to access and update instance variables.
- Class Attributes vs Instance Attributes: Class attributes are shared across all instances, whereas instance attributes belong exclusively to each individual object.""",
                    'syntax': """class Student:
    school_name = "EduAdapt Academy"  # Class attribute
    
    def __init__(self, name, student_id):
        self.name = name              # Instance attribute
        self.student_id = student_id
    
    def get_info(self):
        return f"{self.name} ({self.student_id})"
""",
                    'code_example': """class CourseProgress:
    passing_threshold = 70.0  # Shared class constant

    def __init__(self, course_name, student_name):
        self.course_name = course_name
        self.student_name = student_name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def average_score(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    def is_eligible_next_level(self):
        return self.average_score() >= self.passing_threshold

# Instantiate and use object
p = CourseProgress("Python Fundamentals", "Kiran")
p.add_score(80)
p.add_score(92)
print(f"Student: {p.student_name} | Subject: {p.course_name}")
print(f"Average: {p.average_score():.1f}%")
print("Unlocked next tier?", p.is_eligible_next_level())
""",
                    'expected_output': """Student: Kiran | Subject: Python Fundamentals
Average: 86.0%
Unlocked next tier? True
""",
                    'common_mistakes': 'Forgetting the `self` parameter in method definitions (`def func():` instead of `def func(self):`). Python automatically passes the instance as the first argument, causing a `TypeError`.',
                    'practice_question': 'What is the purpose of `self` in Python class methods? (Answer: It references the specific instance of the class that invoked the method).'
                },
                {
                    'id': 'py-oop-inheritance',
                    'title': '8. OOP: Inheritance & Method Overriding',
                    'read_time': '11 min',
                    'summary': 'Reuse code and establish hierarchical relationships using single/multiple inheritance and super().',
                    'concept': """Inheritance enables a derived child class to inherit attributes and methods from a parent base class, promoting DRY (Don't Repeat Yourself) architecture.

Method Overriding occurs when a child class provides its own implementation of a method already defined in the parent class. The `super()` function delegates calls to the parent class implementation, ensuring cooperative multiple inheritance and DRY initializers.""",
                    'syntax': """class Parent:
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def greet(self):
        parent_msg = super().greet()
        return f"{parent_msg} and Child"
""",
                    'code_example': """class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_role_description(self):
        return "Generic Platform User"

class Student(User):
    def __init__(self, name, email, student_id):
        super().__init__(name, email)
        self.student_id = student_id
        self.enrolled_courses = []

    def enroll(self, course_title):
        self.enrolled_courses.append(course_title)

    def get_role_description(self):
        # Method override
        return f"Student [ID: {self.student_id}] with {len(self.enrolled_courses)} courses."

u = Student("Sahasra", "sahasra@example.com", "ADAPT-882")
u.enroll("Python")
u.enroll("DBMS")
print(f"Name: {u.name} | Email: {u.email}")
print("Role info:", u.get_role_description())
""",
                    'expected_output': """Name: Sahasra | Email: sahasra@example.com
Role info: Student [ID: ADAPT-882] with 2 courses.
""",
                    'common_mistakes': 'Failing to call `super().__init__(...)` in child class `__init__`, leaving base class attributes uninitialized.',
                    'practice_question': 'How does Python determine the order in which base classes are searched when resolving methods? (Answer: Using the Method Resolution Order / MRO via the C3 Linearization algorithm).'
                },
                {
                    'id': 'py-polymorphism',
                    'title': '9. Polymorphism & Duck Typing',
                    'read_time': '10 min',
                    'summary': 'Leverage dynamic polymorphism and "If it walks like a duck and quacks like a duck, it is a duck".',
                    'concept': """Polymorphism means "many forms". In Python, polymorphism is fundamentally driven by **Duck Typing**: Python does not check the formal class type of an object; rather, it checks whether the object possesses the required methods or behaviors at runtime.

This makes code flexible and extensible: any class that implements the expected interface (e.g. `render()`, `calculate_score()`, or `__len__()`) can be used interchangeably without explicit interface declarations.""",
                    'syntax': """def process_assessment(evaluator):
    # Evaluator can be any class having calculate_score()
    return evaluator.calculate_score()
""",
                    'code_example': """class QuizAssessment:
    def __init__(self, questions_correct, total):
        self.correct = questions_correct
        self.total = total

    def calculate_score(self):
        return (self.correct / self.total) * 100

class ProjectAssessment:
    def __init__(self, rubrics_score, bonus):
        self.rubrics = rubrics_score
        self.bonus = bonus

    def calculate_score(self):
        return min(100.0, self.rubrics + self.bonus)

# Polymorphic processing
assessments = [
    QuizAssessment(8, 10),
    ProjectAssessment(92.0, 5.0)
]

for a in assessments:
    print(f"Evaluated Grade: {a.calculate_score():.1f}%")
""",
                    'expected_output': """Evaluated Grade: 80.0%
Evaluated Grade: 97.0%
""",
                    'common_mistakes': 'Writing rigid `isinstance(obj, SpecificClass)` checks everywhere, destroying duck typing and flexibility.',
                    'practice_question': 'What Python philosophy is encapsulated by "Duck Typing"? (Answer: Behavior and interface matter rather than explicit class inheritance).'
                }
            ]
        },
        'complex': {
            'level_number': 3,
            'name': 'Complex (Level 3 - Advanced Architecture & Optimization)',
            'description': 'Encapsulation, abstract base classes, generators, decorators, context managers, profiling, unit testing, and production engineering.',
            'topics': [
                {
                    'id': 'py-encapsulation-props',
                    'title': '1. Encapsulation, Name Mangling & @property Decorators',
                    'read_time': '12 min',
                    'summary': 'Implement private member conventions, name mangling with double underscores, and pythonic getters/setters with @property.',
                    'concept': """Encapsulation hides the internal state of an object and enforces invariants through controlled access.
- Single underscore `_attr`: Internal convention indicating protected member (by agreement, not enforced by interpreter).
- Double underscore `__attr`: Triggers **Name Mangling**, rewriting `__attr` to `_ClassName__attr` to prevent accidental overriding in subclasses.
- `@property`: Turns a method into a read-only attribute getter. Paired with `@setter`, it allows validation logic without changing external attribute access syntax.""",
                    'syntax': """class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = value
""",
                    'code_example': """class StudentProfile:
    def __init__(self, name, initial_score):
        self.name = name
        self._score = 0.0
        self.score = initial_score  # Uses setter validation

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        if not (0.0 <= val <= 100.0):
            raise ValueError(f"Score {val} out of bounds (0-100 required).")
        self._score = float(val)

    @property
    def is_honor_roll(self):
        return self._score >= 90.0

stu = StudentProfile("Marcus", 88.5)
print(f"Student: {stu.name} | Score: {stu.score}% | Honors: {stu.is_honor_roll}")
stu.score = 94.0
print(f"Updated Score: {stu.score}% | Honors: {stu.is_honor_roll}")
""",
                    'expected_output': """Student: Marcus | Score: 88.5% | Honors: False
Updated Score: 94.0% | Honors: True
""",
                    'common_mistakes': 'Writing Java-style `get_score()` and `set_score()` methods in Python instead of using the pythonic `@property` decorator.',
                    'practice_question': 'What does Python do to an attribute named `__secret` inside a class named `Vault`? (Answer: It mangles it to `_Vault__secret`).'
                },
                {
                    'id': 'py-abc-interfaces',
                    'title': '2. Abstract Base Classes (ABCs) & Protocol Enforcements',
                    'read_time': '11 min',
                    'summary': 'Define formal contracts and interface specifications using the abc module and @abstractmethod.',
                    'concept': """While duck typing is Python standard, large enterprise systems benefit from formal interface contracts. The `abc` (Abstract Base Classes) module provides the `ABC` base class and `@abstractmethod` decorator.

When a class inherits from `ABC` and contains at least one `@abstractmethod`, Python prevents instantiation of the class if any abstract methods remain unimplemented in the subclass, raising a `TypeError` at instantiation time.""",
                    'syntax': """from abc import ABC, abstractmethod

class BaseTutorEngine(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass
""",
                    'code_example': """from abc import ABC, abstractmethod

class EducationalDataSource(ABC):
    @abstractmethod
    def fetch_questions(self, subject: str, level: str) -> list:
        \"\"\"Retrieve quiz questions for given subject & level.\"\"\"
        pass

class DatabaseDataSource(EducationalDataSource):
    def fetch_questions(self, subject: str, level: str) -> list:
        return [f"Sample question for {subject} [{level}]"]

db_source = DatabaseDataSource()
print("Questions retrieved:", db_source.fetch_questions("Python", "Complex"))
""",
                    'expected_output': """Questions retrieved: ['Sample question for Python [Complex]']
""",
                    'common_mistakes': 'Attempting to instantiate an abstract class directly: `b = BaseTutorEngine()` throws `TypeError: Can\'t instantiate abstract class with abstract methods`.',
                    'practice_question': 'What module from Python standard library is used to define formal abstract base classes? (Answer: `abc`).'
                },
                {
                    'id': 'py-generators',
                    'title': '3. Iterators, Iterables & Generators (yield)',
                    'read_time': '12 min',
                    'summary': 'Save gigabytes of memory with lazy evaluation, the iterator protocol (__iter__, __next__), and generator functions.',
                    'concept': """An **Iterable** is any object capable of returning its members one at a time (implements `__iter__()`). An **Iterator** is the object that actually produces values sequentially via `__next__()`, raising `StopIteration` when depleted.

A **Generator** is a function that contains the `yield` statement. When called, it does not execute immediately; instead, it returns a generator object. Each call to `next()` executes code until it encounters `yield`, suspends execution, preserves its state and local variables, and yields the value to the caller. This provides $O(1)$ memory consumption for huge sequences.""",
                    'syntax': """def count_up_to(max_val):
    count = 1
    while count <= max_val:
        yield count
        count += 1

gen = count_up_to(1000000)  # Uses negligible memory!
""",
                    'code_example': """def fibonacci_stream():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Generate first 8 Fibonacci numbers lazily
fib = fibonacci_stream()
first_eight = [next(fib) for _ in range(8)]
print("Lazy Fibonacci Stream:", first_eight)

# Generator expression memory efficiency
squares_gen = (x ** 2 for x in range(5))
print("Next square:", next(squares_gen))
print("Next square:", next(squares_gen))
""",
                    'expected_output': """Lazy Fibonacci Stream: [0, 1, 1, 2, 3, 5, 8, 13]
Next square: 0
Next square: 1
""",
                    'common_mistakes': 'Attempting to index a generator object (`gen[0]`), which raises `TypeError: "generator" object is not subscriptable`. Generators produce values dynamically and must be consumed via `next()` or a loop.',
                    'practice_question': 'What exception is raised by an iterator when there are no further items to yield? (Answer: `StopIteration`).'
                },
                {
                    'id': 'py-decorators',
                    'title': '4. Function Decorators & Metaprogramming',
                    'read_time': '13 min',
                    'summary': 'Master higher-order functions, closures, functools.wraps, and writing parameterized decorators.',
                    'concept': """A decorator is a callable that accepts a function as an argument and returns a replacement wrapped function. Decorators allow cross-cutting concerns (logging, authentication, timing, caching, rate-limiting) to be cleanly applied to existing code without modification.

Using `@functools.wraps(fn)` inside the decorator preserves the original function name, docstring, and signature metadata.""",
                    'syntax': """import functools

def my_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Pre-execution logic
        result = fn(*args, **kwargs)
        # Post-execution logic
        return result
    return wrapper

@my_decorator
def core_task():
    pass
""",
                    'code_example': """import time
import functools

def benchmark(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[Audit] Function '{fn.__name__}' executed in {elapsed * 1000:.4f} ms")
        return res
    return wrapper

@benchmark
def compute_prime_sum(limit):
    return sum(x for x in range(limit) if x > 1 and all(x % d != 0 for d in range(2, int(x**0.5) + 1)))

total = compute_prime_sum(5000)
print("Sum of primes below 5000:", total)
""",
                    'expected_output': """[Audit] Function 'compute_prime_sum' executed in 4.5120 ms
Sum of primes below 5000: 1548136
""",
                    'common_mistakes': 'Omitting `@functools.wraps(fn)`, which causes the decorated function name to become `"wrapper"` and erases its docstring.',
                    'practice_question': 'In the syntax `@my_dec def f(): pass`, what is the equivalent assignment statement? (Answer: `f = my_dec(f)`).'
                },
                {
                    'id': 'py-context-managers',
                    'title': '5. Context Managers & the __enter__ / __exit__ Protocol',
                    'read_time': '11 min',
                    'summary': 'Build custom resource management utilities using class dunder methods and contextlib.contextmanager.',
                    'concept': """Context managers govern runtime context when executing a `with` statement. The protocol requires two methods:
1. `__enter__(self)`: Acquires the resource and returns the target bound to the `as` variable.
2. `__exit__(self, exc_type, exc_val, exc_tb)`: Executed on leaving the block. If an exception occurred, returning `True` suppresses the exception; returning `False` or `None` lets it propagate.

Alternatively, `contextlib.contextmanager` allows writing context managers using a simple generator function with a `try-yield-finally` block.""",
                    'syntax': """class DatabaseTransaction:
    def __enter__(self):
        print("Begin SQL Transaction")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print("Rollback Transaction!")
            return False
        print("Commit Transaction.")
        return True
""",
                    'code_example': """from contextlib import contextmanager

@contextmanager
def temporary_learning_session(user_id):
    print(f">> Starting sandbox session for User #{user_id}")
    session_data = {"user": user_id, "active": True}
    try:
        yield session_data
    finally:
        session_data["active"] = False
        print(f">> Terminating and saving sandbox session for User #{user_id}")

with temporary_learning_session(402) as sess:
    print(f"Inside session: {sess}")
""",
                    'expected_output': """>> Starting sandbox session for User #402
Inside session: {'user': 402, 'active': True}
>> Terminating and saving sandbox session for User #402
""",
                    'common_mistakes': 'Suppressing all exceptions inside `__exit__` by unconditionally returning `True`, which masks critical application bugs.',
                    'practice_question': 'What are the two magic methods required to implement a Python context manager class? (Answer: `__enter__` and `__exit__`).'
                },
                {
                    'id': 'py-args-kwargs-lambdas',
                    'title': '6. Variadic Arguments (*args, **kwargs) & Functional Lambdas',
                    'read_time': '10 min',
                    'summary': 'Design flexible APIs accepting variable positional and keyword arguments, paired with anonymous lambda expressions.',
                    'concept': """The `*args` and `**kwargs` syntax allows functions to accept an arbitrary number of positional and keyword arguments:
- `*args`: Collects extra positional arguments into a `tuple`.
- `**kwargs`: Collects extra keyword arguments into a `dict`.
- Forwarding: `fn(*args, **kwargs)` unpacks collections to another callable.

Lambda functions are small, anonymous, single-expression functions defined with `lambda params: expression`. They are best suited for short transform callbacks passed to `sorted()`, `map()`, or `filter()`.""",
                    'syntax': """def dynamic_handler(*args, **kwargs):
    print("Positional:", args)
    print("Keyword:", kwargs)

# Lambda
adder = lambda a, b: a + b
""",
                    'code_example': """# Flexible logging dispatcher
def log_event(event_type, *messages, **metadata):
    combined = " | ".join(str(m) for m in messages)
    print(f"[{event_type.upper()}] {combined}")
    if metadata:
        print("   Metadata:", metadata)

log_event("submission", "Student 101", "Assignment Passed", score=95, attempts=2)

# Lambda sorting by nested dictionary field
students = [
    {"name": "Zack", "score": 75},
    {"name": "Maya", "score": 98},
    {"name": "Liam", "score": 86}
]
students.sort(key=lambda s: s["score"], reverse=True)
print("Leaderboard:", [s["name"] for s in students])
""",
                    'expected_output': """[SUBMISSION] Student 101 | Assignment Passed
   Metadata: {'score': 95, 'attempts': 2}
Leaderboard: ['Maya', 'Liam', 'Zack']
""",
                    'common_mistakes': 'Assigning complex multi-line logic to lambdas. Lambdas can only contain a single expression. For anything more complex, write a `def` function.',
                    'practice_question': 'What type does `*args` evaluate to inside a function body? (Answer: `tuple`).'
                },
                {
                    'id': 'py-complexity-profiling',
                    'title': '7. Algorithmic Complexity, Big-O & Profiling in Python',
                    'read_time': '12 min',
                    'summary': 'Analyze time and space complexity, identify bottlenecks with cProfile, and optimize Python execution.',
                    'concept': """Algorithmic performance dictates how execution time scales with input size $n$.
- $O(1)$: Constant time (dict lookup, list append).
- $O(\\log n)$: Logarithmic (binary search in sorted sequence).
- $O(n)$: Linear (linear search, list iteration).
- $O(n \\log n)$: Linearithmic (Timsort `list.sort()`).
- $O(n^2)$: Quadratic (nested loops over input).

Python standard library includes `cProfile` and `timeit` for rigorous profiling. Bottlenecks often arise from repeated list lookups (`item in list` is $O(n)$) where a set lookup (`item in set` is $O(1)$) should be used.""",
                    'syntax': """import timeit

# Measure execution time of small snippets
timeit.timeit("x = [i**2 for i in range(1000)]", number=1000)
""",
                    'code_example': """import time

n = 20000
test_list = list(range(n))
test_set = set(range(n))

target = n - 1

# List lookup benchmark
t0 = time.perf_counter()
_ = target in test_list
list_time = time.perf_counter() - t0

# Set lookup benchmark
t0 = time.perf_counter()
_ = target in test_set
set_time = time.perf_counter() - t0

print(f"List search time ($O(n)$): {list_time * 1e6:.2f} microseconds")
print(f"Set search time ($O(1)$):  {set_time * 1e6:.2f} microseconds")
print(f"Set lookup speedup: {list_time / (set_time + 1e-9):.1f}x faster!")
""",
                    'expected_output': """List search time ($O(n)$): 240.50 microseconds
Set search time ($O(1)$):  1.20 microseconds
Set lookup speedup: 200.4x faster!
""",
                    'common_mistakes': 'Using `+` string concatenation inside a loop over thousands of strings ($O(n^2)$ due to immutability). Always collect into a list and use `"".join(list)` ($O(n)$).',
                    'practice_question': 'What is the average time complexity of checking membership `x in collection` when `collection` is a Python set vs a list? (Answer: $O(1)$ for set, $O(n)$ for list).'
                },
                {
                    'id': 'py-testing-tdd',
                    'title': '8. Automated Unit Testing with unittest & TDD',
                    'read_time': '11 min',
                    'summary': 'Write comprehensive unit test suites using the unittest module, test fixtures (setUp, tearDown), and assertions.',
                    'concept': """Automated testing guarantees that code functions as specified and protects against regressions. Test-Driven Development (TDD) advocates:
1. Write a failing test (Red).
2. Write minimal code to pass the test (Green).
3. Refactor code while keeping tests green (Refactor).

Python includes `unittest` in its standard library. Tests subclass `unittest.TestCase` and methods starting with `test_` are discovered and executed automatically. Assertions verify expectations: `assertEqual`, `assertTrue`, `assertRaises`, `assertIn`.""",
                    'syntax': """import unittest

class TestProgressionLogic(unittest.TestCase):
    def setUp(self):
        self.passing_score = 70

    def test_passing_unlocks(self):
        self.assertTrue(85 >= self.passing_score)

if __name__ == "__main__":
    unittest.main()
""",
                    'code_example': """import unittest

def calculate_level_progression(score):
    if score < 0 or score > 100:
        raise ValueError("Invalid score range")
    return "Unlocked" if score >= 70 else "Locked"

class ProgressionUnitTests(unittest.TestCase):
    def test_unlock_on_exact_threshold(self):
        self.assertEqual(calculate_level_progression(70), "Unlocked")

    def test_locked_below_threshold(self):
        self.assertEqual(calculate_level_progression(69.9), "Locked")

    def test_out_of_bounds_exception(self):
        with self.assertRaises(ValueError):
            calculate_level_progression(105)

# Run test runner directly
suite = unittest.TestLoader().loadTestsFromTestCase(ProgressionUnitTests)
runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)
print(f"Tests run: {result.testsRun}, Errors: {len(result.errors)}, Failures: {len(result.failures)}")
""",
                    'expected_output': """...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
Tests run: 3, Errors: 0, Failures: 0
""",
                    'common_mistakes': 'Naming test methods without the `test_` prefix (e.g. `def verify_score():`). Test runners will silently skip them!',
                    'practice_question': 'Which assertion method verifies that a specific exception is raised during code execution? (Answer: `self.assertRaises(ExceptionType)`).'
                },
                {
                    'id': 'py-production-apis',
                    'title': '9. Production APIs, Serialization & HTTP Workflows',
                    'read_time': '11 min',
                    'summary': 'Build RESTful patterns, serialize nested JSON, handle network timeouts, and structure production Flask routes.',
                    'concept': """Modern Python applications integrate with distributed microservices and frontends via REST APIs and JSON (JavaScript Object Notation).

Key Production Principles:
- Strict JSON serialization with custom encoders for dates and Decimals.
- Graceful network error handling: Always specify request timeouts and catch connection/timeout exceptions.
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Internal Server Error).
- Input validation: Validate types, presence, and boundary values before touching database persistence layers.""",
                    'syntax': """from flask import jsonify, request

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.get_json()
    if not data or 'score' not in data:
        return jsonify({'error': 'Missing score payload'}), 400
    return jsonify({'status': 'success', 'data': data}), 200
""",
                    'code_example': """import json

def validate_submission_payload(payload_str):
    try:
        data = json.loads(payload_str)
    except json.JSONDecodeError:
        return False, "Malformed JSON", 400

    required_fields = ["user_id", "subject", "level", "answers"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}", 422

    return True, "Valid payload", 200

valid_json = '{"user_id": 42, "subject": "python", "level": "easy", "answers": [0, 2, 1]}'
success, msg, code = validate_submission_payload(valid_json)
print(f"Validation Result: {code} -> {msg}")
""",
                    'expected_output': """Validation Result: 200 -> Valid payload
""",
                    'common_mistakes': 'Trusting raw client input without server-side validation. Clients can manipulate requests; the server must always validate and compute authorization and scores.',
                    'practice_question': 'Which HTTP status code signifies that the client is authenticated but forbidden from accessing a locked resource? (Answer: 403 Forbidden).'
                }
            ]
        }
    }
}
