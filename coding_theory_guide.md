# Coding Theory Guide: Fundamentals, Patterns & Concepts

> Structured for interview preparation. Each section covers: **What it is**, **How it works in memory**, **Core operations & complexity**, **Patterns**, **Side concepts**, and **When to use what**.

---

# Table of Contents

1. [Arrays & Strings (~30% of questions)](#1-arrays--strings)
2. [Linked Lists (~20%)](#2-linked-lists)
3. [Trees & Graphs (~20%)](#3-trees--graphs)
4. [Dynamic Programming (~12%)](#4-dynamic-programming)
5. [Hash Maps & Sets (~8%)](#5-hash-maps--sets)
6. [Stacks & Queues (~5%)](#6-stacks--queues)
7. [Sorting & Searching (~5%)](#7-sorting--searching)
8. [Bit Manipulation (Bonus)](#8-bit-manipulation)

---

# 1. Arrays & Strings

## 1.1 Fundamentals

### What Is an Array?

An array is a contiguous block of memory where elements are stored sequentially. Each element occupies the same fixed size, which means any element can be accessed in O(1) time by computing its memory address:

```
address(arr[i]) = base_address + i * element_size
```

In Python, `list` is a dynamic array (resizable). Under the hood it stores an array of **pointers** to objects, not the objects themselves.

### Memory Layout

```
Index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
Memory: │  10 │  20 │  30 │  40 │  50 │   ← contiguous
        └─────┴─────┴─────┴─────┴─────┘
```

Key consequence: inserting/deleting in the middle requires shifting all subsequent elements.

### Core Operations & Complexity

| Operation | Time | Why |
|-----------|------|-----|
| Access by index `arr[i]` | O(1) | Direct address calculation |
| Search (unsorted) | O(n) | Must scan linearly |
| Search (sorted) | O(log n) | Binary search |
| Append to end | O(1) amortized | Occasionally resizes (doubles capacity) |
| Insert at index | O(n) | Must shift elements right |
| Delete at index | O(n) | Must shift elements left |
| Slice `arr[i:j]` | O(j-i) | Copies the range |

### Dynamic Array Resizing (Amortized Analysis)

When a dynamic array runs out of capacity, it allocates a new array (typically 2x the size), copies everything over, and frees the old one. This single resize is O(n), but since it happens after n insertions, the **amortized** cost per insertion is O(1).

```
Capacity: 1 → 2 → 4 → 8 → 16 → 32 → ...
           └─copy 1  └─copy 2  └─copy 4  └─copy 8
```

Total copies after n insertions: 1 + 2 + 4 + ... + n ≈ 2n = O(n) total → O(1) amortized per operation.

### Strings

Strings are essentially arrays of characters. In Python, strings are **immutable** — every modification creates a new string.

Critical implication:

```python
# BAD: O(n²) because each += creates a new string
s = ""
for char in chars:
    s += char

# GOOD: O(n)
s = "".join(chars)
```

String comparison is O(min(len(a), len(b))) — character by character.

---

## 1.2 Patterns

### Pattern: Two Pointers

**When to use**: Sorted arrays, finding pairs, comparing from both ends, partitioning.

**How it works**: Maintain two indices that move toward each other (or in the same direction) based on conditions.

**Variant A: Opposite Direction (converging)**

```
left →              ← right
[1, 2, 3, 4, 5, 6, 7]

Move left right if sum too small, right left if too large.
```

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
```

**Variant B: Same Direction (fast/slow or read/write)**

Used for in-place modifications — one pointer reads, one writes.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

**Classic problems**: 3Sum, Container With Most Water, Trapping Rain Water, Remove Duplicates, Move Zeroes.

---

### Pattern: Sliding Window

**When to use**: Finding a contiguous subarray/substring that satisfies some constraint (max/min length, sum, distinct count, etc.).

**How it works**: Maintain a window `[left, right]` that expands by moving `right` and contracts by moving `left`. Use a hash map or counter to track the window state.

**Template (variable-size window)**:

```python
def sliding_window(s):
    left = 0
    window_state = {}  # or set, counter, etc.
    best = 0

    for right in range(len(s)):
        # 1. Expand: add s[right] to window state
        window_state[s[right]] = window_state.get(s[right], 0) + 1

        # 2. Contract: shrink from left while window is invalid
        while window_is_invalid(window_state):
            window_state[s[left]] -= 1
            if window_state[s[left]] == 0:
                del window_state[s[left]]
            left += 1

        # 3. Update answer
        best = max(best, right - left + 1)

    return best
```

**Fixed-size window** (size k): just move left = right - k + 1 when right >= k-1.

**Classic problems**: Longest Substring Without Repeating Characters, Minimum Window Substring, Maximum Sum Subarray of Size K, Longest Repeating Character Replacement.

---

### Pattern: Prefix Sum

**When to use**: Frequent range sum queries, subarray sum equals K.

**How it works**: Precompute cumulative sums. Any range sum becomes a subtraction.

```
Array:      [3, 1, 4, 1, 5]
Prefix Sum: [0, 3, 4, 8, 9, 14]

Sum(arr[1..3]) = prefix[4] - prefix[1] = 9 - 3 = 6
```

```python
def subarray_sum_equals_k(nums, k):
    prefix_sum = 0
    count = 0
    seen = {0: 1}  # prefix_sum -> frequency
    for num in nums:
        prefix_sum += num
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    return count
```

**Classic problems**: Subarray Sum Equals K, Range Sum Query, Contiguous Array (0s and 1s).

---

### Pattern: Kadane's Algorithm

**When to use**: Maximum subarray sum (contiguous).

**Core idea**: At each position, decide: extend the previous subarray or start a new one.

```python
def max_subarray(nums):
    curr_max = global_max = nums[0]
    for num in nums[1:]:
        curr_max = max(num, curr_max + num)
        global_max = max(global_max, curr_max)
    return global_max
```

This is actually a form of 1D dynamic programming: `dp[i] = max(nums[i], dp[i-1] + nums[i])`.

---

### Pattern: In-Place Array Manipulation

**When to use**: Problems that require O(1) extra space — use the array itself as storage.

Techniques:
- **Swap elements** to their correct position (Cyclic Sort)
- **Use sign flipping** to mark visited indices (e.g., Find All Duplicates)
- **Use modular arithmetic** to encode two values in one cell

```python
# Find all duplicates in [1..n] array, O(1) space
def find_duplicates(nums):
    result = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] = -nums[idx]
    return result
```

---

## 1.3 Side Concepts

### Subarray vs. Subsequence vs. Subset

- **Subarray**: contiguous elements. `[2,3]` is a subarray of `[1,2,3,4]`.
- **Subsequence**: elements in order but not necessarily contiguous. `[1,3]` is a subsequence.
- **Subset**: any combination, order doesn't matter. `{3,1}` is a subset.

### String-Specific Techniques

- **Character frequency array**: For lowercase letters, use `[0]*26` instead of a hash map. Index = `ord(c) - ord('a')`.
- **Anagram check**: Two strings are anagrams if their sorted forms are equal, or if their character frequency arrays are equal.
- **Palindrome check**: `s == s[::-1]` or use two pointers converging from both ends.
- **KMP / Rabin-Karp**: Pattern matching algorithms. KMP is O(n+m). Rarely needed in interviews but good to mention.

### Matrix (2D Array)

- Access: `matrix[row][col]`
- Traversal patterns: row-by-row, column-by-column, diagonal, spiral
- **Rotation 90° clockwise**: Transpose + reverse each row
- **In-place marking**: Use a sentinel value to mark visited cells (e.g., grid problems like Number of Islands)

---

# 2. Linked Lists

## 2.1 Fundamentals

### What Is a Linked List?

A linked list is a sequence of nodes where each node contains data and a pointer (reference) to the next node. Unlike arrays, nodes are **not contiguous in memory** — they can be anywhere on the heap.

```
┌──────┬──────┐    ┌──────┬──────┐    ┌──────┬──────┐
│ data │ next │───→│ data │ next │───→│ data │ next │───→ None
│  10  │   ●──│    │  20  │   ●──│    │  30  │   ●──│
└──────┴──────┘    └──────┴──────┘    └──────┴──────┘
  head
```

### Singly vs. Doubly Linked List

**Singly linked**: Each node has `data` + `next`. Can only traverse forward.

**Doubly linked**: Each node has `data` + `next` + `prev`. Can traverse both directions. Costs extra memory per node.

```
None ←── ┌──────┬──────┬──────┐    ┌──────┬──────┬──────┐
         │ prev │ data │ next │←──→│ prev │ data │ next │ ──→ None
         └──────┴──────┴──────┘    └──────┴──────┴──────┘
```

### Core Operations & Complexity

| Operation | Singly Linked | Doubly Linked | Array |
|-----------|:---:|:---:|:---:|
| Access by index | O(n) | O(n) | O(1) |
| Search | O(n) | O(n) | O(n) |
| Insert at head | **O(1)** | **O(1)** | O(n) |
| Insert at tail (with tail ptr) | **O(1)** | **O(1)** | O(1) amortized |
| Insert at middle (given node) | **O(1)** | **O(1)** | O(n) |
| Delete given node | O(n)* | **O(1)** | O(n) |
| Delete at head | **O(1)** | **O(1)** | O(n) |

\* Singly linked delete requires the previous node, which means traversal unless you use the copy-and-delete-next trick.

### Why Use Linked Lists?

- O(1) insertion/deletion at known positions (no shifting)
- Dynamic size without resizing overhead
- Building block for stacks, queues, hash map chaining, LRU caches, adjacency lists

### Node Definition

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

---

## 2.2 Patterns

### Pattern: Dummy Head Node

**When to use**: Any time the head of the list might change (insertions at front, deletions of head, merging lists).

**Why**: Eliminates special-case handling for the head node.

```python
def remove_elements(head, val):
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return dummy.next
```

Without dummy, you'd need separate logic for `head.val == val`.

---

### Pattern: Fast & Slow Pointers (Floyd's Tortoise & Hare)

**When to use**: Cycle detection, finding the middle, finding the nth-from-end.

**How it works**: Two pointers traverse the list at different speeds. Fast moves 2 steps per iteration, slow moves 1.

**Finding middle node:**

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle (right-middle for even length)
```

Why it works: When fast reaches the end, slow is at the halfway point.

**Cycle detection:**

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

Why it works: If there's a cycle, fast will eventually "lap" slow inside the cycle. If no cycle, fast reaches None.

**Finding cycle start:**

After slow and fast meet, move one pointer back to head. Advance both by 1. They meet at the cycle start.

```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Found cycle; now find entry point
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

Why this works (mathematical proof):
- Let distance from head to cycle start = `a`
- Let distance from cycle start to meeting point = `b`
- Let cycle length = `c`
- Slow traveled: `a + b`
- Fast traveled: `a + b + k*c` (for some k laps)
- Since fast = 2 * slow: `a + b + k*c = 2(a + b)` → `a = k*c - b`
- So moving `a` steps from meeting point lands at cycle start

---

### Pattern: Reverse a Linked List

**When to use**: Palindrome check, reversing sections, many list manipulation problems.

**Iterative (O(1) space):**

```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next    # save next
        curr.next = prev   # reverse pointer
        prev = curr        # advance prev
        curr = nxt         # advance curr
    return prev
```

Visualization:
```
Step 0: None   1 → 2 → 3 → None
               ↑prev  ↑curr

Step 1: None ← 1   2 → 3 → None
                    ↑prev  ↑curr

Step 2: None ← 1 ← 2   3 → None
                        ↑prev  ↑curr

Step 3: None ← 1 ← 2 ← 3
                         ↑prev   curr=None
```

**Recursive:**

```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

### Pattern: Merge Two Sorted Lists

**Core technique used in**: Merge K sorted lists, merge sort on linked lists.

```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

---

### Pattern: Two-Pointer for Nth from End

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
```

Why: Fast gets `n+1` ahead, then both advance. When fast hits None, slow is right before the target.

---

## 2.3 Side Concepts

### Linked List vs. Array: When to Choose

| Need | Choose |
|------|--------|
| Random access by index | Array |
| Frequent insertions/deletions at arbitrary positions | Linked List |
| Memory efficiency (small elements) | Array (no pointer overhead) |
| Unknown or highly variable size | Linked List |
| Cache performance (spatial locality) | Array |

### Common Traps

1. **Losing references**: Always save `next` before modifying pointers.
2. **Null pointer**: Always check `node is not None` and `node.next is not None` before accessing.
3. **Off-by-one with dummy**: Remember to return `dummy.next`, not `dummy`.
4. **Modifying while iterating**: If you delete a node, your iteration pointer must account for the change.

---

# 3. Trees & Graphs

## 3.1 Tree Fundamentals

### What Is a Tree?

A tree is a connected, acyclic graph. In interview context, usually a **binary tree**: each node has at most 2 children (left, right).

```
        1           ← root (level 0, depth 0)
       / \
      2   3         ← level 1
     / \   \
    4   5   6       ← level 2 (leaves: 4, 5, 6)
```

### Key Terminology

| Term | Definition |
|------|-----------|
| **Root** | The topmost node (no parent) |
| **Leaf** | A node with no children |
| **Depth** | Distance from root to node (root depth = 0) |
| **Height** | Distance from node to deepest leaf (leaf height = 0) |
| **Height of tree** | Height of the root |
| **Level** | Set of all nodes at the same depth |
| **Subtree** | A node and all its descendants |
| **Complete binary tree** | Every level fully filled except possibly the last, which fills left to right |
| **Full binary tree** | Every node has 0 or 2 children |
| **Perfect binary tree** | All internal nodes have 2 children and all leaves are at the same level |
| **Balanced tree** | Height of left and right subtrees differ by at most 1 |

### Binary Search Tree (BST)

A binary tree where for every node:
- All values in left subtree < node's value
- All values in right subtree > node's value

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

**BST operations:**

| Operation | Average | Worst (skewed) |
|-----------|---------|----------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| In-order traversal | O(n) | O(n) |

**In-order traversal of BST produces sorted output.** This is a frequently tested property.

### Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## 3.2 Tree Traversal Patterns

### The Three DFS Traversals

```
        1
       / \
      2   3
     / \
    4   5
```

| Traversal | Order | Visits | Result | Use Case |
|-----------|-------|--------|--------|----------|
| **Pre-order** | Root → Left → Right | Process before children | [1,2,4,5,3] | Serialize/copy tree |
| **In-order** | Left → Root → Right | Process between children | [4,2,5,1,3] | BST sorted order |
| **Post-order** | Left → Right → Root | Process after children | [4,5,2,3,1] | Delete tree, evaluate expressions |

**Recursive implementations:**

```python
def preorder(root):
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def postorder(root):
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

**Iterative pre-order (using stack):**

```python
def preorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)  # right first so left is processed first
        if node.left: stack.append(node.left)
    return result
```

**Iterative in-order (using stack):**

```python
def inorder_iterative(root):
    stack, result = [], []
    curr = root
    while curr or stack:
        while curr:            # go as far left as possible
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

### BFS / Level-Order Traversal

```python
from collections import deque

def level_order(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

The `for _ in range(len(queue))` trick processes exactly one level per outer loop iteration.

---

## 3.3 Tree Patterns

### Pattern: Recursive Structure (Most Tree Problems)

Most binary tree problems follow this template:

```python
def solve(root):
    # Base case
    if not root:
        return base_value

    # Recursive calls
    left_result = solve(root.left)
    right_result = solve(root.right)

    # Combine results
    return combine(root.val, left_result, right_result)
```

**Examples:**

```python
# Max depth
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Is balanced?
def is_balanced(root):
    def height(node):
        if not node: return 0
        left_h = height(node.left)
        right_h = height(node.right)
        if left_h == -1 or right_h == -1 or abs(left_h - right_h) > 1:
            return -1
        return 1 + max(left_h, right_h)
    return height(root) != -1

# Invert binary tree
def invert_tree(root):
    if not root: return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

### Pattern: Path-Based Problems

Track a running value (sum, path) as you traverse.

```python
# Has path sum equal to target?
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:  # leaf
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))
```

### Pattern: Lowest Common Ancestor (LCA)

**For BST** (exploit ordering):

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

**For general binary tree** (no ordering guarantee):

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root     # p and q are in different subtrees
    return left or right
```

### Pattern: Serialize / Deserialize

Convert tree to string and back. Use pre-order with null markers.

```python
def serialize(root):
    if not root: return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    nodes = iter(data.split(","))
    def build():
        val = next(nodes)
        if val == "null": return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()
```

---

## 3.4 Graph Fundamentals

### Representation

**Adjacency List** (most common in interviews):

```python
# Unweighted
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# From edge list
from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # omit for directed
```

**Adjacency Matrix**: `matrix[i][j] = 1` if edge from i to j. O(V²) space. Good for dense graphs.

### Directed vs. Undirected

- **Undirected**: edge (u,v) means you can go both ways. Add both `graph[u].append(v)` and `graph[v].append(u)`.
- **Directed**: edge (u,v) means u→v only. Add only `graph[u].append(v)`.

### Weighted Graphs

Store `(neighbor, weight)` tuples:

```python
graph = defaultdict(list)
for u, v, w in edges:
    graph[u].append((v, w))
```

---

## 3.5 Graph Patterns

### Pattern: BFS (Breadth-First Search)

**When to use**: Shortest path in unweighted graph, level-by-level exploration, nearest neighbor problems.

**How it works**: Explore all neighbors at distance d before exploring distance d+1. Uses a queue.

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**BFS always finds the shortest path in an unweighted graph.** This is because it explores nodes in order of increasing distance from the source.

**Time**: O(V + E). **Space**: O(V).

### Pattern: DFS (Depth-First Search)

**When to use**: Connectivity, cycle detection, topological sort, path finding, exhaustive search.

**How it works**: Go as deep as possible before backtracking. Uses recursion (implicit stack) or explicit stack.

```python
# Recursive
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Iterative
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

**Time**: O(V + E). **Space**: O(V).

### BFS vs. DFS: When to Use Which

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Shortest path (unweighted) | BFS | Explores by distance |
| Shortest path (weighted) | Dijkstra / BFS variant | BFS doesn't handle weights |
| Check if path exists | Either | Both work |
| Connected components | Either | Both work |
| Cycle detection (directed) | DFS | Track recursion stack |
| Topological sort | DFS | Post-order gives reverse topo order |
| Level-order / layers | BFS | Natural level structure |
| Exhaustive search / backtracking | DFS | Memory efficient for deep search |

### Pattern: Grid as Graph

Many interview problems represent graphs as 2D grids. Each cell is a node; its neighbors are the 4 (or 8) adjacent cells.

```python
def grid_bfs(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    visited = set()
    visited.add((start_r, start_c))
    queue = deque([(start_r, start_c)])

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 1:
                visited.add((nr, nc))
                queue.append((nr, nc))
```

### Pattern: Cycle Detection

**Undirected graph**: DFS — if you encounter a visited node that isn't the parent, there's a cycle.

**Directed graph**: DFS with 3 states (unvisited, in-progress, completed). If you encounter an in-progress node, there's a cycle.

```python
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True   # back edge = cycle
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    return any(color[i] == WHITE and dfs(i) for i in range(n))
```

### Pattern: Topological Sort

**What it is**: A linear ordering of nodes in a DAG (Directed Acyclic Graph) such that for every edge u→v, u comes before v.

**When to use**: Course scheduling, build systems, dependency resolution.

**Kahn's Algorithm (BFS-based):**

```python
from collections import deque

def topological_sort(graph, n):
    in_degree = [0] * n
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []  # empty = cycle exists
```

### Pattern: Union-Find (Disjoint Set Union)

**When to use**: Dynamic connectivity, counting connected components, cycle detection in undirected graphs.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

**Time**: Nearly O(1) per operation (amortized with path compression + union by rank).

**Classic problems**: Number of Islands, Accounts Merge, Redundant Connection.

### Pattern: Shortest Path (Weighted) — Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph, start, n):
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    return dist
```

**Time**: O((V + E) log V) with a binary heap.

**Requirement**: No negative edge weights.

---

## 3.6 Side Concepts

### Tree Properties to Know

- A binary tree with n nodes has exactly n-1 edges
- A perfect binary tree of height h has 2^(h+1) - 1 nodes
- Max nodes at level k = 2^k
- Height of a balanced binary tree with n nodes ≈ log₂(n)
- **BST in-order traversal = sorted order** (frequently tested)

### N-ary Trees

Same patterns as binary trees, just iterate over `node.children` instead of `left`/`right`.

### Trie (Prefix Tree)

Specialized tree for string operations. Each node represents a character; paths from root represent prefixes.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

**Use cases**: Autocomplete, spell check, IP routing, word search puzzles.

---

# 4. Dynamic Programming

## 4.1 Fundamentals

### What Is Dynamic Programming?

Dynamic programming (DP) is an optimization technique for problems with two properties:

1. **Optimal substructure**: The optimal solution can be built from optimal solutions to subproblems.
2. **Overlapping subproblems**: The same subproblems are solved repeatedly.

DP avoids redundant computation by storing results of subproblems (memoization or tabulation).

### Recursion vs. Memoization vs. Tabulation

```
Plain Recursion:     Exponential time, recomputes subproblems
                     fib(5) → fib(4) + fib(3)
                              fib(3) + fib(2)  +  fib(2) + fib(1)
                              ...many repeated calls...

Memoization:         Top-down, cache results, recursive
(Top-Down DP)        Same recursion tree but each subproblem computed only once

Tabulation:          Bottom-up, iterative, fill a table
(Bottom-Up DP)       No recursion overhead, explicit iteration order
```

### The Fibonacci Example (All 3 Approaches)

```python
# 1. Plain recursion — O(2^n) time, O(n) stack space
def fib_recursive(n):
    if n <= 1: return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# 2. Memoization (top-down) — O(n) time, O(n) space
def fib_memo(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# 3. Tabulation (bottom-up) — O(n) time, O(n) space
def fib_tab(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# 4. Space-optimized — O(n) time, O(1) space
def fib_opt(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

---

## 4.2 The 5-Step DP Framework

For any DP problem, follow these steps:

### Step 1: Define the State

What does `dp[i]` (or `dp[i][j]`) represent? This is the most important step.

### Step 2: Write the Recurrence (Transition)

How does `dp[i]` relate to smaller subproblems?

### Step 3: Identify the Base Cases

What are the trivially solvable subproblems?

### Step 4: Determine the Iteration Order

Which subproblems must be solved first? (Bottom-up: left to right, top to bottom, etc.)

### Step 5: Optimize Space (if needed)

If `dp[i]` only depends on `dp[i-1]` (or a fixed window), reduce the table to O(1) or O(n) space.

---

## 4.3 DP Patterns

### Pattern: 1D DP (Linear Sequence)

**State**: `dp[i]` = answer for the first `i` elements.

**Classic problems:**

**Climbing Stairs:**
```python
# dp[i] = number of ways to reach step i
# dp[i] = dp[i-1] + dp[i-2]  (take 1 or 2 steps)
def climb_stairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

**House Robber:**
```python
# dp[i] = max money from houses 0..i
# dp[i] = max(dp[i-1], dp[i-2] + nums[i])  (skip or rob)
def rob(nums):
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1
```

**Word Break:**
```python
# dp[i] = can s[0:i] be segmented using dictionary words?
def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]
```

### Pattern: 2D DP (Two Sequences or Grid)

**State**: `dp[i][j]` = answer considering first `i` elements of A and first `j` elements of B, or position (i,j) in a grid.

**Longest Common Subsequence:**
```python
# dp[i][j] = LCS length of s1[0:i] and s2[0:j]
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

**Edit Distance:**
```python
# dp[i][j] = min edits to convert s1[0:i] to s2[0:j]
def min_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],      # delete
                                   dp[i][j-1],      # insert
                                   dp[i-1][j-1])    # replace
    return dp[m][n]
```

**Unique Paths (Grid):**
```python
# dp[i][j] = number of ways to reach (i,j) from (0,0)
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
```

### Pattern: Knapsack

**0/1 Knapsack** (each item used at most once):

```python
# dp[i][w] = max value using items 0..i with capacity w
def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # don't take item i
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]
```

**Unbounded Knapsack** (items can be reused):

```python
# Coin Change: min coins to make amount
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Pattern: Interval DP

**State**: `dp[i][j]` = answer for the subarray/substring from index `i` to `j`.

**Longest Palindromic Substring:**
```python
def longest_palindrome(s):
    n = len(s)
    if n < 2: return s
    start, max_len = 0, 1

    # Expand around center (simpler than full DP)
    def expand(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1

    for i in range(n):
        # Odd length
        l, length = expand(i, i)
        if length > max_len:
            start, max_len = l, length
        # Even length
        l, length = expand(i, i + 1)
        if length > max_len:
            start, max_len = l, length

    return s[start:start + max_len]
```

### Pattern: Decision at Each Step

Many DP problems boil down to: at position i, what choices do I have?

```
dp[i] = best of all choices at position i

Common choices:
  - Take or skip (knapsack, house robber)
  - Come from left, top, or diagonal (grid, edit distance)
  - Split at position k (matrix chain, burst balloons)
  - Extend previous or start fresh (Kadane's)
```

---

## 4.4 Side Concepts

### Recognizing DP Problems

A problem likely needs DP if:
1. It asks for **optimal** (min/max) or **count** of something
2. It involves making **choices** at each step
3. Greedy doesn't work (counterexample exists)
4. Brute force has **exponential** complexity due to repeated subproblems

### Memoization vs. Tabulation: When to Choose

| Aspect | Memoization (Top-Down) | Tabulation (Bottom-Up) |
|--------|----------------------|----------------------|
| Direction | Starts from original problem | Starts from base cases |
| Implementation | Recursion + cache | Loops + table |
| Subproblems solved | Only those needed | All of them |
| Stack overflow risk | Yes (deep recursion) | No |
| Easier to code? | Often yes (natural recursion) | Sometimes (explicit loops) |

### Space Optimization

If the recurrence only looks back a fixed number of rows/steps:
- `dp[i]` depends on `dp[i-1]` only → use two variables
- `dp[i][j]` depends on `dp[i-1][j]` → use one row, iterate left-to-right or right-to-left depending on dependencies

---

# 5. Hash Maps & Sets

## 5.1 Fundamentals

### What Is a Hash Map?

A hash map (dictionary in Python) stores key-value pairs and supports O(1) average-case lookup, insertion, and deletion. It works by:

1. Computing a **hash function** on the key → produces an integer
2. Using modulo to map the integer to a **bucket** (array index)
3. Storing the key-value pair in that bucket

```
key "apple" → hash("apple") = 42 → 42 % 8 = 2 → store in bucket 2

Buckets:
  [0]: empty
  [1]: empty
  [2]: ("apple", 5)  ← stored here
  [3]: empty
  ...
```

### Hash Collisions

When two keys map to the same bucket. Resolution strategies:

**Chaining**: Each bucket holds a linked list of entries. Worst case: all keys in one bucket → O(n) lookup.

```
Bucket 2: ("apple", 5) → ("grape", 3) → None
```

**Open addressing**: Probe for the next empty slot (linear probing, quadratic probing, double hashing).

### Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| Get | O(1) | O(n) |
| Put | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Contains | O(1) | O(n) |

Worst case happens with pathological hash collisions. In practice (and interviews), assume O(1).

### Hash Set

Same as hash map but stores only keys (no values). Used for membership testing.

### Python Specifics

```python
# dict — ordered by insertion order (Python 3.7+)
d = {}
d['key'] = 'value'
'key' in d                   # O(1) membership check
d.get('key', default)        # returns default if key missing
del d['key']                 # delete

# defaultdict — auto-initializes missing keys
from collections import defaultdict
d = defaultdict(list)        # missing key → empty list
d = defaultdict(int)         # missing key → 0

# Counter — frequency counting
from collections import Counter
c = Counter([1, 1, 2, 3])   # Counter({1: 2, 2: 1, 3: 1})
c.most_common(2)             # [(1, 2), (2, 1)]

# set
s = set()
s.add(1)
s.remove(1)                  # raises KeyError if missing
s.discard(1)                 # no error if missing
s1 & s2                      # intersection
s1 | s2                      # union
s1 - s2                      # difference
```

---

## 5.2 Patterns

### Pattern: Frequency Counting

Count occurrences and make decisions based on counts.

```python
def top_k_frequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in count.most_common(k)]
```

### Pattern: Hash Map as Cache/Index

Store previously seen values for O(1) lookups.

```python
# Two Sum: value → index mapping
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

### Pattern: Grouping by Key

Group elements that share a property.

```python
# Group Anagrams: sort as key
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### Pattern: Hash Set for Deduplication / Seen Tracking

```python
# Contains Duplicate
def contains_duplicate(nums):
    return len(nums) != len(set(nums))

# Longest Consecutive Sequence — O(n)
def longest_consecutive(nums):
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:  # only start from sequence beginning
            length = 1
            while num + length in num_set:
                length += 1
            best = max(best, length)
    return best
```

### Pattern: Rolling Hash

Compute hash of a sliding window in O(1) per slide. Used in Rabin-Karp string matching.

---

## 5.3 Side Concepts

### What Can Be a Hash Key in Python?

Only **immutable, hashable** objects:
- `int`, `float`, `str`, `bool` — yes
- `tuple` (of hashable elements) — yes
- `list`, `dict`, `set` — **NO** (mutable)
- `frozenset` — yes (immutable set)

This is why anagram keys use `tuple(sorted(s))` instead of `list(sorted(s))`.

### OrderedDict vs. dict

Since Python 3.7, `dict` maintains insertion order. `OrderedDict` additionally supports:
- `move_to_end(key)` — O(1) move to front or back
- `popitem(last=False)` — O(1) pop from front

This makes `OrderedDict` perfect for LRU Cache implementation.

### Hash Map vs. BST-based Map

| | Hash Map | BST Map (TreeMap) |
|--|---------|-------------------|
| Lookup | O(1) avg | O(log n) |
| Ordered iteration | No | Yes |
| Range queries | No | Yes |
| Worst case | O(n) | O(log n) balanced |

Use BST map when you need ordered keys or range queries. Use hash map for everything else.

---

# 6. Stacks & Queues

## 6.1 Stack Fundamentals

### What Is a Stack?

A stack is a Last-In-First-Out (LIFO) data structure. Think of a stack of plates — you add and remove from the top.

```
    ┌─────┐
    │  3  │  ← top (last in, first out)
    ├─────┤
    │  2  │
    ├─────┤
    │  1  │  ← bottom
    └─────┘

    push(4): add to top
    pop():   remove from top, returns 3
    peek():  look at top without removing, returns 3
```

### Operations & Complexity

| Operation | Time | Description |
|-----------|------|-------------|
| push | O(1) | Add to top |
| pop | O(1) | Remove from top |
| peek/top | O(1) | View top element |
| isEmpty | O(1) | Check if empty |
| search | O(n) | Must scan |

### Python Implementation

```python
# Use a list as a stack
stack = []
stack.append(1)    # push
stack.append(2)
stack.pop()        # returns 2
stack[-1]          # peek = 1
len(stack) == 0    # isEmpty
```

### Where Stacks Appear Naturally

- **Function call stack**: Each function call pushes a frame, return pops it
- **Recursion**: Every recursive call adds to the call stack
- **Undo operations**: Each action pushed, undo pops
- **Expression parsing**: Operators and operands
- **Browser history**: Forward/back navigation

---

## 6.2 Stack Patterns

### Pattern: Matching Brackets / Parentheses

**When to use**: Any problem involving nested structures, balanced pairs, or matching delimiters.

```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
```

**Why stack works**: The last opened bracket must be the first one closed — exactly LIFO order.

### Pattern: Monotonic Stack

**When to use**: Finding the next greater/smaller element, stock span, largest rectangle in histogram, trapping rain water.

**Monotonic decreasing stack** (for "next greater element"):

```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices; values at these indices are decreasing

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result

# Example: nums = [2, 1, 2, 4, 3]
# Result:         [4, 2, 4,-1,-1]
```

**Why it works**: The stack maintains elements waiting for their "next greater." When we find a larger element, we pop and assign. Each element is pushed and popped at most once → O(n).

**Monotonic increasing stack** (for "next smaller element"): flip the comparison.

### Pattern: Evaluate Expression

Process operators and operands using stacks.

```python
def eval_rpn(tokens):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),
    }
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]
```

### Pattern: Min Stack

Stack that supports getMin() in O(1).

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val

    def getMin(self):
        return self.min_stack[-1]
```

**Why two stacks**: The min_stack tracks the current minimum at each "level" of the main stack. When we pop a value that equals the current min, we also pop from min_stack to reveal the previous min.

---

## 6.3 Queue Fundamentals

### What Is a Queue?

A queue is a First-In-First-Out (FIFO) data structure. Think of a line at a store.

```
    enqueue →  ┌───┬───┬───┬───┐  → dequeue
     (rear)    │ 4 │ 3 │ 2 │ 1 │    (front)
               └───┴───┴───┴───┘
```

### Operations & Complexity

| Operation | Time |
|-----------|------|
| enqueue (add to rear) | O(1) |
| dequeue (remove from front) | O(1) |
| peek (view front) | O(1) |
| isEmpty | O(1) |

### Python Implementation

```python
from collections import deque

queue = deque()
queue.append(1)      # enqueue (right end)
queue.append(2)
queue.popleft()      # dequeue (left end), returns 1
queue[0]             # peek front
```

**Never use `list` as a queue**: `list.pop(0)` is O(n) because it shifts all elements. `deque.popleft()` is O(1).

### Deque (Double-Ended Queue)

Supports O(1) add/remove from both ends:

```python
d = deque()
d.append(x)       # add to right
d.appendleft(x)   # add to left
d.pop()            # remove from right
d.popleft()        # remove from left
```

---

## 6.4 Queue Patterns

### Pattern: BFS (the primary use of queues)

Covered in Trees & Graphs section. BFS uses a queue to process nodes level by level.

### Pattern: Sliding Window Maximum (Monotonic Deque)

Find the maximum in every window of size k in O(n) total.

```python
def max_sliding_window(nums, k):
    dq = deque()  # stores indices; values at indices are decreasing
    result = []

    for i in range(len(nums)):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements (they'll never be the max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

**Why it works**: The deque maintains indices of potentially useful elements in decreasing order. The front is always the current window maximum.

---

## 6.5 Priority Queue (Heap)

### What Is a Heap?

A binary heap is a complete binary tree where every parent is smaller (min-heap) or larger (max-heap) than its children. Implemented as an array.

```
Min-Heap:
         1
        / \
       3   2
      / \
     7   4

Array: [1, 3, 2, 7, 4]
Parent of i: (i-1) // 2
Left child of i: 2*i + 1
Right child of i: 2*i + 2
```

### Operations & Complexity

| Operation | Time |
|-----------|------|
| Insert (heappush) | O(log n) |
| Extract min/max (heappop) | O(log n) |
| Peek min/max | O(1) |
| Build heap from array (heapify) | O(n) |

### Python heapq (Min-Heap Only)

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappop(heap)         # returns 1 (smallest)
heap[0]                      # peek min = 2

# Max-heap trick: negate values
heapq.heappush(heap, -5)    # store negative
-heapq.heappop(heap)        # negate on extraction = 5

# Heapify existing list
arr = [3, 1, 2]
heapq.heapify(arr)           # in-place, O(n)

# N largest / smallest
heapq.nlargest(2, arr)
heapq.nsmallest(2, arr)
```

### When to Use a Heap

- **Top K elements**: Keep a heap of size K
- **Merge K sorted lists**: Min-heap of size K for the current front of each list
- **Stream median**: Two heaps (max-heap for lower half, min-heap for upper half)
- **Dijkstra's shortest path**: Min-heap for selecting next closest node
- **Task scheduling**: Process by priority

### Kth Largest Element

```python
def find_kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

Keep a min-heap of size k. After processing all elements, the root is the kth largest.

---

# 7. Sorting & Searching

## 7.1 Sorting Fundamentals

### Comparison of Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable? | Notes |
|-----------|------|---------|-------|-------|---------|-------|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Educational only |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | No | Minimal swaps |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes | Good for nearly sorted |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Guaranteed performance |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Fastest in practice |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No | In-place, not cache-friendly |
| **Counting Sort** | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | k = range of values |
| **Radix Sort** | O(d·n) | O(d·n) | O(d·n) | O(n+k) | Yes | d = number of digits |

### Stability

A sorting algorithm is **stable** if equal elements maintain their relative order from the input. Python's `sorted()` and `list.sort()` use **Timsort** (stable, O(n log n)).

Stability matters when sorting by multiple keys:
```python
# Sort by age, then by name (stable sort preserves name order within same age)
people.sort(key=lambda x: x.name)
people.sort(key=lambda x: x.age)
```

### Key Algorithms to Know Well

#### Merge Sort

Divide array in half, recursively sort each half, merge the sorted halves.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key properties**: Stable, O(n log n) guaranteed, O(n) extra space, great for linked lists (no random access needed), basis for external sorting.

#### Quick Sort

Choose a pivot, partition array into elements < pivot and elements > pivot, recursively sort partitions.

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Key properties**: In-place (O(log n) stack space), O(n²) worst case (sorted input with bad pivot), but O(n log n) average with random pivot. Fastest in practice due to cache efficiency.

**Quick Select** (find kth smallest in O(n) average):

```python
def quick_select(arr, k):
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k <= len(left):
        return quick_select(left, k)
    elif k <= len(left) + len(mid):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(mid))
```

#### Counting Sort

For integers in a known range [0, k]. Count occurrences, then reconstruct.

```python
def counting_sort(arr, max_val):
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)
    return result
```

O(n + k) time, O(k) space. Useful when k is small relative to n.

---

## 7.2 Searching: Binary Search

### The Fundamental Idea

Binary search works on **sorted** data. At each step, compare the middle element to the target and eliminate half the search space. O(log n) time.

### The Standard Template

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # avoids overflow in other languages
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # not found
```

### Variants: Finding Boundaries

**Find leftmost (first) occurrence:**

```python
def find_left(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

**Find rightmost (last) occurrence:**

```python
def find_right(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

### Pattern: Binary Search on Answer

**When to use**: The problem asks for a min/max value that satisfies a condition. The condition is monotonic (once true, stays true or vice versa).

```python
def binary_search_on_answer(low, high):
    while low < high:
        mid = (low + high) // 2
        if condition(mid):
            high = mid      # mid might be the answer, search left
        else:
            low = mid + 1   # mid doesn't work, search right
    return low
```

**Classic problems**: Koko Eating Bananas, Split Array Largest Sum, Capacity to Ship Packages.

### Pattern: Search in Rotated Sorted Array

The array was sorted then rotated. One half is always sorted.

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

---

## 7.3 Side Concepts

### Python Sorting Tips

```python
# Custom sort with key function
intervals.sort(key=lambda x: x[0])

# Sort by multiple criteria (sort by second element, then first)
arr.sort(key=lambda x: (x[1], x[0]))

# Sort descending
arr.sort(reverse=True)

# Stable sort allows multi-pass sorting
# Sort by age, maintaining alphabetical order within same age
people.sort(key=lambda p: p.name)
people.sort(key=lambda p: p.age)
```

### When Binary Search Applies (Non-Obvious Cases)

Binary search doesn't need a literal sorted array. It needs a **monotonic predicate** — a function that transitions from False to True (or True to False) and never switches back.

- Finding square root: `is mid*mid <= n?`
- Finding peak element: compare with neighbors
- Minimizing maximum: `can we achieve max_val <= mid?`
- Searching in matrix: treat as flattened sorted array

---

# 8. Bit Manipulation

## 8.1 Fundamentals

### Binary Representation

Every integer is stored as a sequence of bits (0s and 1s).

```
Decimal 13 = Binary 1101
             = 1×2³ + 1×2² + 0×2¹ + 1×2⁰
             = 8 + 4 + 0 + 1
```

### Core Bitwise Operations

| Operation | Symbol | Example | Result |
|-----------|--------|---------|--------|
| AND | `&` | `1010 & 1100` | `1000` |
| OR | `\|` | `1010 \| 1100` | `1110` |
| XOR | `^` | `1010 ^ 1100` | `0110` |
| NOT | `~` | `~1010` | `0101` (inverts) |
| Left shift | `<<` | `1 << 3` | `1000` (= 8) |
| Right shift | `>>` | `1000 >> 2` | `10` (= 2) |

### Essential Bit Tricks

```python
# Check if number is even/odd
n & 1 == 0   # even
n & 1 == 1   # odd

# Check if nth bit is set
(n >> i) & 1  # or: n & (1 << i) != 0

# Set nth bit
n | (1 << i)

# Clear nth bit
n & ~(1 << i)

# Toggle nth bit
n ^ (1 << i)

# Check if power of 2
n > 0 and (n & (n - 1)) == 0

# Count set bits (Brian Kernighan's)
count = 0
while n:
    n &= n - 1   # removes lowest set bit
    count += 1

# Get lowest set bit
lowest = n & (-n)

# XOR properties
a ^ a = 0       # same numbers cancel
a ^ 0 = a       # XOR with 0 is identity
a ^ b ^ a = b   # find single number in pairs
```

### Classic Problem: Single Number

Every element appears twice except one. Find it.

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

Why: all pairs XOR to 0, leaving only the unique number.

### Classic Problem: Number of 1 Bits

```python
def hamming_weight(n):
    count = 0
    while n:
        count += 1
        n &= n - 1
    return count
```

### When Bit Manipulation Appears

- Problems explicitly about binary numbers
- Finding single/unique elements in duplicated arrays
- Subsets generation (each bit represents include/exclude)
- Flags and state compression in DP
- Permissions and feature flags

---

# Quick Reference: Complexity Cheat Sheet

## Data Structure Operations

| Data Structure | Access | Search | Insert | Delete | Space |
|---------------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Sorted Array | O(1) | O(log n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* | O(n) |
| Hash Map | N/A | O(1) | O(1) | O(1) | O(n) |
| BST (balanced) | N/A | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | N/A | O(n) | O(log n) | O(log n) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Trie | N/A | O(m) | O(m) | O(m) | O(n·m) |

\* At known position. m = key/word length.

## Algorithm Complexities

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Binary Search | O(log n) | O(1) | Sorted input required |
| BFS/DFS | O(V+E) | O(V) | Graph traversal |
| Merge Sort | O(n log n) | O(n) | Stable, guaranteed |
| Quick Sort | O(n log n) avg | O(log n) | In-place, fastest in practice |
| Heap Sort | O(n log n) | O(1) | In-place, not stable |
| Dijkstra | O((V+E) log V) | O(V) | No negative weights |
| Topological Sort | O(V+E) | O(V) | DAG only |
| Union-Find | O(α(n)) ≈ O(1) | O(n) | Per operation, amortized |

## Common Time Complexity Intuitions

| Complexity | Name | Typical Pattern | n=10⁶ ops |
|-----------|------|----------------|-----------|
| O(1) | Constant | Hash lookup, array access | 1 |
| O(log n) | Logarithmic | Binary search, balanced BST | 20 |
| O(n) | Linear | Single pass, hash map build | 10⁶ |
| O(n log n) | Linearithmic | Sorting, heap operations | 2×10⁷ |
| O(n²) | Quadratic | Nested loops, brute force pairs | 10¹² (too slow) |
| O(2ⁿ) | Exponential | Subsets, brute force recursion | ∞ |
| O(n!) | Factorial | Permutations | ∞ |

**Interview rule of thumb**: ~10⁸ operations per second. If n ≤ 10⁴, O(n²) is fine. If n ≤ 10⁶, need O(n log n) or better. If n ≤ 10⁹, need O(n) or O(log n).

---

*Master these fundamentals and patterns, and you'll be equipped to handle any coding problem in the phone screen. Focus on understanding WHY each approach works, not just memorizing solutions.*
