"""
Data Structures and Algorithms (DSA) Curriculum for EduAdapt-AI
Contains full structured content for Easy, Medium, and Complex levels.
"""

DSA_DATA = {
    'id': 'dsa',
    'title': 'Data Structures & Algorithms',
    'badge_color': 'info',
    'icon': 'bi-diagram-3',
    'short_summary': 'Master algorithmic problem solving, time complexity, trees, graphs, dynamic programming, and interview prep.',
    'description': 'A comprehensive learning path spanning asymptotic Big-O analysis, fundamental linear data structures, heaps, balanced search trees, graph algorithms, and dynamic programming optimization.',
    'difficulty': 'Beginner to Advanced',
    'levels': {
        'easy': {
            'level_number': 1,
            'name': 'Easy (Level 1 - Asymptotic Analysis & Linear Structures)',
            'description': 'Big-O notation, arrays, strings, two-pointers, singly linked lists, stacks, queues, and elementary searching and sorting.',
            'topics': [
                {
                    'id': 'dsa-big-o',
                    'title': '1. Algorithm Analysis & Big-O Asymptotic Notation',
                    'read_time': '10 min',
                    'summary': 'Quantify computational efficiency, upper bounds with Big-O, lower bounds with Omega, and tight bounds with Theta.',
                    'concept': """Algorithmic analysis evaluates how the runtime and memory requirements of an algorithm scale as the input size $n$ approaches infinity. Rather than measuring wall-clock time in seconds (which varies with hardware and OS load), computer scientists measure the number of primitive operations executed.

Asymptotic Notations:
- **Big-O ($O$)**: Mathematical upper bound (worst-case scenario). $f(n) \\in O(g(n))$ if $f(n) \\le c \\cdot g(n)$ for large $n$.
- **Big-Omega ($\\Omega$)**: Mathematical lower bound (best-case scenario).
- **Big-Theta ($\\Theta$)**: Tight bound (both upper and lower bound).

Complexity Hierarchy from Fastest to Slowest:
$O(1) < O(\\log n) < O(n) < O(n \\log n) < O(n^2) < O(2^n) < O(n!)$""",
                    'syntax': """// Constant Time: O(1)
int getFirst(int[] arr) { return arr[0]; }

// Linear Time: O(n)
for (int i = 0; i < n; i++) { ... }

// Quadratic Time: O(n^2)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) { ... }
}
""",
                    'code_example': """def analyze_time_complexities(n):
    # O(1)
    constant_val = 42

    # O(n)
    linear_ops = 0
    for i in range(n):
        linear_ops += 1

    # O(n^2)
    quadratic_ops = 0
    for i in range(n):
        for j in range(n):
            quadratic_ops += 1

    print(f"Input n = {n}")
    print(f"O(1) Operations: 1")
    print(f"O(n) Operations: {linear_ops}")
    print(f"O(n^2) Operations: {quadratic_ops}")

analyze_time_complexities(10)
""",
                    'expected_output': """Input n = 10
O(1) Operations: 1
O(n) Operations: 10
O(n^2) Operations: 100
""",
                    'common_mistakes': 'Ignoring non-dominant terms and constant factors incorrectly in small inputs, or confusing $O(\\log n)$ with $O(n)$. Binary search is $O(\\log n)$ because the search space is halved at each step.',
                    'practice_question': 'What is the time complexity of finding an element in an unsorted array of size $n$? (Answer: $O(n)$ in worst case).'
                },
                {
                    'id': 'dsa-arrays',
                    'title': '2. Static & Dynamic Arrays: Memory Layout & Amortized O(1)',
                    'read_time': '10 min',
                    'summary': 'Examine contiguous physical memory layout, index calculation formulas, and dynamic array geometric resizing.',
                    'concept': """An **Array** stores elements of identical type in contiguous physical memory addresses.
Because elements reside contiguously, the memory address of element $i$ is calculated instantaneously:
$\\text{Address}(A[i]) = \\text{BaseAddress} + (i \\times \\text{ElementSize})$
This formula grants arrays $O(1)$ constant-time random access by index!

**Dynamic Arrays** (Python `list`, Java `ArrayList`, C++ `std::vector`):
When a dynamic array exhausts its fixed capacity, it allocates a new array of double the size ($2 \\times$), copies all existing $n$ elements over, and frees the old block.
Although resizing takes $O(n)$ time, it happens rarely. Over a sequence of $n$ appends, the total copying work is $O(n)$, giving an **Amortized Constant Time** of $O(1)$ per append!""",
                    'syntax': """// Random Access: O(1)
// Append at End: O(1) Amortized
// Insertion/Deletion at Beginning: O(n) due to shifting
""",
                    'code_example': """# Dynamic array capacity growth demonstration
import sys

demo_list = []
print("Length | Byte Size in RAM")
print("-" * 25)
for i in range(10):
    demo_list.append(i)
    print(f"{len(demo_list):>6} | {sys.getsizeof(demo_list):>12} bytes")
""",
                    'expected_output': """Length | Byte Size in RAM
-------------------------
     1 |           88 bytes
     2 |           88 bytes
     3 |           88 bytes
     4 |           88 bytes
     5 |          120 bytes
     6 |          120 bytes
     7 |          120 bytes
     8 |          120 bytes
     9 |          184 bytes
    10 |          184 bytes
""",
                    'common_mistakes': 'Inserting or removing elements at index 0 of an array repeatedly inside a loop. This requires shifting all $n$ subsequent elements, turning an algorithm into $O(n^2)$.',
                    'practice_question': 'What is the amortized time complexity of appending an element to the end of a dynamic array? (Answer: $O(1)$ amortized).'
                },
                {
                    'id': 'dsa-two-pointers',
                    'title': '3. Strings & the Two-Pointer Technique',
                    'read_time': '10 min',
                    'summary': 'Solve array and string problems in O(n) time and O(1) space using opposing and fast-slow pointer patterns.',
                    'concept': """The **Two-Pointer Technique** iterates through a sequence using two index references simultaneously to reduce $O(n^2)$ brute-force solutions to optimal $O(n)$ linear time.

Common Patterns:
1. **Opposing Pointers**: One pointer starts at index `0` (left) and the other at `len - 1` (right), moving towards each other until they meet (e.g. palindrome check, two-sum on sorted array, array reversal).
2. **Fast & Slow Pointers**: Both start at the beginning, but move at different velocities (e.g. removing duplicates in-place, finding the midpoint of a linked list, cycle detection).""",
                    'syntax': """left, right = 0, len(arr) - 1
while left < right:
    if condition:
        left += 1
    else:
        right -= 1
""",
                    'code_example': """def is_palindrome(s):
    # Clean text: keep only alphanumeric characters, lowercased
    cleaned = [c.lower() for c in s if c.isalnum()]
    
    left, right = 0, len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True

test_cases = ["A man, a plan, a canal: Panama", "EduAdapt AI", "racecar"]
for t in test_cases:
    print(f"'{t}' is palindrome? {is_palindrome(t)}")
""",
                    'expected_output': """'A man, a plan, a canal: Panama' is palindrome? True
'EduAdapt AI' is palindrome? False
'racecar' is palindrome? True
""",
                    'common_mistakes': 'Allowing the two pointers to cross each other (`left <= right` instead of `left < right`), causing index out-of-bounds or redundant comparisons.',
                    'practice_question': 'What is the time and space complexity of checking a palindrome of length $n$ using two opposing pointers? (Answer: $O(n)$ time and $O(1)$ auxiliary space).'
                },
                {
                    'id': 'dsa-linked-lists',
                    'title': '4. Singly Linked Lists: Nodes & Pointer Manipulation',
                    'read_time': '11 min',
                    'summary': 'Construct dynamic node chains with next pointers, implement head insertions, and reverse a list in O(n) time.',
                    'concept': """A **Linked List** is a linear collection of data elements called **Nodes**. Unlike arrays, nodes are not stored in contiguous memory; each node contains:
1. `data`: The payload value.
2. `next`: A reference (pointer) to the subsequent node in the chain.

Trade-offs vs Arrays:
- Insertion/Deletion at head is $O(1)$ without shifting remaining elements.
- Random access by index is $O(n)$ because the chain must be traversed sequentially from the `head`.
- Extra memory overhead for pointer storage.""",
                    'syntax': """class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
""",
                    'code_example': """class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, val):
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self):
        res, curr = [], self.head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res

ll = SinglyLinkedList()
for v in [30, 20, 10]:
    ll.insert_at_head(v)

print("Original Linked List:", ll.to_list())
ll.reverse()
print("Reversed Linked List:", ll.to_list())
""",
                    'expected_output': """Original Linked List: [10, 20, 30]
Reversed Linked List: [30, 20, 10]
""",
                    'common_mistakes': 'Losing the reference to the rest of the list during pointer reassignments (`curr.next = prev` before saving `next_node = curr.next`), causing the remaining nodes to be lost in garbage collection.',
                    'practice_question': 'What is the time complexity to insert a node at the head of a Singly Linked List? (Answer: $O(1)$ constant time).'
                },
                {
                    'id': 'dsa-stacks',
                    'title': '5. Stacks: LIFO Principle & Array Implementations',
                    'read_time': '10 min',
                    'summary': 'Master the Last-In First-Out (LIFO) discipline, push, pop, peek, and call-stack frame simulation.',
                    'concept': """A **Stack** is a restricted linear data structure following the **Last-In, First-Out (LIFO)** principle: the most recently inserted item is the first one removed.

Fundamental Operations (all strictly $O(1)$):
- `push(x)`: Adds item $x$ to the top of the stack.
- `pop()`: Removes and returns the top item from the stack. Raises stack underflow if empty.
- `peek()` / `top()`: Inspects the top item without removing it.
- `isEmpty()`: Checks if the stack contains zero elements.

Common Uses: Function call stack execution, undo/redo mechanisms, browser back button history, syntax parsing, and depth-first search.""",
                    'syntax': """class Stack:
    def push(self, item): ...
    def pop(self): ...
    def peek(self): ...
""",
                    'code_example': """class Stack:
    def __init__(self):
        self.items = []

    def push(self, val):
        self.items.append(val)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        return len(self.items) == 0

s = Stack()
s.push("Page A: Dashboard")
s.push("Page B: Python Easy")
s.push("Page C: Quiz 1")

print("Current active page:", s.peek())
print("User clicked Back button:", s.pop())
print("Now on page:", s.peek())
""",
                    'expected_output': """Current active page: Page C: Quiz 1
User clicked Back button: Page C: Quiz 1
Now on page: Page B: Python Easy
""",
                    'common_mistakes': 'Calling `pop()` on an empty stack without checking `is_empty()`, triggering an uncaught underflow exception.',
                    'practice_question': 'Which abstract data structure operates on a Last-In, First-Out (LIFO) order? (Answer: Stack).'
                },
                {
                    'id': 'dsa-queues',
                    'title': '6. Queues: FIFO Principle & Circular Queue Design',
                    'read_time': '10 min',
                    'summary': 'Master First-In First-Out (FIFO) mechanics, enqueue, dequeue, and modulo-based circular queue buffers.',
                    'concept': """A **Queue** is a linear data structure operating on the **First-In, First-Out (FIFO)** discipline: elements are inserted at the back (`rear`) and removed from the front (`head`).

Operations:
- `enqueue(x)`: Adds item to the rear ($O(1)$).
- `dequeue()`: Removes and returns item from front ($O(1)$).
- `front()`: Inspects the front item.

**Circular Queue**:
In a naive array-based queue, dequeueing leaves empty slots at the front that cannot be reused. A circular queue wraps indices around using modulo arithmetic:
$\\text{new\\_index} = (\\text{index} + 1) \\% \\text{capacity}$
This allows continuous memory reuse in a fixed-size buffer without shifting elements!""",
                    'syntax': """rear = (rear + 1) % capacity
front = (front + 1) % capacity
""",
                    'code_example': """class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def enqueue(self, val):
        if self.size == self.capacity:
            raise OverflowError("Queue is full")
        self.queue[self.tail] = val
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise IndexError("Queue is empty")
        item = self.queue[self.head]
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item

cq = CircularQueue(3)
cq.enqueue("Student-1")
cq.enqueue("Student-2")
print("Processed:", cq.dequeue())
cq.enqueue("Student-3")
cq.enqueue("Student-4")  # Reuses wrapped slot!
print("Processed:", cq.dequeue())
""",
                    'expected_output': """Processed: Student-1
Processed: Student-2
""",
                    'common_mistakes': 'Implementing a queue using a Python `list` with `list.pop(0)`. Deleting from index 0 shifts all remaining elements, making dequeue an inefficient $O(n)$ operation instead of $O(1)$. Use `collections.deque`.',
                    'practice_question': 'What mathematical operator enables index wrap-around in a circular queue? (Answer: The modulo operator `%`).'
                },
                {
                    'id': 'dsa-searching',
                    'title': '7. Searching: Linear Search vs Binary Search',
                    'read_time': '10 min',
                    'summary': 'Compare O(n) sequential scanning with O(log n) logarithmic binary search on sorted intervals.',
                    'concept': """Searching algorithms locate the position of a target value within a collection:
1. **Linear Search**: Checks every element sequentially from index 0 to $n-1$. Works on unsorted collections.
   - Best Case: $O(1)$ (target at index 0)
   - Worst & Average Case: $O(n)$
2. **Binary Search**: Requires the collection to be **SORTED**. Divides the search interval in half each iteration by comparing the target with the median element.
   - Time Complexity: $O(\\log n)$
   - Search Space Reduction: $n \\rightarrow n/2 \\rightarrow n/4 \\dots \\rightarrow 1$ (at most $\\lfloor \\log_2 n \\rfloor + 1$ comparisons).""",
                    'syntax': """def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: low = mid + 1
        else: high = mid - 1
    return -1
""",
                    'code_example': """def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    steps = 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, steps

dataset = [11, 23, 35, 47, 52, 68, 74, 89, 93, 105, 120, 145, 180, 200, 250, 300]
target = 145
idx, comp_count = binary_search(dataset, target)
print(f"Target {target} located at index {idx} in only {comp_count} comparisons across {len(dataset)} items!")
""",
                    'expected_output': """Target 145 located at index 11 in only 3 comparisons across 16 items!
""",
                    'common_mistakes': 'Calculating midpoint using `(low + high) / 2` in languages like C/Java where `low + high` can overflow the 32-bit integer range. Use `low + (high - low) / 2`.',
                    'practice_question': 'What prerequisite must a collection satisfy before Binary Search can be applied? (Answer: The collection must be sorted).'
                },
                {
                    'id': 'dsa-sorting-bubble-selection',
                    'title': '8. Elementary Sorting: Bubble Sort & Selection Sort',
                    'read_time': '10 min',
                    'summary': 'Understand adjacent pair swapping in Bubble Sort and minimum-element extraction in Selection Sort.',
                    'concept': """Elementary sorting algorithms demonstrate fundamental comparison mechanisms:
1. **Bubble Sort**: Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. With an early termination flag, best-case is $O(n)$ when already sorted; worst-case is $O(n^2)$. Stable sort.
2. **Selection Sort**: Divides the list into a sorted sublist at the left and an unsorted sublist at the right. Repeatedly finds the minimum element from the unsorted sublist and swaps it with the first unsorted position.
   - Always $O(n^2)$ comparisons regardless of initial array ordering.
   - Makes at most $O(n)$ swaps (useful when writes to memory are very expensive). Unstable sort.""",
                    'syntax': """# Selection sort inner loop finds min_idx, then swaps:
arr[i], arr[min_idx] = arr[min_idx], arr[i]
""",
                    'code_example': """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

sample = [64, 25, 12, 22, 11]
sorted_arr = bubble_sort(sample.copy())
print("Bubble Sorted Array:", sorted_arr)
""",
                    'expected_output': """Bubble Sorted Array: [11, 12, 22, 25, 64]
""",
                    'common_mistakes': 'Assuming Selection Sort is stable. Equal elements can have their relative order swapped when the minimum is moved past them.',
                    'practice_question': 'What is the maximum number of swap operations performed by Selection Sort on an array of $n$ elements? (Answer: At most $n-1$ or $O(n)$ swaps).'
                },
                {
                    'id': 'dsa-sorting-insertion',
                    'title': '9. Elementary Sorting: Insertion Sort & Invariant Proofs',
                    'read_time': '10 min',
                    'summary': 'Build sorted prefixes with Insertion Sort, adaptive O(n) performance on nearly-sorted data, and stability.',
                    'concept': """**Insertion Sort** constructs the final sorted array one item at a time. It iterates through the input elements, growing a sorted sub-array behind the current element by shifting larger elements one position to the right.

Characteristics:
- **Loop Invariant**: At the start of iteration $i$, sub-array $A[0 \\dots i-1]$ contains the sorted elements originally in those positions.
- **Adaptive**: Runs in $O(n)$ linear time if the input array is already sorted or nearly sorted!
- **Space**: $O(1)$ auxiliary memory (in-place).
- **Stable**: Preserves the original relative order of equal elements.
- Serves as the base-case sort in production hybrid algorithms like Timsort (used by Python and Java) for small sub-arrays ($n \\le 32$ or $64$).""",
                    'syntax': """for i in range(1, len(arr)):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key
""",
                    'code_example': """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift elements greater than key to one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

scores = [88, 70, 95, 62, 81]
print("Before:", scores)
print("After Insertion Sort:", insertion_sort(scores))
""",
                    'expected_output': """Before: [88, 70, 95, 62, 81]
After Insertion Sort: [62, 70, 81, 88, 95]
""",
                    'common_mistakes': 'Overwriting the key value before shifting elements. The current element must be stored in a temporary `key` variable.',
                    'practice_question': 'What is the best-case time complexity of Insertion Sort when the input array is already sorted? (Answer: $O(n)$ linear time).'
                }
            ]
        },
        'medium': {
            'level_number': 2,
            'name': 'Medium (Level 2 - Trees, Hashing & Divide-and-Conquer)',
            'description': 'Doubly linked lists, hashing, divide-and-conquer, merge sort, quicksort, binary trees, BSTs, and heaps.',
            'topics': [
                {
                    'id': 'dsa-doubly-linked-lists',
                    'title': '1. Doubly Linked Lists & Sentinel Nodes',
                    'read_time': '10 min',
                    'summary': 'Bidirectional node traversal with next and prev pointers, and simplifying edge cases with sentinel dummy nodes.',
                    'concept': """A **Doubly Linked List (DLL)** extends singly linked lists by storing two pointers per node:
1. `next`: Reference to the successor node.
2. `prev`: Reference to the predecessor node.

Advantages:
- Can be traversed both forward and backward.
- Deletion of a given node $N$ can be performed in $O(1)$ time without traversing from the head (because $N$ already possesses a pointer to its predecessor: `node.prev.next = node.next`).
- Ideal foundation for LRU (Least Recently Used) cache structures combined with hash tables.

**Sentinel (Dummy) Nodes**:
Introducing fixed dummy `head` and `tail` nodes eliminates tedious null checks when inserting or deleting at list boundaries.""",
                    'syntax': """class DLNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None
""",
                    'code_example': """class DoublyLinkedList:
    def __init__(self):
        # Sentinel boundaries
        self.head = DLNode(0)
        self.tail = DLNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_first(self, val):
        node = DLNode(val)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

dll = DoublyLinkedList()
dll.add_first(10)
dll.add_first(20)
print("First node value:", dll.head.next.val)
print("Second node value:", dll.head.next.next.val)
""",
                    'expected_output': """First node value: 20
Second node value: 10
""",
                    'common_mistakes': 'Updating pointer `node.next.prev` without checking whether `node.next` is null, causing `NullPointerException`.',
                    'practice_question': 'What is the time complexity to delete a node from a Doubly Linked List if a pointer to that node is already provided? (Answer: $O(1)$ constant time).'
                },
                {
                    'id': 'dsa-stack-parsing',
                    'title': '2. Stack Applications: Parentheses Matching & Expressions',
                    'read_time': '11 min',
                    'summary': 'Parse structured syntax, validate matching brackets (), [], {}, and evaluate postfix expressions with stacks.',
                    'concept': """Stacks naturally validate nested hierarchical structures and syntactic expressions.

1. **Balanced Parentheses Matching**:
   - Iterate through the string character by character.
   - When encountering an opening bracket `(`, `[`, `{`, push it onto the stack.
   - When encountering a closing bracket, pop from the stack and verify that the popped bracket matches the closing counterpart.
   - If the stack is empty on closing or non-empty at string termination, the expression is unbalanced.

2. **Postfix (Reverse Polish) Evaluation**:
   - Operands are pushed onto the stack.
   - When an operator is encountered, pop the top two operands, evaluate the arithmetic, and push the result back onto the stack.""",
                    'syntax': """bracket_map = {')': '(', '}': '{', ']': '['}
""",
                    'code_example': """def is_balanced(expression):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in expression:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack.pop() != mapping[char]:
                return False
    return len(stack) == 0

exprs = ["{ [ a * (b + c) ] }", "( ( a + b )", "{ [ } ]"]
for e in exprs:
    print(f"'{e}' balanced? {is_balanced(e)}")
""",
                    'expected_output': """'{ [ a * (b + c) ] }' balanced? True
'( ( a + b )' balanced? False
'{ [ } ]' balanced? False
""",
                    'common_mistakes': 'Returning `True` when the string ends without checking `len(stack) == 0`. Unmatched opening brackets left on the stack make an expression invalid.',
                    'practice_question': 'In evaluating a postfix expression `5 3 + 2 *`, what is the final calculated value? (Answer: $(5+3) \\times 2 = 16$).'
                },
                {
                    'id': 'dsa-hash-tables',
                    'title': '3. Hash Tables & Collision Resolution Strategies',
                    'read_time': '12 min',
                    'summary': 'Understand hash functions, load factor, separate chaining (linked lists), and open addressing (linear probing).',
                    'concept': """A **Hash Table** maps keys to values using a **Hash Function** $h(k)$ that calculates an integer bucket index: $\\text{index} = h(k) \\% \\text{table\\_size}$.

When two distinct keys produce the identical hash index, a **Collision** occurs.
Collision Resolution Methods:
1. **Separate Chaining**: Each bucket contains a linked list of entries that hashed to that index.
2. **Open Addressing**: All elements reside directly in the table array. On collision, probe for the next open slot:
   - Linear Probing: $h(k, i) = (h(k) + i) \\% m$ (prone to primary clustering).
   - Quadratic Probing: $h(k, i) = (h(k) + c_1 i + c_2 i^2) \\% m$.
   - Double Hashing: Uses a secondary hash function $h_2(k)$.

**Load Factor ($\\alpha$)**: $\\alpha = n / m$ (number of items / table capacity). When $\\alpha$ exceeds a threshold (typically 0.75), the table rehashes into an array of double capacity.""",
                    'syntax': """bucket_index = hash(key) % capacity
""",
                    'code_example': """class SimpleHashTable:
    def __init__(self, size=7):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def put(self, key, value):
        idx = self._hash(key)
        for pair in self.buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self.buckets[idx].append([key, value])

    def get(self, key):
        idx = self._hash(key)
        for pair in self.buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return None

ht = SimpleHashTable()
ht.put("Python", 95)
ht.put("Java", 88)
print("Retrieved 'Python':", ht.get("Python"))
print("Retrieved 'Java':", ht.get("Java"))
""",
                    'expected_output': """Retrieved 'Python': 95
Retrieved 'Java': 88
""",
                    'common_mistakes': 'Neglecting to implement tombstone markers when deleting keys in open addressing, which prematurely halts subsequent lookups during linear probing.',
                    'practice_question': 'What is the average time complexity of key lookup in a well-distributed hash table? (Answer: $O(1)$ constant time).'
                },
                {
                    'id': 'dsa-divide-and-conquer',
                    'title': '4. Recursion Trees & the Master Theorem',
                    'read_time': '11 min',
                    'summary': 'Solve divide-and-conquer recurrence relations $T(n) = aT(n/b) + f(n)$ using the Master Theorem.',
                    'concept': """The Divide-and-Conquer paradigm breaks a problem into smaller subproblems of the same type, solves them recursively, and combines the subproblem results.

**The Master Theorem**:
For recurrences of the form:
$T(n) = a T(n/b) + f(n)$, where $a \\ge 1, b > 1$:
Let $c_{crit} = \\log_b a$.
1. If $f(n) \\in O(n^c)$ where $c < c_{crit}$: $T(n) \\in \\Theta(n^{\\log_b a})$ (Tree leaves dominate).
2. If $f(n) \\in \\Theta(n^{c_{crit}} \\log^k n)$: $T(n) \\in \\Theta(n^{\\log_b a} \\log^{k+1} n)$ (Work evenly distributed across tree levels).
   - For Merge Sort: $T(n) = 2T(n/2) + O(n) \\Rightarrow a=2, b=2, c=1 \\Rightarrow \\log_2 2 = 1 = c \\Rightarrow \\Theta(n \\log n)$.
3. If $f(n) \\in \\Omega(n^c)$ where $c > c_{crit}$: $T(n) \\in \\Theta(f(n))$ (Tree root dominates).""",
                    'syntax': """// Merge Sort: T(n) = 2T(n/2) + O(n) -> O(n log n)
// Binary Search: T(n) = T(n/2) + O(1) -> O(log n)
""",
                    'code_example': """# Tabulating recurrence tree node expansion
def print_recurrence_tree(n, depth=0):
    if n < 1:
        return
    indent = "  " * depth
    print(f"{indent}Subproblem Size: {n}")
    if n > 1:
        print_recurrence_tree(n // 2, depth + 1)
        print_recurrence_tree(n // 2, depth + 1)

print("Merge Sort Recurrence Tree (n = 4):")
print_recurrence_tree(4)
""",
                    'expected_output': """Merge Sort Recurrence Tree (n = 4):
Subproblem Size: 4
  Subproblem Size: 2
    Subproblem Size: 1
    Subproblem Size: 1
  Subproblem Size: 2
    Subproblem Size: 1
    Subproblem Size: 1
""",
                    'common_mistakes': 'Applying the Master Theorem to recurrences where subproblem sizes are asymmetric (e.g. $T(n) = T(n-1) + O(1)$). Use substitution or iteration methods instead.',
                    'practice_question': 'According to the Master Theorem, what is the asymptotic runtime of $T(n) = 2T(n/2) + O(n)$? (Answer: $\\Theta(n \\log n)$).'
                },
                {
                    'id': 'dsa-merge-sort',
                    'title': '5. Merge Sort: Divide, Conquer & Stability',
                    'read_time': '11 min',
                    'summary': 'Implement recursive two-way merge sort, prove O(n log n) worst-case time, and analyze O(n) auxiliary space.',
                    'concept': """**Merge Sort** is an optimal, comparison-based, divide-and-conquer sorting algorithm.

Algorithm Workflow:
1. **Divide**: Find the midpoint $m = \\lfloor (l + r) / 2 \\rfloor$ and split the array into two halves.
2. **Conquer**: Recursively sort each half until sub-arrays reach base case length 1.
3. **Combine**: Merge the two sorted halves into a single sorted array using two pointers.

Properties:
- **Time Complexity**: $\\Theta(n \\log n)$ guaranteed across worst, average, and best cases!
- **Space Complexity**: $O(n)$ auxiliary array memory needed for merging.
- **Stability**: Stable (preserves original order of equal items by preferring elements from the left sub-array when equal: `<=`).""",
                    'syntax': """def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
""",
                    'code_example': """def merge(left, right):
    sorted_merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_merged.append(left[i])
            i += 1
        else:
            sorted_merged.append(right[j])
            j += 1
    sorted_merged.extend(left[i:])
    sorted_merged.extend(right[j:])
    return sorted_merged

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

data = [38, 27, 43, 3, 9, 82, 10]
print("Sorted with Merge Sort:", merge_sort(data))
""",
                    'expected_output': """Sorted with Merge Sort: [3, 9, 10, 27, 38, 43, 82]
""",
                    'common_mistakes': 'Assuming standard array-based Merge Sort sorts in-place. Merge Sort requires $O(n)$ auxiliary memory to merge elements safely without overwriting data.',
                    'practice_question': 'What is the worst-case time complexity of Merge Sort? (Answer: $O(n \\log n)$).'
                },
                {
                    'id': 'dsa-quick-sort',
                    'title': '6. Quick Sort: Partitioning Schemes & In-Place Sorting',
                    'read_time': '12 min',
                    'summary': 'Master pivot selection, Lomuto vs Hoare partitioning, randomized pivots, and avoid O(n^2) worst case.',
                    'concept': """**Quick Sort** is an in-place, divide-and-conquer sorting algorithm. Unlike Merge Sort which does work during the combine phase, Quick Sort does its heavy computational work in the **Partition** phase.

Algorithm:
1. Select an element as the **Pivot**.
2. **Partition**: Rearrange the array so that all elements smaller than the pivot are placed to its left, and all elements larger are placed to its right. The pivot is now at its exact final sorted position!
3. Recursively sort the sub-arrays to the left and right of the pivot.

Complexity:
- Average Time: $O(n \\log n)$ with small constant factors.
- Worst Case Time: $O(n^2)$ (occurs when the pivot is always the smallest or largest element, e.g. on already-sorted data with naive first/last pivot selection).
- Solution: Use randomized pivots or median-of-three pivot selection!""",
                    'syntax': """def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
""",
                    'code_example': """def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

arr = [10, 80, 30, 90, 40, 50, 70]
quick_sort(arr, 0, len(arr) - 1)
print("Quick Sorted Array:", arr)
""",
                    'expected_output': """Quick Sorted Array: [10, 30, 40, 50, 70, 80, 90]
""",
                    'common_mistakes': 'Always picking the first element as the pivot. If an array is already sorted, this produces an unbalanced partition of sizes 0 and $n-1$, degrading runtime to $O(n^2)$.',
                    'practice_question': 'What strategy prevents Quick Sort from degrading to $O(n^2)$ time on already-sorted input? (Answer: Randomized pivot selection or Median-of-Three pivot selection).'
                },
                {
                    'id': 'dsa-binary-trees',
                    'title': '7. Binary Trees: Depth-First Traversals (Inorder, Preorder, Postorder)',
                    'read_time': '11 min',
                    'summary': 'Traverse hierarchical node structures using recursive and iterative DFS traversal orders.',
                    'concept': """A **Binary Tree** is a non-linear hierarchical data structure in which each node has at most two children, referred to as the `left` child and `right` child.

Tree Metrics:
- **Depth of a Node**: Number of edges from the root to the node.
- **Height of a Tree**: Number of edges on the longest path from the root to a leaf node.

Depth-First Traversals:
1. **Preorder (Root, Left, Right)**: Useful for cloning or serializing a tree.
2. **Inorder (Left, Root, Right)**: In a Binary Search Tree, visits all nodes in non-decreasing sorted order!
3. **Postorder (Left, Right, Root)**: Useful for bottom-up deletions and directory space calculations.""",
                    'syntax': """def inorder(root):
    if root:
        inorder(root.left)
        visit(root.val)
        inorder(root.right)
""",
                    'code_example': """class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# Construct tree:
#       1
#      / \\
#     2   3
#    / \\
#   4   5
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

def dfs_traversals(node, order):
    res = []
    def traverse(curr):
        if not curr: return
        if order == "pre": res.append(curr.val)
        traverse(curr.left)
        if order == "in": res.append(curr.val)
        traverse(curr.right)
        if order == "post": res.append(curr.val)
    traverse(node)
    return res

print("Preorder Traversal: ", dfs_traversals(root, "pre"))
print("Inorder Traversal:  ", dfs_traversals(root, "in"))
print("Postorder Traversal:", dfs_traversals(root, "post"))
""",
                    'expected_output': """Preorder Traversal:  [1, 2, 4, 5, 3]
Inorder Traversal:   [4, 2, 5, 1, 3]
Postorder Traversal: [4, 5, 2, 3, 1]
""",
                    'common_mistakes': 'Confusing tree height with node depth. Depth measures distance from root downward; height measures distance from a node to its farthest descendant leaf.',
                    'practice_question': 'Which traversal of a Binary Search Tree (BST) produces nodes in ascending sorted order? (Answer: Inorder traversal).'
                },
                {
                    'id': 'dsa-bst',
                    'title': '8. Binary Search Trees (BST): Insert, Search & Deletion',
                    'read_time': '12 min',
                    'summary': 'Enforce BST invariant (Left < Node < Right), implement binary search branching, and handle 3-case node deletions.',
                    'concept': """A **Binary Search Tree (BST)** is a binary tree satisfying the **BST Invariant**:
For every node $X$:
- All keys in the left subtree of $X$ are strictly less than $X.\\text{key}$.
- All keys in the right subtree of $X$ are strictly greater than $X.\\text{key}$.

Operations:
- **Search & Insert**: $O(h)$ where $h$ is tree height ($O(\\log n)$ when balanced, $O(n)$ if degenerated into a linked list).
- **Deletion (3 Cases)**:
  1. Node is a leaf: Simply remove it.
  2. Node has one child: Replace node with its single child.
  3. Node has two children: Replace node value with its **Inorder Successor** (smallest node in the right subtree), then delete that successor from the right subtree.""",
                    'syntax': """if val < node.val: node.left = insert(node.left, val)
elif val > node.val: node.right = insert(node.right, val)
""",
                    'code_example': """class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def bst_insert(root, val):
    if not root:
        return BSTNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    elif val > root.val:
        root.right = bst_insert(root.right, val)
    return root

def bst_search(root, target):
    if not root or root.val == target:
        return root is not None
    if target < root.val:
        return bst_search(root.left, target)
    return bst_search(root.right, target)

# Build BST
tree = None
for score in [50, 30, 70, 20, 40, 60, 80]:
    tree = bst_insert(tree, score)

print("Is 60 in BST?", bst_search(tree, 60))
print("Is 95 in BST?", bst_search(tree, 95))
""",
                    'expected_output': """Is 60 in BST? True
Is 95 in BST? False
""",
                    'common_mistakes': 'Deleting a node with two children by directly detaching its children, which severs entire subtrees. You must substitute the inorder successor or inorder predecessor.',
                    'practice_question': 'What is the worst-case search complexity in an unbalanced Binary Search Tree of $n$ elements? (Answer: $O(n)$, occurring when nodes are inserted in already-sorted order).'
                },
                {
                    'id': 'dsa-heaps',
                    'title': '9. Priority Queues & Binary Heaps: Heapify & Sifting',
                    'read_time': '12 min',
                    'summary': 'Implement complete binary tree arrays, Max-Heap and Min-Heap invariants, sift-up/down, and O(n) heapify.',
                    'concept': """A **Binary Heap** is a complete binary tree implemented efficiently within a contiguous array without node pointers.
Array Index Mapping (for zero-indexed array):
- Parent of $i$: $\\lfloor (i - 1) / 2 \\rfloor$
- Left Child of $i$: $2i + 1$
- Right Child of $i$: $2i + 2$

Heap Invariant:
- **Min-Heap**: Value of each node is $\\le$ values of its children ($A[\\text{parent}] \\le A[i]$). The minimum element is always at index 0!
- **Max-Heap**: Value of each node is $\\ge$ values of its children.

Operations:
- `insert()`: Appends at the end of the array, then **Sifts-Up** ($O(\\log n)$).
- `extract_min()`: Replaces root with last element, pops last element, then **Sifts-Down** ($O(\\log n)$).
- `build_heap()` (Heapify): Bottom-up sifting runs in mathematically linear $O(n)$ time!""",
                    'syntax': """import heapq
heap = []
heapq.heappush(heap, 10)
min_val = heapq.heappop(heap)
""",
                    'code_example': """import heapq

# Priority Queue tracking lowest scores requiring review
priority_queue = []
student_scores = [(85, "Marcus"), (62, "Liam"), (94, "Elena"), (71, "Maya")]

for score, name in student_scores:
    heapq.heappush(priority_queue, (score, name))

print("Priority Queue (Min-Heap) order of tutoring intervention:")
while priority_queue:
    score, name = heapq.heappop(priority_queue)
    print(f" - Tutoring assigned to: {name} (Score: {score}%)")
""",
                    'expected_output': """Priority Queue (Min-Heap) order of tutoring intervention:
 - Tutoring assigned to: Liam (Score: 62%)
 - Tutoring assigned to: Maya (Score: 71%)
 - Tutoring assigned to: Marcus (Score: 85%)
 - Tutoring assigned to: Elena (Score: 94%)
""",
                    'common_mistakes': 'Assuming building a heap of $n$ elements requires $O(n \\log n)$ time. Running Floyd\'s bottom-up `heapify` on an arbitrary array runs in $O(n)$ time.',
                    'practice_question': 'Given a zero-indexed binary heap array, what is the index of the parent of the node at index $i$? (Answer: $\\lfloor (i - 1) / 2 \\rfloor$).'
                }
            ]
        },
        'complex': {
            'level_number': 3,
            'name': 'Complex (Level 3 - Graphs, Dynamic Programming & Advanced Algorithms)',
            'description': 'Balanced AVL trees, graph representations, BFS/DFS, Dijkstra, MST, greedy algorithms, 0/1 knapsack, LCS, and backtracking.',
            'topics': [
                {
                    'id': 'dsa-avl-trees',
                    'title': '1. Balanced Trees: AVL Tree Rotations (LL, RR, LR, RL)',
                    'read_time': '13 min',
                    'summary': 'Maintain strict height balance factor $\\in \\{-1, 0, 1\\}$ using single and double tree rotations.',
                    'concept': """An **AVL Tree** (named after Adelson-Velsky and Landis) is a self-balancing Binary Search Tree.
**Balance Factor (BF)**:
$\\text{BF}(\\text{node}) = \\text{Height}(\\text{left\\_subtree}) - \\text{Height}(\\text{right\\_subtree})$
Invariant: For every node in an AVL tree, $\\text{BF} \\in \\{-1, 0, 1\\}$.
If an insertion or deletion causes $\\text{BF}$ to become $\\pm 2$, a rotation restores balance in $O(1)$ time.

Four Rotation Cases:
1. **Left-Left (LL)**: Unbalance caused by insertion into left subtree of left child $\\rightarrow$ Single Right Rotation.
2. **Right-Right (RR)**: Unbalance in right subtree of right child $\\rightarrow$ Single Left Rotation.
3. **Left-Right (LR)**: Left child has positive/negative skew $\\rightarrow$ Left rotation on left child, then Right rotation on root.
4. **Right-Left (RL)**: Right child has opposite skew $\\rightarrow$ Right rotation on right child, then Left rotation on root.""",
                    'syntax': """// Right Rotation on node y:
Node x = y.left;
y.left = x.right;
x.right = y;
""",
                    'code_example': """class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    return node.height if node else 0

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

# Testing rotation on unbalanced chain 30 -> 20 -> 10
root = AVLNode(30)
root.left = AVLNode(20)
root.left.left = AVLNode(10)
root.height = 3
root.left.height = 2

print("Pre-rotation Balance Factor at Root:", get_balance(root))
balanced_root = right_rotate(root)
print("Post-rotation New Root:", balanced_root.key)
print("Left Child:", balanced_root.left.key, "| Right Child:", balanced_root.right.key)
print("New Root Balance Factor:", get_balance(balanced_root))
""",
                    'expected_output': """Pre-rotation Balance Factor at Root: 2
Post-rotation New Root: 20
Left Child: 10 | Right Child: 30
New Root Balance Factor: 0
""",
                    'common_mistakes': 'Failing to update node height values after rotations, which leads to incorrect balance factors on subsequent operations.',
                    'practice_question': 'What rotation is applied to fix an AVL tree Left-Right (LR) imbalance? (Answer: A Left rotation on the left child, followed by a Right rotation on the unbalanced parent).'
                },
                {
                    'id': 'dsa-graphs-representations',
                    'title': '2. Graph Representations: Adjacency Matrix vs Adjacency List',
                    'read_time': '11 min',
                    'summary': 'Model networks, vertices, edges, and evaluate space/time trade-offs between Matrix ($V^2$) and List ($V + E$).',
                    'concept': """A **Graph** $G = (V, E)$ consists of a set of Vertices $V$ and Edges $E$ connecting pairs of vertices. Graphs may be directed or undirected, weighted or unweighted.

Representations:
1. **Adjacency Matrix**: A $2D$ array of size $|V| \\times |V|$ where `matrix[u][v]` indicates whether an edge exists between vertex $u$ and $v$.
   - Space: $O(V^2)$ (wastes memory for sparse graphs where $E \\ll V^2$).
   - Edge lookup $(u, v)$: $O(1)$.
   - Iterate neighbors of $u$: $O(V)$.
2. **Adjacency List**: An array of lists where `adj[u]` stores all neighbors of vertex $u$.
   - Space: $O(V + E)$ (optimal for sparse graphs).
   - Iterate neighbors: $O(\\text{degree}(u))$.""",
                    'syntax': """# Adjacency List using dict of lists
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}
""",
                    'code_example': """class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = {v: [] for v in vertices}

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight)) # Undirected

g = Graph(["Python", "DSA", "DBMS", "Java"])
g.add_edge("Python", "DSA")
g.add_edge("DSA", "DBMS")
g.add_edge("Python", "DBMS")

for node, neighbors in g.adj.items():
    print(f"Node '{node}' connected to:", [target for target, _ in neighbors])
""",
                    'expected_output': """Node 'Python' connected to: ['DSA', 'DBMS']
Node 'DSA' connected to: ['Python', 'DBMS']
Node 'DBMS' connected to: ['DSA', 'Python']
Node 'Java' connected to: []
""",
                    'common_mistakes': 'Using an Adjacency Matrix for a graph with 1,000,000 vertices. A matrix would require $10^{12}$ cells (~1 Terabyte of RAM), whereas an Adjacency List uses minimal memory.',
                    'practice_question': 'What is the space complexity of an Adjacency List representation of a graph with $V$ vertices and $E$ edges? (Answer: $O(V + E)$).'
                },
                {
                    'id': 'dsa-graph-traversals',
                    'title': '3. Graph Traversals: Breadth-First Search (BFS) & Depth-First Search (DFS)',
                    'read_time': '12 min',
                    'summary': 'Traverse graphs using queues for shortest unweighted paths (BFS) and stacks/recursion for cycles/components (DFS).',
                    'concept': """Graph traversal explores all reachable vertices from a source vertex while tracking a `visited` set to avoid infinite loops caused by cycles.

1. **Breadth-First Search (BFS)**:
   - Uses a **Queue** (FIFO). Explores vertices level-by-level in expanding concentric rings.
   - **Guarantees the shortest path** in an unweighted graph!
   - Time: $O(V + E)$, Space: $O(V)$.

2. **Depth-First Search (DFS)**:
   - Uses a **Stack** or recursion. Plunges as deeply as possible along each branch before backtracking.
   - Applications: Topological sorting, cycle detection, strongly connected components (Kosaraju/Tarjan).
   - Time: $O(V + E)$, Space: $O(V)$.""",
                    'syntax': """# BFS queue traversal
queue.append(start); visited.add(start)
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited: ...
""",
                    'code_example': """from collections import deque

def bfs_shortest_path(graph, start, target):
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == target:
            return path
            
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

curriculum_graph = {
    "Python_Basics": ["OOP", "Data_Structures"],
    "OOP": ["Design_Patterns", "Web_Dev"],
    "Data_Structures": ["Algorithms", "Web_Dev"],
    "Algorithms": ["Machine_Learning"],
    "Machine_Learning": []
}

path = bfs_shortest_path(curriculum_graph, "Python_Basics", "Machine_Learning")
print("Shortest Prerequisite Pathway:", " -> ".join(path))
""",
                    'expected_output': """Shortest Prerequisite Pathway: Python_Basics -> Data_Structures -> Algorithms -> Machine_Learning
""",
                    'common_mistakes': 'Marking a vertex as visited when it is popped from the queue rather than when it is enqueued. This causes duplicate nodes to be enqueued multiple times.',
                    'practice_question': 'Which traversal algorithm guarantees finding the shortest path between two nodes in an unweighted graph? (Answer: Breadth-First Search / BFS).'
                },
                {
                    'id': 'dsa-dijkstra',
                    'title': '4. Single-Source Shortest Path: Dijkstra\'s Algorithm',
                    'read_time': '13 min',
                    'summary': 'Find minimum-cost paths on non-negative weighted graphs using greedy priority queues and edge relaxation.',
                    'concept': """**Dijkstra's Algorithm** computes the shortest paths from a single source vertex to all other vertices in a directed or undirected graph with **non-negative edge weights**.

Key Mechanics:
- Maintains a table of shortest distance estimates `dist[v]` initialized to $\\infty$ (`dist[source] = 0`).
- Uses a **Min-Priority Queue** to greedily extract the unvisited vertex $u$ with minimal `dist[u]`.
- **Edge Relaxation**: For each edge $(u, v)$ with weight $w$:
  $\\text{if } \\text{dist}[u] + w < \\text{dist}[v]: \\text{dist}[v] = \\text{dist}[u] + w$

Complexity:
- Using a Min-Heap: $O((V + E) \\log V)$.
- Limitation: **Fails on graphs with negative edge weights**! (Use the Bellman-Ford algorithm $O(VE)$ instead).""",
                    'syntax': """heapq.heappush(pq, (dist[v], v))
""",
                    'code_example': """import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, u = heapq.heappop(pq)
        
        if curr_dist > distances[u]:
            continue
            
        for v, weight in graph[u]:
            distance = curr_dist + weight
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return distances

network = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('B', 1), ('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}

shortest_distances = dijkstra(network, 'A')
for dest, cost in sorted(shortest_distances.items()):
    print(f"Cost to reach '{dest}' from 'A': {cost}")
""",
                    'expected_output': """Cost to reach 'A' from 'A': 0
Cost to reach 'B' from 'A': 3
Cost to reach 'C' from 'A': 2
Cost to reach 'D' from 'A': 8
Cost to reach 'E' from 'A': 10
""",
                    'common_mistakes': 'Attempting to run Dijkstra\'s algorithm on graphs with negative weight edges, which causes infinite loops or incorrect greedy choices.',
                    'practice_question': 'What is the time complexity of Dijkstra\'s algorithm implemented with a binary min-heap? (Answer: $O((V + E) \\log V)$).'
                },
                {
                    'id': 'dsa-mst',
                    'title': '5. Minimum Spanning Trees (MST): Kruskal\'s & Prim\'s',
                    'read_time': '12 min',
                    'summary': 'Connect all graph vertices with minimal total edge weight using Disjoint-Set Union (Kruskal) or priority queues (Prim).',
                    'concept': """A **Spanning Tree** of an undirected, connected, weighted graph $G=(V, E)$ is a subgraph that is a tree and connects all vertices together without cycles (contains exactly $V - 1$ edges).
A **Minimum Spanning Tree (MST)** is a spanning tree whose sum of edge weights is minimized.

Algorithms:
1. **Kruskal's Algorithm** (Greedy edge selection):
   - Sort all edges in ascending order of weight.
   - Iterate through sorted edges: if adding the edge does not form a cycle, include it in the MST.
   - Cycle detection is performed in near $O(1)$ amortized time using **Disjoint-Set Union (Union-Find)** with path compression.
   - Complexity: $O(E \\log E)$.
2. **Prim's Algorithm** (Greedy vertex growth):
   - Grows a single tree starting from an arbitrary root node, repeatedly picking the cheapest edge connecting the tree to an unvisited vertex using a priority queue.
   - Complexity: $O(E \\log V)$.""",
                    'syntax': """# Kruskal's Disjoint-Set Union
def find(i): ...
def union(i, j): ...
""",
                    'code_example': """class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

# Edges: (weight, u, v)
edges = [
    (1, 0, 1),
    (3, 1, 2),
    (4, 0, 2),
    (2, 1, 3),
    (5, 2, 3)
]
edges.sort()
ds = DisjointSet(4)
mst_weight = 0
mst_edges = []

for w, u, v in edges:
    if ds.union(u, v):
        mst_weight += w
        mst_edges.append((u, v, w))

print("Kruskal MST Total Weight:", mst_weight)
print("Included MST Edges (u, v, weight):", mst_edges)
""",
                    'expected_output': """Kruskal MST Total Weight: 6
Included MST Edges (u, v, weight): [(0, 1, 1), (1, 3, 2), (1, 2, 3)]
""",
                    'common_mistakes': 'Adding an edge in Kruskal\'s without verifying `find(u) != find(v)`, which introduces cycles and violates tree properties.',
                    'practice_question': 'How many edges are contained in a Minimum Spanning Tree of a connected graph with $V$ vertices? (Answer: Exactly $V - 1$ edges).'
                },
                {
                    'id': 'dsa-greedy-algorithms',
                    'title': '6. Greedy Algorithms: Activity Selection & Fractional Knapsack',
                    'read_time': '11 min',
                    'summary': 'Prove greedy choice property and optimal substructure on Activity Selection and Fractional Knapsack.',
                    'concept': """A **Greedy Algorithm** builds up a solution piece by piece, always choosing the next piece that offers the most immediate, local optimal benefit ("greedy choice").

Prerequisites for Greedy Correctness:
1. **Greedy Choice Property**: A globally optimal solution can be arrived at by making locally optimal decisions without backtracking.
2. **Optimal Substructure**: An optimal solution to the overall problem contains optimal solutions to its subproblems.

Classic Problems:
- **Activity Selection**: Select maximum non-overlapping intervals. Sort activities by **Finish Time** and pick greedily!
- **Fractional Knapsack**: Items can be subdivided. Sort items by value-to-weight ratio ($v_i / w_i$) and fill greedily ($O(n \\log n)$). Note: The 0/1 Knapsack problem CANNOT be solved with a greedy approach; it requires Dynamic Programming!""",
                    'syntax': """activities.sort(key=lambda x: x[1]) # Sort by finish time
""",
                    'code_example': """def activity_selection(intervals):
    # Sort intervals by finish time
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    selected = [sorted_intervals[0]]
    
    for start, finish in sorted_intervals[1:]:
        # If start is >= finish time of last selected
        if start >= selected[-1][1]:
            selected.append((start, finish))
            
    return selected

class_sessions = [(1, 3), (2, 5), (4, 6), (6, 8), (5, 7), (8, 9)]
scheduled = activity_selection(class_sessions)
print(f"Scheduled {len(scheduled)} optimal sessions without collision:")
for s, f in scheduled:
    print(f" - Session from {s}:00 to {f}:00")
""",
                    'expected_output': """Scheduled 4 optimal sessions without collision:
 - Session from 1:00 to 3:00
 - Session from 4:00 to 6:00
 - Session from 6:00 to 8:00
 - Session from 8:00 to 9:00
""",
                    'common_mistakes': 'Attempting to solve the 0/1 Knapsack problem (where items cannot be divided) using a greedy value-density heuristic. Counterexamples readily prove greedy yields suboptimal values for 0/1 knapsack.',
                    'practice_question': 'By what attribute must intervals be sorted to solve the Activity Selection problem greedily? (Answer: By their Finish / End time).'
                },
                {
                    'id': 'dsa-dp-knapsack',
                    'title': '7. Dynamic Programming: 0/1 Knapsack (Memoization vs Tabulation)',
                    'read_time': '13 min',
                    'summary': 'Transform exponential recursive searches into pseudo-polynomial DP tables using overlapping subproblem reuse.',
                    'concept': """**Dynamic Programming (DP)** solves complex problems by breaking them down into simpler subproblems, solving each subproblem once, and storing their solutions in a table.

Requirements:
1. **Overlapping Subproblems**: The same recursive subproblems are encountered repeatedly.
2. **Optimal Substructure**: Optimal solution built from optimal subproblem solutions.

DP Approaches:
- **Top-Down with Memoization**: Standard recursion augmented with a cache table (dict or array).
- **Bottom-Up Tabulation**: Iterative table filling from smallest base cases to final answer.

**0/1 Knapsack Problem**:
Given $n$ items with weights $w_i$ and values $v_i$, maximize total value within weight capacity $W$.
Recurrence:
$DP[i][w] = \\max(DP[i-1][w], \\, v_{i-1} + DP[i-1][w - w_{i-1}])$ if $w_{i-1} \\le w$, else $DP[i-1][w]$.
Complexity: $O(n \\cdot W)$ time and space (pseudo-polynomial).""",
                    'syntax': """dp = [[0] * (W + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for w in range(1, W + 1): ...
""",
                    'code_example': """def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

w = [2, 3, 4, 5]
v = [3, 4, 5, 6]
W = 5
max_val = knapsack_01(w, v, W)
print(f"Maximum knapsack value achieved for capacity {W}: ${max_val}")
""",
                    'expected_output': """Maximum knapsack value achieved for capacity 5: $7
""",
                    'common_mistakes': 'Confusing polynomial time with pseudo-polynomial time. The 0/1 knapsack runtime $O(n \\cdot W)$ depends on the numerical value of $W$, not just its input representation length.',
                    'practice_question': 'What are the two core properties a problem must possess to be solvable via Dynamic Programming? (Answer: Overlapping Subproblems and Optimal Substructure).'
                },
                {
                    'id': 'dsa-dp-lcs',
                    'title': '8. Dynamic Programming: Longest Common Subsequence (LCS)',
                    'read_time': '12 min',
                    'summary': 'Compute longest common subsequences for diff engines, DNA sequencing, and backtrack optimal alignment strings.',
                    'concept': """The **Longest Common Subsequence (LCS)** problem finds the length of the longest subsequence present in both strings $X[0 \\dots m-1]$ and $Y[0 \\dots n-1]$ in the same relative order (not necessarily contiguous).

Recurrence Relation:
Let $c[i, j]$ be the length of LCS of prefixes $X[0 \\dots i-1]$ and $Y[0 \\dots j-1]$:
- If $X[i-1] == Y[j-1]$: $c[i, j] = 1 + c[i-1, j-1]$ (diagonal transition)
- If $X[i-1] \\ne Y[j-1]$: $c[i, j] = \\max(c[i-1, j], \\, c[i, j-1])$ (max of left and top cells)

Applications: Git diff comparison algorithms, bioinformatics DNA sequence alignment, and spell checkers.""",
                    'syntax': """if X[i-1] == Y[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
""",
                    'code_example': """def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct the LCS string by backtracking through the matrix
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], "".join(reversed(lcs_chars))

length, sequence = lcs("EDUCATIONAL", "ADAPTIVE")
print(f"LCS Length: {length} | Subsequence: '{sequence}'")
""",
                    'expected_output': """LCS Length: 4 | Subsequence: 'DAI' or matching alignment
""",
                    'common_mistakes': 'Confusing a subsequence with a substring. A substring must be contiguous, while a subsequence does not have to be contiguous.',
                    'practice_question': 'What is the time complexity of computing the LCS of two strings of lengths $m$ and $n$ using DP? (Answer: $O(m \\cdot n)$).'
                },
                {
                    'id': 'dsa-backtracking',
                    'title': '9. Backtracking: State-Space Search & the N-Queens Problem',
                    'read_time': '12 min',
                    'summary': 'Prune invalid state-space trees with backtracking, bounding functions, and solve the N-Queens constraint puzzle.',
                    'concept': """**Backtracking** is an algorithmic technique for solving constraint satisfaction problems incrementally. It attempts to build a candidate solution step by step: as soon as it determines that a candidate cannot possibly be completed into a valid solution, it **abandons (prunes)** the candidate and backtracks to the previous choice point.

**N-Queens Problem**:
Place $N$ chess queens on an $N \\times N$ chessboard such that no two queens attack each other (no two queens share the same row, column, or diagonal).
Instead of checking all $N^{2N}$ board configurations, backtracking checks columns incrementally row-by-row, reducing search branches exponentially.""",
                    'syntax': """def backtrack(candidate):
    if is_solution(candidate):
        output(candidate); return
    for choice in choices:
        if is_valid(choice, candidate):
            apply(choice)
            backtrack(candidate)
            undo(choice) # Backtrack!
""",
                    'code_example': """def solve_n_queens(n):
    solutions = []
    cols = set()
    diag1 = set() # (r - c)
    diag2 = set() # (r + c)

    def backtrack(r, current_board):
        if r == n:
            solutions.append(list(current_board))
            return

        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue

            # Place queen
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            current_board.append(c)

            backtrack(r + 1, current_board)

            # Undo move (backtrack)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            current_board.pop()

    backtrack(0, [])
    return solutions

solutions_4 = solve_n_queens(4)
print(f"Total valid configurations for 4-Queens: {len(solutions_4)}")
print("First valid board (queen col per row):", solutions_4[0])
""",
                    'expected_output': """Total valid configurations for 4-Queens: 2
First valid board (queen col per row): [1, 3, 0, 2]
""",
                    'common_mistakes': 'Forgetting to undo choices (state modifications) after returning from recursive calls, which poisons subsequent candidate explorations.',
                    'practice_question': 'How does backtracking differ from brute-force exhaustive search? (Answer: Backtracking prunes entire subtrees of candidates as soon as a constraint is violated, avoiding exhaustive exploration).'
                }
            ]
        }
    }
}
