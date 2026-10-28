import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, g, current_app, has_request_context
from models import db, ChatMessage
from auth import login_required
from content import SUBJECTS_CATALOG

chatbot_bp = Blueprint('chatbot', __name__)

# System persona for EduAdapt-AI
EDUCATIONAL_SYSTEM_PROMPT = """You are EduAdapt Tutor, a friendly, encouraging, and expert AI tutor for the EduAdapt-AI Personalized Student Learning Platform.
You teach 4 core computer science subjects:
1. Python Programming
2. Java Programming
3. Database Management Systems (DBMS)
4. Data Structures and Algorithms (DSA)

Pedagogical Guidelines:
- Adopt a clear, structured, and patient teaching style.
- When students ask for assignment help or hints, guide them conceptually with hints and pseudocode; DO NOT simply give away answers directly.
- When explaining code, break it down clearly line-by-line.
- Use formatting (markdown headers, bullet points, and code blocks) for readability.
- Maintain an encouraging and motivating tone.
"""

# Local Educational Rule-Based Knowledge Base
KNOWLEDGE_BASE = {
    'python': {
        'keywords': ['python', 'py', 'pvm', 'pip', 'pep8', 'indentation', 'duck typing', 'decorator', 'generator', 'comprehension'],
        'concepts': {
            'decorator': """In Python, a **Decorator** is a higher-order function that takes another function as an argument and extends its behavior without modifying its source code.
Syntax:
```python
def my_decorator(fn):
    def wrapper(*args, **kwargs):
        print("Before execution")
        result = fn(*args, **kwargs)
        print("After execution")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")
```
Decorators are widely used for logging, authentication, caching (`@lru_cache`), and route binding in Flask!""",
            'generator': """A **Generator** is a function that produces a sequence of values lazily using the `yield` statement.
Instead of storing millions of items in RAM all at once (like a list), a generator produces items on-the-fly, consuming $O(1)$ memory!
Example:
```python
def count_stream(n):
    count = 1
    while count <= n:
        yield count
        count += 1

# Lazy consumption
for num in count_stream(3):
    print(num)
```""",
            'comprehension': """**Comprehensions** provide concise, expressive syntax for creating new sequences.
Forms:
- List: `[x**2 for x in range(10) if x % 2 == 0]`
- Dict: `{k: v for k, v in pairs if v >= 70}`
- Set: `{len(w) for w in words}`
Comprehensions run at C-speed in the Python bytecode interpreter, making them faster than traditional for-loop appends!""",
            'oop': """Python supports full **Object-Oriented Programming (OOP)**:
- Encapsulation: Binding data and methods within a `class`.
- `__init__(self)`: Instance constructor method.
- `self`: Explicit reference to the current object instance.
- Inheritance: `class Student(User):`
- Polymorphism & Duck Typing: "If it walks like a duck and quacks like a duck, it is a duck." Classes don't need formal interface inheritance as long as they implement the expected methods."""
        }
    },
    'java': {
        'keywords': ['java', 'jvm', 'jdk', 'jre', 'stringbuilder', 'collections', 'multithreading', 'interface', 'abstract class', 'streams', 'lambda'],
        'concepts': {
            'jvm': """The **Java Virtual Machine (JVM)** is the abstract runtime engine that executes compiled Java bytecode (`.class` files).
Key components:
1. **Classloader Subsystem**: Loads, links, and initializes bytecode into memory.
2. **JVM Memory**: Method Area, Heap (objects), Java Stacks (method frames), PC Registers, Native Stacks.
3. **Execution Engine**: Bytecode Interpreter + JIT (Just-In-Time) Compiler + Garbage Collector (GC).
4. **WORA**: "Write Once, Run Anywhere" is enabled because bytecode runs on any OS having a compatible JVM!""",
            'stringbuilder': """In Java, `String` objects are **immutable**. Any concatenation (`+`) creates a brand-new string on the heap.
Doing this in a loop causes $O(n^2)$ memory churn!
**StringBuilder** provides a mutable character buffer:
```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100; i++) {
    sb.append(i).append(" ");
}
String result = sb.toString();
```
Use `StringBuilder` for single-threaded mutation and `StringBuffer` if multi-threaded synchronization is strictly required.""",
            'streams': """The **Java 8 Stream API** enables declarative, functional processing of collections:
- **Intermediate operations** (lazy): `filter()`, `map()`, `sorted()`, `distinct()`.
- **Terminal operations** (eager): `collect()`, `reduce()`, `forEach()`, `count()`.
Example:
```java
List<String> honorRoll = students.stream()
    .filter(s -> s.getGpa() >= 3.8)
    .map(Student::getName)
    .sorted()
    .collect(Collectors.toList());
```""",
            'multithreading': """Java provides concurrent execution through Threads:
1. Implement `Runnable` (recommended): `new Thread(() -> System.out.println("Running")).start();`
2. Extend `Thread`: override `run()`.
Always start a thread using `thread.start()` (which spawns an OS thread), NOT `thread.run()` (which executes synchronously in the caller thread)!"""
        }
    },
    'dbms': {
        'keywords': ['dbms', 'sql', 'normalization', 'acid', 'join', 'subquery', 'primary key', 'foreign key', 'b+ tree', 'wal', '2pl'],
        'concepts': {
            'normalization': """**Database Normalization** systematically eliminates redundant data and update anomalies:
- **1NF**: Atomic cell values (no repeating groups/arrays) + unique primary key.
- **2NF**: In 1NF + No Partial Dependencies (non-key columns must depend on the whole composite primary key).
- **3NF**: In 2NF + No Transitive Dependencies (non-key columns must not depend on other non-key columns).
- **BCNF**: Stricter 3NF where for every functional dependency $X \\rightarrow Y$, $X$ must be a Super Key!""",
            'acid': """**ACID Properties** guarantee transactional reliability in relational databases:
- **A (Atomicity)**: "All or Nothing." If any step in a transaction fails, everything is rolled back via Write-Ahead Logs.
- **C (Consistency)**: Transactions transition the database from one valid integrity state to another.
- **I (Isolation)**: Concurrent transactions execute without cross-contamination, enforced by Two-Phase Locking (2PL) and MVCC.
- **D (Durability)**: Once committed, updates survive server crashes and power loss via flushed transaction logs.""",
            'join': """**SQL Joins** combine rows from two tables:
- **INNER JOIN**: Returns only matching rows from both tables.
- **LEFT JOIN**: Returns all left table rows, with NULLs for unmatched right rows.
- **RIGHT JOIN**: Returns all right table rows, with NULLs for unmatched left rows.
- **FULL OUTER JOIN**: Returns all rows from both tables, filling mismatches with NULLs.
- **CROSS JOIN**: Cartesian product ($N \\times M$ rows).""",
            'indexing': """Without indexes, finding a record requires a full disk table scan ($O(n)$).
Databases use **B+ Tree Indexes**:
- Balanced search tree with high fanout (thousands of keys per disk block).
- Data records or pointers reside exclusively in the leaf nodes.
- Leaf nodes are linked sequentially, providing $O(\\log n)$ search and fast range scans (`BETWEEN`)."""
        }
    },
    'dsa': {
        'keywords': ['dsa', 'big-o', 'algorithm', 'binary search', 'linked list', 'stack', 'queue', 'tree', 'graph', 'dynamic programming', 'heap', 'sorting'],
        'concepts': {
            'big-o': """**Big-O Notation** measures how runtime or space scales as input size $n \\rightarrow \\infty$:
- $O(1)$: Constant (Array index access, hash table lookup)
- $O(\\log n)$: Logarithmic (Binary search in sorted array)
- $O(n)$: Linear (Linear search, traversing a list)
- $O(n \\log n)$: Linearithmic (Merge Sort, Heap Sort)
- $O(n^2)$: Quadratic (Nested loops, Bubble Sort)
- $O(2^n)$: Exponential (Naive recursive Fibonacci)""",
            'dynamic programming': """**Dynamic Programming (DP)** solves complex problems by breaking them into overlapping subproblems and storing the sub-answers (memoization or tabulation).
Classic examples:
- 0/1 Knapsack: $O(n \\cdot W)$
- Longest Common Subsequence (LCS): $O(m \\cdot n)$
- Shortest Path: Floyd-Warshall
DP requires:
1. **Optimal Substructure**: Global optimal solution constructed from sub-optimal solutions.
2. **Overlapping Subproblems**: The same recursive subproblems are encountered repeatedly.""",
            'binary search': """**Binary Search** finds a target in a **SORTED** array in $O(\\log n)$ time by halving the search space each step:
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```""",
            'trees': """A **Binary Search Tree (BST)** enforces:
For every node $X$, $\\text{Left Subtree Keys} < X < \\text{Right Subtree Keys}$.
Traversals:
- **Inorder (Left, Root, Right)**: Visits BST keys in ascending sorted order!
- **Preorder (Root, Left, Right)**: Useful for copying trees.
- **Postorder (Left, Right, Root)**: Useful for bottom-up deletions."""
        }
    }
}

def generate_local_response(user_message, subject_context=None, level_context=None):
    msg_lower = user_message.lower().strip()
    name = session.get('user_name', 'Student') if has_request_context() and 'user_name' in session else 'Student'
    
    # 1. Greetings
    if any(msg_lower.startswith(g) for g in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']) or msg_lower in ['hi', 'hello', 'hey']:
        return (
            f"Hello {name}! 👋 I am your **EduAdapt-AI Learning Tutor**.\n\n"
            f"I can help you with:\n"
            f"- 🐍 **Python Programming** (syntax, OOP, decorators, generators)\n"
            f"- ☕ **Java Programming** (JVM, OOP, collections, streams, threads)\n"
            f"- 🗄️ **DBMS** (SQL queries, relational algebra, 1NF-BCNF, ACID)\n"
            f"- 🌲 **Data Structures & Algorithms** (Big-O, trees, graphs, DP)\n\n"
            f"Feel free to ask a concept question, request code explanation, ask for an assessment hint, or say **'quiz me on [subject]'**!"
        )

    # 2. Progression rules
    if any(phrase in msg_lower for phrase in ['unlock', 'how to unlock', 'how do i unlock', 'pass score', 'passing percentage', 'how do i advance', 'threshold']):
        return (
            "🎯 **EduAdapt-AI Learning Progression Rules**:\n\n"
            "1. **Level 1 (Easy)**: Unlocked by default as soon as you enroll in a subject.\n"
            "2. **Level 2 (Medium)**: Unlocked automatically when you score **70% or higher** on the Level 1 (Easy) assessment.\n"
            "3. **Level 3 (Complex)**: Unlocked automatically when you score **70% or higher** on the Level 2 (Medium) assessment.\n"
            "4. **Subject Mastery**: Passing the Level 3 (Complex) assessment with $\\ge 70\\%$ marks that subject as **Completed** on your dashboard!\n\n"
            "If you fail an assessment, don't worry: you can revisit the study material anytime and retake the assessment as many times as you need!"
        )

    # 3. Hint request (pedagogical hint without revealing direct answer)
    if any(h in msg_lower for h in ['hint', 'clue', 'stuck', 'help with assignment', 'dont give answer', "don't give answer"]):
        return (
            "💡 **EduAdapt Conceptual Hint**:\n\n"
            "When approaching this problem:\n"
            "1. **Identify the Core Invariant**: What property must remain true after every step? (For example, in a BST, left < root < right; in 2PL, no locks after first unlock).\n"
            "2. **Check the Base Case**: What is the simplest input possible (e.g. empty list, length 1, zero)?\n"
            "3. **Eliminate Distractors**: In multiple choice questions, eliminate options that violate definition bounds (e.g. primary keys containing NULL, or naive quicksort on sorted data without random pivots).\n\n"
            "Tell me the specific topic or question you are working on, and I'll give you a targeted conceptual clue without spoiling the answer!"
        )

    # 4. Code Explanation request
    code_indicators = ['def ', 'class ', 'public static void', 'system.out', 'select ', 'create table', 'function', 'for (int', 'import ']
    if 'explain' in msg_lower and any(ind in msg_lower for ind in code_indicators):
        return (
            "🔍 **Line-by-Line Code Breakdown**:\n\n"
            "Here is how this logic operates step-by-step:\n"
            "1. **Declaration & Signature**: Defines the component, specifying parameter types, return contracts, and encapsulation boundaries.\n"
            "2. **Initialization**: Variables and memory buffers are allocated before loop or computation starts.\n"
            "3. **Core Computation Loop**: Executes the primary algorithm, maintaining state invariants across iterations.\n"
            "4. **Termination & Return**: Returns the calculated result or releases acquired system resources.\n\n"
            "To get a tailored line-by-line review, paste your exact code snippet enclosed in triple backticks!"
        )

    # 5. Quiz Me / Practice question request
    if 'quiz me' in msg_lower or 'practice question' in msg_lower:
        if 'python' in msg_lower or subject_context == 'python':
            return (
                "📝 **Python Quick Check**:\n\n"
                "**Question**: What is the result of `type(10 / 2)` in Python 3?\n\n"
                "A) `<class 'int'>`\n"
                "B) `<class 'float'>`\n"
                "C) `<class 'double'>`\n"
                "D) `<class 'number'>`\n\n"
                "*Reply with your choice (A, B, C, or D) to check your understanding!*"
            )
        elif 'java' in msg_lower or subject_context == 'java':
            return (
                "📝 **Java Quick Check**:\n\n"
                "**Question**: Why is the `main` method declared as `static` in Java?\n\n"
                "A) To run in a separate background thread\n"
                "B) So the JVM can invoke it directly without instantiating an object of the class\n"
                "C) To make all local variables within it static constants\n"
                "D) To prevent garbage collection\n\n"
                "*Reply with your choice (A, B, C, or D) to check your understanding!*"
            )
        elif 'dbms' in msg_lower or subject_context == 'dbms':
            return (
                "📝 **DBMS Quick Check**:\n\n"
                "**Question**: What type of functional dependency is eliminated when a table is normalized from 1NF to 2NF?\n\n"
                "A) Transitive Dependency\n"
                "B) Partial Dependency of non-prime attributes on a composite candidate key\n"
                "C) Multivalued Dependency\n"
                "D) Cyclic Join Dependency\n\n"
                "*Reply with your choice (A, B, C, or D) to check your understanding!*"
            )
        else:
            return (
                "📝 **DSA Quick Check**:\n\n"
                "**Question**: What is the worst-case time complexity of Binary Search on a sorted array of $n$ elements?\n\n"
                "A) $O(1)$\n"
                "B) $O(\\log n)$\n"
                "C) $O(n)$\n"
                "D) $O(n \\log n)$\n\n"
                "*Reply with your choice (A, B, C, or D) to check your understanding!*"
            )

    # 6. Specific Concept matching across the knowledge base
    for domain, domain_data in KNOWLEDGE_BASE.items():
        for concept_key, concept_text in domain_data['concepts'].items():
            if concept_key in msg_lower or any(kw in msg_lower for kw in concept_key.split()):
                return f"📘 **Concept Review: {concept_key.title()}** ({domain.upper()})\n\n{concept_text}"

    # 7. Common Error Debugging
    if 'indexerror' in msg_lower or 'index out of bounds' in msg_lower:
        return (
            "⚠️ **Debugging: IndexError / ArrayIndexOutOfBoundsException**\n\n"
            "**Cause**: You attempted to access an array or list index that does not exist.\n"
            "Remember that in zero-indexed collections of size $n$:\n"
            "- Valid indices are strictly from `0` to `n - 1`.\n"
            "- Index `n` is always out of bounds!\n\n"
            "**Fix**: Verify your loop boundary is `i < len(arr)` or `i < arr.length`, NOT `<= length`."
        )
    if 'nullpointer' in msg_lower:
        return (
            "⚠️ **Debugging: NullPointerException (NPE)**\n\n"
            "**Cause**: You invoked a method or accessed a field on an object reference that currently points to `null`.\n\n"
            "**Fixes**:\n"
            "1. Add defensive null checks: `if (obj != null) { obj.doWork(); }`\n"
            "2. Use Java 8 `Optional<T>` to make missing values explicit.\n"
            "3. Ensure constructor dependency injection initializes all required references."
        )

    # 8. Domain specific broad overview
    if 'python' in msg_lower:
        return (
            "🐍 **Python Programming Track Overview**:\n\n"
            "Python is an interpreted, dynamically typed language emphasizing readable code.\n"
            "- **Level 1 (Easy)**: Variables, data types, loops, strings, lists, tuples, and dictionaries.\n"
            "- **Level 2 (Medium)**: Functions, recursion, comprehensions, file handling (`with`), and OOP classes.\n"
            "- **Level 3 (Complex)**: Abstract base classes, generators (`yield`), decorators, context managers, and Big-O profiling.\n\n"
            "What specific Python topic would you like to explore?"
        )
    if 'java' in msg_lower:
        return (
            "☕ **Java Programming Track Overview**:\n\n"
            "Java is a strongly typed, class-based, object-oriented language running on the JVM.\n"
            "- **Level 1 (Easy)**: JVM architecture, primitive types, control flow, loops, and 1D/2D arrays.\n"
            "- **Level 2 (Medium)**: String immutability, StringBuilder, OOP encapsulation, inheritance, interfaces, and polymorphism.\n"
            "- **Level 3 (Complex)**: Checked/unchecked exceptions, generics, collections, Streams, lambdas, and multithreading.\n\n"
            "Which Java concept can I explain for you?"
        )
    if 'dbms' in msg_lower or 'database' in msg_lower or 'sql' in msg_lower:
        return (
            "🗄️ **DBMS Track Overview**:\n\n"
            "Database Management Systems organize data reliably using relational theory and SQL.\n"
            "- **Level 1 (Easy)**: 3-tier schema architecture, keys (primary, foreign, candidate), ER modeling, and SQL DDL.\n"
            "- **Level 2 (Medium)**: SQL DML, joins (inner/left/right), aggregates, GROUP BY, HAVING, subqueries, and views.\n"
            "- **Level 3 (Complex)**: Functional dependencies, normalization (1NF, 2NF, 3NF, BCNF), ACID, 2PL locking, and B+ Trees.\n\n"
            "What database or SQL challenge are you working on?"
        )
    if 'dsa' in msg_lower or 'algorithm' in msg_lower or 'data structure' in msg_lower:
        return (
            "🌲 **Data Structures & Algorithms Track Overview**:\n\n"
            "DSA equips you to write computationally efficient software.\n"
            "- **Level 1 (Easy)**: Big-O analysis, arrays, two-pointer techniques, linked lists, stacks, queues, and binary search.\n"
            "- **Level 2 (Medium)**: Doubly linked lists, hashing, merge sort, quicksort, binary trees, BSTs, and heaps.\n"
            "- **Level 3 (Complex)**: AVL trees, graph representations, BFS, DFS, Dijkstra, Minimum Spanning Trees, 0/1 Knapsack DP, and Backtracking.\n\n"
            "Ask me to break down any algorithm or data structure!"
        )

    # 9. General helpful fallback
    return (
        f"That is a great learning inquiry, {name}!\n\n"
        f"As your EduAdapt-AI Tutor, I specialize in **Python**, **Java**, **DBMS**, and **Data Structures & Algorithms**.\n\n"
        f"Try asking:\n"
        f"- *'Explain Big-O notation with simple examples'*\n"
        f"- *'What is the difference between 3NF and BCNF?'*\n"
        f"- *'How does StringBuilder improve Java performance?'*\n"
        f"- *'What is a Python decorator and when do I use it?'*\n"
        f"- *'How do I unlock Level 2?'*\n"
        f"- *'Quiz me on DSA'*"
    )

def query_cloud_ai_provider(prompt, context=None):
    """
    Optional AI integration via server-side environment variables.
    Supports Google Gemini API or OpenAI API without paid third-party dependencies.
    Times out safely to ensure instant fallback to local tutor.
    """
    gemini_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY') or os.environ.get('AI_API_KEY')
    openai_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    
    # 1. Try Gemini REST endpoint if key provided
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {'Content-Type': 'application/json'}
            
            full_prompt = f"{EDUCATIONAL_SYSTEM_PROMPT}\nContext: {context or 'General CS'}\nStudent Question: {prompt}"
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }]
            }
            
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=4.0) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                candidates = res_data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', ''), 'gemini_cloud_ai'
        except Exception:
            # Fall back seamlessly to local rule-based tutor
            pass

    # 2. Try OpenAI REST endpoint if key provided
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {openai_key}'
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": EDUCATIONAL_SYSTEM_PROMPT},
                    {"role": "user", "content": f"[Context: {context or 'General CS'}] {prompt}"}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=4.0) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                choices = res_data.get('choices', [])
                if choices:
                    return choices[0].get('message', {}).get('content', ''), 'openai_cloud_ai'
        except Exception:
            pass

    # If no key or cloud query failed, return None to trigger local rule engine
    return None, None

@chatbot_bp.route('/chatbot')
@login_required
def chat_page():
    user = g.user
    
    # Retrieve past messages for this user (up to last 20)
    history = ChatMessage.query.filter_by(user_id=user.id).order_by(ChatMessage.created_at.asc()).limit(20).all()
    
    return render_template(
        'chatbot/chat.html',
        user=user,
        history=history,
        catalog=SUBJECTS_CATALOG
    )

@chatbot_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    user = g.user
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    subject_context = data.get('subject_context')
    level_context = data.get('level_context')

    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Save user message to database
    user_msg_record = ChatMessage(
        user_id=user.id,
        role='user',
        content=user_message,
        subject_context=subject_context,
        level_context=level_context,
        created_at=datetime.utcnow()
    )
    db.session.add(user_msg_record)

    # Check for optional Cloud AI first
    context_str = f"Subject: {subject_context or 'General'}, Level: {level_context or 'Any'}"
    ai_response, source = query_cloud_ai_provider(user_message, context_str)
    
    if not ai_response:
        # High-intelligence local educational tutor
        ai_response = generate_local_response(user_message, subject_context, level_context)
        source = 'local_rule_tutor'

    # Save assistant message to database
    bot_msg_record = ChatMessage(
        user_id=user.id,
        role='assistant',
        content=ai_response,
        subject_context=subject_context,
        level_context=level_context,
        created_at=datetime.utcnow()
    )
    db.session.add(bot_msg_record)
    db.session.commit()

    return jsonify({
        'response': ai_response,
        'source': source,
        'timestamp': datetime.utcnow().strftime('%I:%M %p')
    })

@chatbot_bp.route('/api/chat/clear', methods=['POST'])
@login_required
def api_clear_chat():
    user = g.user
    ChatMessage.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Chat history cleared'})
