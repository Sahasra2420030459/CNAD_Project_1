/**
 * EduAdapt-AI - Client-Side Rule-Based Educational AI Tutor
 * Powers the floating widget on all pages and the full /chatbot.html page.
 * Completely frontend-only without external backend APIs or cloud costs.
 */

(function () {
    const KNOWLEDGE_BASE = {
        python: {
            keywords: ['python', 'py', 'pvm', 'pip', 'pep8', 'indentation', 'duck typing', 'decorator', 'generator', 'comprehension', 'lambda', 'self'],
            concepts: {
                decorator: `In Python, a **Decorator** is a higher-order function that takes another function as an argument and extends or alters its behavior without modifying its source code.
Syntax:
\`\`\`python
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
\`\`\`
Decorators are widely used for logging, authorization, caching (\`@functools.lru_cache\`), and framework routing!`,

                generator: `A **Generator** in Python produces a sequence of values lazily using the \`yield\` statement.
Instead of storing millions of elements in RAM all at once (like a giant list), a generator produces each item on-demand, consuming $O(1)$ memory!
Example:
\`\`\`python
def count_up(n):
    count = 1
    while count <= n:
        yield count
        count += 1

# Consuming lazily
for num in count_up(3):
    print(num)
\`\`\``,

                comprehension: `**Comprehensions** provide concise, expressive syntax for creating new sequences.
Forms:
- List: \`[x**2 for x in range(10) if x % 2 == 0]\`
- Dict: \`{k: v for k, v in pairs if v >= 70}\`
- Set: \`{len(w) for w in words}\`
Comprehensions execute at C-level speed inside CPython bytecode, performing faster than conventional \`for\` loops with \`.append()\`!`,

                oop: `Python supports full **Object-Oriented Programming (OOP)**:
- Encapsulation: Grouping attributes and methods inside a \`class\`.
- \`__init__(self)\`: Instance initializer constructor.
- \`self\`: Explicit reference to the current object instance.
- Inheritance: \`class Student(User):\`
- Polymorphism & Duck Typing: "If it walks like a duck and quacks like a duck, it is a duck." Classes don't need formal interface inheritance as long as they implement expected methods.`
            }
        },

        java: {
            keywords: ['java', 'jvm', 'jdk', 'jre', 'stringbuilder', 'collections', 'multithreading', 'interface', 'abstract class', 'streams', 'generics'],
            concepts: {
                jvm: `The **Java Virtual Machine (JVM)** is the abstract execution engine that executes compiled Java bytecode (\`.class\` files).
Key components:
1. **Classloader Subsystem**: Loads, links, and initializes bytecode into memory.
2. **JVM Memory**: Method Area, Heap (objects), Java Stacks (method frames), PC Registers, Native Stacks.
3. **Execution Engine**: Bytecode Interpreter + JIT (Just-In-Time) Compiler + Garbage Collector (GC).
4. **WORA**: "Write Once, Run Anywhere" is enabled because the same bytecode runs on any OS having a compatible JVM!`,

                stringbuilder: `In Java, \`String\` objects are **immutable**. Any concatenation (\`+\`) creates a brand-new object on the heap.
Doing this in a loop causes $O(n^2)$ memory churn!
**StringBuilder** provides an efficient mutable character buffer:
\`\`\`java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100; i++) {
    sb.append(i).append(" ");
}
String result = sb.toString();
\`\`\`
Use \`StringBuilder\` for single-threaded mutation and \`StringBuffer\` if multi-threaded synchronization is strictly required.`,

                streams: `The **Java 8 Stream API** enables declarative, functional processing of collections:
- **Intermediate operations** (lazy): \`filter()\`, \`map()\`, \`sorted()\`, \`distinct()\`.
- **Terminal operations** (eager): \`collect()\`, \`reduce()\`, \`forEach()\`, \`count()\`.
Example:
\`\`\`java
List<String> honorRoll = students.stream()
    .filter(s -> s.getGpa() >= 3.8)
    .map(Student::getName)
    .sorted()
    .collect(Collectors.toList());
\`\`\``,

                multithreading: `Java provides concurrent execution through Threads:
1. Implement \`Runnable\` (recommended):
\`\`\`java
Thread t = new Thread(() -> System.out.println("Running concurrently"));
t.start();
\`\`\`
2. Extend \`Thread\`: override \`run()\`.
Always start a thread using \`thread.start()\` (which spawns an OS thread), NOT \`thread.run()\` (which executes synchronously in the caller thread)!`
            }
        },

        dbms: {
            keywords: ['dbms', 'sql', 'normalization', 'acid', 'join', 'subquery', 'primary key', 'foreign key', 'b+ tree', 'wal', 'index', 'transaction'],
            concepts: {
                normalization: `**Database Normalization** systematically eliminates redundant data and update anomalies:
- **1NF**: Atomic column values (no repeating groups or arrays) + unique primary key.
- **2NF**: In 1NF + No Partial Dependencies (non-key columns must depend on the whole composite primary key).
- **3NF**: In 2NF + No Transitive Dependencies (non-key columns must not depend on other non-key columns).
- **BCNF**: Stricter 3NF where for every functional dependency $X \\rightarrow Y$, $X$ must be a Super Key!`,

                acid: `**ACID Properties** guarantee transactional reliability in relational databases:
- **A (Atomicity)**: "All or Nothing." If any step fails, all operations are reverted via rollback.
- **C (Consistency)**: Transactions transition the database from one valid integrity state to another.
- **I (Isolation)**: Concurrent transactions execute without cross-contamination (enforced via 2PL and MVCC).
- **D (Durability)**: Once committed, updates survive server crashes and power loss via flushed write-ahead logs.`,

                join: `**SQL Joins** combine rows from two or more tables:
- **INNER JOIN**: Returns only matching rows from both tables.
- **LEFT JOIN**: Returns all left table rows, filling unmatched right columns with NULL.
- **RIGHT JOIN**: Returns all right table rows, filling unmatched left columns with NULL.
- **FULL OUTER JOIN**: Returns all rows from both tables, filling mismatches with NULL.
- **CROSS JOIN**: Cartesian product ($N \\times M$ rows).`,

                indexing: `Without indexes, finding a record requires a full disk table scan ($O(n)$).
Databases use **B+ Tree Indexes**:
- Balanced search tree with high fanout (thousands of keys per disk block).
- Data records or leaf pointers reside exclusively in leaf nodes.
- Leaf nodes are linked sequentially, providing $O(\\log n)$ point lookups and fast range scans (\`BETWEEN\`).`
            }
        },

        dsa: {
            keywords: ['dsa', 'big-o', 'algorithm', 'binary search', 'linked list', 'stack', 'queue', 'tree', 'graph', 'dynamic programming', 'heap', 'sorting'],
            concepts: {
                'big-o': `**Big-O Notation** measures how runtime or memory scales as input size $n \\rightarrow \\infty$:
- $O(1)$: Constant (Array index access, hash table lookup)
- $O(\\log n)$: Logarithmic (Binary search in sorted array)
- $O(n)$: Linear (Linear search, traversing a list)
- $O(n \\log n)$: Linearithmic (Merge Sort, Heap Sort)
- $O(n^2)$: Quadratic (Nested loops, Bubble Sort)
- $O(2^n)$: Exponential (Naive recursive Fibonacci)`,

                'dynamic programming': `**Dynamic Programming (DP)** solves complex problems by breaking them into overlapping subproblems and storing the sub-answers (memoization or tabulation).
Classic examples:
- 0/1 Knapsack: $O(n \\cdot W)$
- Longest Common Subsequence (LCS): $O(m \\cdot n)$
- Shortest Path: Floyd-Warshall
DP requires:
1. **Optimal Substructure**: Global optimal solution constructed from sub-optimal solutions.
2. **Overlapping Subproblems**: The same recursive subproblems are encountered repeatedly.`,

                'binary search': `**Binary Search** finds a target in a **SORTED** array in $O(\\log n)$ time by halving the search space each step:
\`\`\`python
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
\`\`\``,

                trees: `A **Binary Search Tree (BST)** enforces:
For every node $X$, $\\text{Left Subtree Keys} < X < \\text{Right Subtree Keys}$.
Traversals:
- **Inorder (Left, Root, Right)**: Visits BST keys in ascending sorted order!
- **Preorder (Root, Left, Right)**: Useful for duplicating trees.
- **Postorder (Left, Right, Root)**: Useful for bottom-up deletions.`
            }
        }
    };

    function generateResponse(userMessage, subjectContext) {
        const msg = userMessage.toLowerCase().trim();
        const user = window.Auth ? window.Auth.getCurrentUser() : null;
        const name = user ? user.name.split(' ')[0] : 'Student';

        // 1. Greetings
        if (['hi', 'hello', 'hey', 'greetings', 'help', 'good morning', 'good afternoon'].some(g => msg.startsWith(g) || msg === g)) {
            return `Hello ${name}! 👋 I am your **EduAdapt-AI Learning Tutor**.

I can assist you with:
- 🐍 **Python Programming** (syntax, OOP, decorators, generators)
- ☕ **Java Programming** (JVM, OOP, collections, streams, threads)
- 🗄️ **DBMS** (SQL queries, relational algebra, 1NF-BCNF, ACID)
- 🌲 **Data Structures & Algorithms** (Big-O, trees, graphs, DP)

Ask me a concept question, request an assignment hint, ask for code debugging, or say **"quiz me on [subject]"**!`;
        }

        // 2. Progression & Unlock Rules
        if (['unlock', 'how to unlock', 'pass score', 'threshold', 'advance'].some(p => msg.includes(p))) {
            return `🎯 **EduAdapt-AI Learning Progression Rules**:

1. **Level 1 (Easy)**: Unlocked automatically when you enroll in a subject.
2. **Level 2 (Medium)**: Unlocked automatically when you score **70% or higher** on the Level 1 (Easy) assessment.
3. **Level 3 (Complex)**: Unlocked automatically when you score **70% or higher** on the Level 2 (Medium) assessment.
4. **Subject Mastery**: Passing the Level 3 (Complex) assessment with $\\ge 70\\%$ marks that subject as **Mastered** on your dashboard!

*Note: You can revisit study topics and retry assessments anytime without penalty.*`;
        }

        // 3. Assignment Hints (Pedagogical Guidance Without Direct Spoiling)
        if (['hint', 'clue', 'stuck', 'assignment help', "don't give answer"].some(h => msg.includes(h))) {
            return `💡 **EduAdapt Conceptual Hint**:

When approaching multiple choice or coding problems:
1. **Identify the Invariant**: What property must stay true after every operation? (e.g. In a BST, left < root < right; in 2PL, no locks can be acquired after the first release).
2. **Examine Edge Cases**: Consider $n = 0$, $n = 1$, empty arrays, negative numbers, or duplicate keys.
3. **Eliminate Non-Viable Options**: Eliminate choices that violate core definitions (e.g. Primary keys containing NULL, or naive linear search on unsorted arrays taking logarithmic time).

Tell me the specific subject or topic you are working on, and I'll give you a targeted pedagogical clue!`;
        }

        // 4. Common Programming Errors
        if (msg.includes('indexerror') || msg.includes('index out of bounds') || msg.includes('out of range')) {
            return `⚠️ **Debugging: IndexError / ArrayIndexOutOfBoundsException**

**Cause**: You attempted to access an index that does not exist in the collection.
Remember that in zero-indexed arrays of length $n$:
- Valid indices are strictly \`0\` to \`n - 1\`.
- Index \`n\` is ALWAYS out of bounds!

**Fix**: Ensure your loop condition is \`i < len(arr)\` or \`i < arr.length\`, NOT \`<= length\`.`;
        }

        if (msg.includes('nullpointer') || msg.includes('null reference') || msg.includes('attributeerror')) {
            return `⚠️ **Debugging: NullPointerException / AttributeError**

**Cause**: You called a method or accessed an attribute on a reference that currently evaluates to \`null\` (Java) or \`None\` (Python).

**Fixes**:
1. Check object initialization: \`if (obj != null) { obj.doWork(); }\`
2. In Python, use safe attribute fetching: \`getattr(obj, 'prop', default_val)\`
3. In Java 8+, consider using \`Optional<T>\` to handle potentially missing values.`;
        }

        // 5. Interactive Quiz Me
        if (msg.includes('quiz me') || msg.includes('quick question')) {
            if (msg.includes('python') || subjectContext === 'python') {
                return `📝 **Python Quick Check**:

**Question**: What is the output of the expression \`type(10 / 2)\` in Python 3?

A) \`<class 'int'>\`
B) \`<class 'float'>\`
C) \`<class 'double'>\`
D) \`<class 'number'>\`

*Answer: B! The single slash \`/\` operator in Python 3 always performs floating-point division.*`;
            } else if (msg.includes('java') || subjectContext === 'java') {
                return `📝 **Java Quick Check**:

**Question**: Why is the \`main\` method declared as \`static\` in Java?

A) To run in a separate background thread
B) So the JVM can invoke it directly without instantiating an object of the class
C) To make all local variables within it static constants
D) To prevent garbage collection

*Answer: B! The JVM calls \`ClassName.main()\` before any instance of the class exists.*`;
            } else if (msg.includes('dbms') || subjectContext === 'dbms') {
                return `📝 **DBMS Quick Check**:

**Question**: What type of functional dependency is eliminated when normalising a relational schema from 1NF to 2NF?

A) Transitive Dependency
B) Partial Dependency of non-prime attributes on a composite candidate key
C) Multivalued Dependency
D) Cross Join Dependency

*Answer: B! 2NF requires every non-prime attribute to be fully functionally dependent on the primary key.*`;
            } else {
                return `📝 **DSA Quick Check**:

**Question**: What is the worst-case time complexity of Binary Search on a sorted array of $n$ elements?

A) $O(1)$
B) $O(\\log n)$
C) $O(n)$
D) $O(n \\log n)$

*Answer: B! At each step, Binary Search eliminates half the remaining search space.*`;
            }
        }

        // 6. Direct Concept Matching in Knowledge Base
        for (const domain in KNOWLEDGE_BASE) {
            const domainData = KNOWLEDGE_BASE[domain];
            for (const conceptKey in domainData.concepts) {
                if (msg.includes(conceptKey) || conceptKey.split(' ').every(w => msg.includes(w))) {
                    return `📘 **Concept Guide: ${conceptKey.toUpperCase()}** (${domain.toUpperCase()})

${domainData.concepts[conceptKey]}`;
                }
            }
        }

        // 7. Broad Domain Overviews
        if (msg.includes('python')) {
            return `🐍 **Python Track Overview**:
Python is a dynamically typed, interpreted language emphasizing code readability.
- **Easy**: Variables, datatypes, operators, conditionals, loops, strings, lists, dicts.
- **Medium**: Functions, recursion, comprehensions, file I/O, OOP classes, inheritance.
- **Complex**: Metaprogramming, decorators, generators, context managers, and profiling.

Which Python concept would you like to review?`;
        }
        if (msg.includes('java')) {
            return `☕ **Java Track Overview**:
Java is a statically typed, class-based, object-oriented language executed on the JVM.
- **Easy**: JVM architecture, primitives, control flow, loops, methods, arrays.
- **Medium**: String immutability, StringBuilder, OOP, inheritance, interfaces, file I/O.
- **Complex**: Generics, collections framework, lambda streams, multithreading, and GC.

What Java topic can I help explain?`;
        }
        if (msg.includes('dbms') || msg.includes('sql') || msg.includes('database')) {
            return `🗄️ **DBMS Track Overview**:
Database Management Systems organize and protect persistent relational data.
- **Easy**: 3-tier architecture, primary/foreign keys, ER modeling, SQL DDL.
- **Medium**: SQL DML, joins (inner/left/right), aggregate functions, GROUP BY, subqueries.
- **Complex**: Functional dependencies, 1NF-BCNF normalization, ACID transactions, B+ trees.

What SQL or database question do you have?`;
        }
        if (msg.includes('dsa') || msg.includes('algorithm') || msg.includes('data structure')) {
            return `🌲 **Data Structures & Algorithms Track Overview**:
DSA enables writing computationally optimal and scalable software.
- **Easy**: Big-O notation, static/dynamic arrays, linked lists, stacks, queues, binary search.
- **Medium**: Hash tables, collision resolution, recursion, merge sort, quicksort, BSTs, heaps.
- **Complex**: AVL trees, graph BFS/DFS, Dijkstra, minimum spanning trees, and Dynamic Programming.

Ask me to break down any algorithm or data structure!`;
        }

        // 8. Honest Pedagogical Fallback
        return `That is a thoughtful inquiry, ${name}!

As an offline, client-side educational tutor, my local knowledge base currently covers:
- **Python**: Variables, OOP, Decorators, Generators, Comprehensions
- **Java**: JVM, StringBuilder, Streams, Multithreading, Interfaces
- **DBMS**: Normalization (1NF-BCNF), ACID properties, SQL Joins, B+ Trees
- **DSA**: Big-O analysis, Binary Search, Trees, Dynamic Programming

Try clicking one of the suggested prompt pills below or asking:
- *"Explain Big-O notation with simple examples"*
- *"What is the difference between 3NF and BCNF?"*
- *"How does StringBuilder improve Java performance?"*
- *"How do I unlock Level 2?"*`;
    }

    // --- Chat UI Controller ---
    function setupChatDock() {
        // Floating Widget Toggle
        const widgetBtn = document.getElementById('chatWidgetBtn');
        const widgetDock = document.getElementById('chatWidgetDock');
        const closeBtn = document.getElementById('chatWidgetCloseBtn');

        if (widgetBtn && widgetDock) {
            widgetBtn.addEventListener('click', () => {
                widgetDock.classList.toggle('open');
                if (widgetDock.classList.contains('open')) {
                    const input = widgetDock.querySelector('.chat-input');
                    if (input) input.focus();
                    scrollToBottom(widgetDock.querySelector('.chat-messages'));
                }
            });
        }

        if (closeBtn && widgetDock) {
            closeBtn.addEventListener('click', () => {
                widgetDock.classList.remove('open');
            });
        }

        // Setup engines for both dock and full page
        initChatEngine('chatWidgetDock');
        initChatEngine('fullChatPageContainer');
    }

    function initChatEngine(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const messagesEl = container.querySelector('.chat-messages');
        const inputEl = container.querySelector('.chat-input');
        const sendBtn = container.querySelector('.chat-send-btn');
        const clearBtn = container.querySelector('.chat-clear-btn');
        const subjectSelect = container.querySelector('.chat-subject-select');

        if (!messagesEl || !inputEl || !sendBtn) return;

        // Load saved chat history
        loadChatHistory(messagesEl, containerId);

        const handleSend = () => {
            const rawMsg = inputEl.value.trim();
            if (!rawMsg) return;

            inputEl.value = '';
            inputEl.disabled = true;
            sendBtn.disabled = true;

            // Render user bubble
            appendMessage(messagesEl, rawMsg, 'user');
            saveMessageToHistory(rawMsg, 'user', containerId);
            scrollToBottom(messagesEl);

            // Show typing indicator
            const typingEl = appendTypingIndicator(messagesEl);
            scrollToBottom(messagesEl);

            // Context determination
            const subjectCtx = subjectSelect ? subjectSelect.value : (container.dataset.subjectContext || '');

            // Simulate realistic cognitive delay (300-600ms)
            setTimeout(() => {
                if (typingEl) typingEl.remove();
                const botReply = generateResponse(rawMsg, subjectCtx);
                appendMessage(messagesEl, botReply, 'assistant');
                saveMessageToHistory(botReply, 'assistant', containerId);
                scrollToBottom(messagesEl);

                inputEl.disabled = false;
                sendBtn.disabled = false;
                inputEl.focus();
            }, 450);
        };

        sendBtn.addEventListener('click', handleSend);
        inputEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });

        // Clear chat button
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                if (confirm('Clear chat history for this session?')) {
                    clearChatHistory(containerId);
                    messagesEl.innerHTML = `
                        <div class="chat-bubble chat-bubble-assistant">
                            <div class="assistant-content">
                                <p class="mb-0">Chat history cleared. How can I help you today?</p>
                            </div>
                        </div>
                    `;
                }
            });
        }

        // Suggested prompt pills
        container.querySelectorAll('.chat-suggestion-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                inputEl.value = pill.textContent.trim();
                handleSend();
            });
        });
    }

    function appendMessage(container, text, role) {
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble chat-bubble-${role}`;

        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\n\n/g, '</p><p class="mb-1">')
            .replace(/\n/g, '<br>');

        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        bubble.innerHTML = `
            <div>${formatted}</div>
            <div class="chat-timestamp text-end ${role === 'user' ? 'text-white-50' : 'text-muted'}">${timeStr}</div>
        `;
        container.appendChild(bubble);
    }

    function appendTypingIndicator(container) {
        const ind = document.createElement('div');
        ind.className = 'typing-indicator';
        ind.innerHTML = '<span></span><span></span><span></span>';
        container.appendChild(ind);
        return ind;
    }

    function scrollToBottom(el) {
        if (el) el.scrollTop = el.scrollHeight;
    }

    function getHistoryKey(containerId) {
        const user = window.Auth ? window.Auth.getCurrentUser() : null;
        const email = user ? user.email.toLowerCase() : 'guest';
        return `eduadapt_chat_${containerId}_${email}`;
    }

    function saveMessageToHistory(text, role, containerId) {
        try {
            const key = getHistoryKey(containerId);
            const history = JSON.parse(localStorage.getItem(key) || '[]');
            history.push({ text, role, timestamp: new Date().toISOString() });
            if (history.length > 30) history.shift();
            localStorage.setItem(key, JSON.stringify(history));
        } catch (e) {
            console.error('Failed to save chat history', e);
        }
    }

    function loadChatHistory(container, containerId) {
        try {
            const key = getHistoryKey(containerId);
            const history = JSON.parse(localStorage.getItem(key) || '[]');
            if (history.length > 0) {
                container.innerHTML = '';
                history.forEach(item => {
                    appendMessage(container, item.text, item.role);
                });
                scrollToBottom(container);
            }
        } catch (e) {
            console.error('Failed to load chat history', e);
        }
    }

    function clearChatHistory(containerId) {
        localStorage.removeItem(getHistoryKey(containerId));
    }

    document.addEventListener('DOMContentLoaded', setupChatDock);
})();
