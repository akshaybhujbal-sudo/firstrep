# ALGORITHM ANALYSIS & DRY RUN MANUAL

## Student Record Management System — Dynamic Arrays & Linear Search

This document provides a formal mathematical and algorithmic examination of the core data structure operations implemented in `student_manager.py`. It includes pseudocode, asymptotic analysis, memory layout diagrams, and dry runs with sample roll numbers **101**, **102**, and **103**.

---

## 1. Memory Representation: The Dynamic Array

In Python, the list `students = []` is represented under CPython as a `PyListObject`. It contains:
- `ob_item`: A pointer to a contiguous block of pointers, each pointing to a `PyObject` (the student dictionary).
- `allocated`: The total number of elements the current allocated memory block can hold.
- `ob_size`: The current number of elements logically in the array (`len(students)`).

### Physical Memory Diagram
```
students (PyListObject)
┌──────────────┬──────────────┬──────────────┐
│ ob_size: 3   │ allocated: 4 │ ob_item: ────┼───┐
└──────────────┴──────────────┴──────────────┘   │
                                                 ▼
               Contiguous Pointer Array in Memory (Heap):
               ┌──────────────┬──────────────┬──────────────┬──────────────┐
               │   Index 0    │   Index 1    │   Index 2    │   Index 3    │
               │ Pointer 0x01 │ Pointer 0x02 │ Pointer 0x03 │    [NULL]    │
               └──────┬───────┴──────┬───────┴──────┬───────┴──────────────┘
                      │              │              │
                      ▼              ▼              ▼
                 {Roll: 101,    {Roll: 102,    {Roll: 103,
                  Name: Alice}   Name: Bob}     Name: Charlie}
```

---

## 2. Operation-by-Operation Algorithmic Analysis

### Operation 1: Linear Search (`search_student`)

#### Mathematical Formulation
Given an array $A = [s_0, s_1, \dots, s_{n-1}]$ of $n$ student records and a target key $k$:
$$
\text{LinearSearch}(A, k) =
\begin{cases}
s_i & \text{if } \exists i \in [0, n-1] \text{ such that } s_i.\text{roll\_no} = k \\
\text{NIL} & \text{otherwise}
\end{cases}
$$

#### Pseudocode
```text
FUNCTION search_student(target_roll):
    INPUT: integer target_roll
    OUTPUT: dictionary record OR None

    n = LENGTH(students)
    FOR index FROM 0 TO n - 1 DO:
        current_student = students[index]
        IF current_student["roll_no"] == target_roll THEN:
            RETURN current_student       // Target located
        END IF
    END FOR

    RETURN None                          // Exhaustive search completed with no match
END FUNCTION
```

#### Asymptotic Complexity
- **Best Case ($\Omega(1)$):** The target key resides at index $0$. Only $1$ comparison is executed.
- **Worst Case ($O(n)$):** The target key is at index $n-1$ or does not exist in the array. Exactly $n$ comparisons are made.
- **Average Case ($\Theta(n)$):** Assuming a uniform probability distribution $P(i) = \frac{1}{n}$ of the target being at index $i$:
  $$
  T_{\text{avg}}(n) = \sum_{i=1}^{n} i \cdot \frac{1}{n} = \frac{1}{n} \cdot \frac{n(n+1)}{2} = \frac{n+1}{2} \in \Theta(n)
  $$
- **Space Complexity:** $O(1)$ auxiliary space.

---

### Operation 2: Insertion (`insert_student`)

#### Pseudocode
```text
FUNCTION insert_student(roll_no, name, branch, semester):
    INPUT: integer roll_no, string name, string branch, integer semester
    OUTPUT: boolean (True if inserted, False if duplicate rejected)

    // Step 1: Duplicate check via Linear Search
    existing_record = search_student(roll_no)
    IF existing_record is not None THEN:
        RETURN False                     // Duplicate roll number rejected
    END IF

    // Step 2: Record creation
    student = {
        "roll_no": roll_no,
        "name": name,
        "branch": branch,
        "semester": semester
    }

    // Step 3: Append to dynamic array
    APPEND(students, student)
    RETURN True
END FUNCTION
```

#### Asymptotic Complexity
- **Duplicate Validation Phase:** $T_{\text{search}}(n) \in O(n)$ time.
- **Array Append Phase:** $T_{\text{append}} \in O(1)$ amortized time.
- **Total Time Complexity:**
  $$
  T_{\text{insert}}(n) = T_{\text{search}}(n) + T_{\text{append}} = O(n) + O(1) = O(n)
  $$
- **Space Complexity:** $O(1)$ auxiliary space ($O(n)$ overall data structure storage).

---

### Operation 3: Deletion (`delete_student`)

#### Pseudocode
```text
FUNCTION delete_student(target_roll):
    INPUT: integer target_roll
    OUTPUT: boolean (True if deleted, False if not found)

    n = LENGTH(students)
    target_index = -1

    // Step 1: Locate the target index using Linear Search
    FOR i FROM 0 TO n - 1 DO:
        IF students[i]["roll_no"] == target_roll THEN:
            target_index = i
            BREAK
        END IF
    END FOR

    IF target_index == -1 THEN:
        RETURN False                     // Record does not exist
    END IF

    // Step 2: Pop and shift elements left
    // Equivalent to C-level:
    // for (j = target_index; j < n - 1; j++) students[j] = students[j+1];
    POP(students, target_index)

    RETURN True
END FUNCTION
```

#### Memory Shift Analysis
When deleting at index $i$, all $(n - 1 - i)$ elements to the right must shift left by one slot:
- **Best Case ($\Omega(1)$):** Deleting the last element ($i = n-1$). Number of shifts $= 0$. (Finding it still takes $O(n)$ without an index reference).
- **Worst Case ($O(n)$):** Deleting the first element ($i = 0$). Number of shifts $= n - 1$.
- **Total Deletion Complexity:** Search $O(n)$ + Shift $O(n) = O(n)$.
- **Space Complexity:** $O(1)$ auxiliary space.

---

### Operation 4: Array Traversal (`get_all_students`)

#### Asymptotic Complexity
- Returns the list reference: $O(1)$.
- Jinja2 HTML rendering loop visits every element from $0 \dots n-1$:
  $$
  T_{\text{traverse}}(n) = c \cdot n \in \Theta(n)
  $$
- Auxiliary Space: $O(1)$.

---

## 3. Step-by-Step Dry Runs with Sample Data

Let us trace the system execution through an 8-step lifecycle using sample roll numbers **101**, **102**, and **103**.

---

### Trace 1: Insert Student 101
- **Input:** `roll_no = 101, name = "Alice Brown", branch = "CSE", semester = 4`
- **Initial Array:** `students = []` ($n = 0$)

| Step | Operation | Condition Evaluated | State of Array | Result |
|---|---|---|---|---|
| 1.1 | `search_student(101)` | Array is empty; loop does not run | `[]` | Returns `None` |
| 1.2 | Duplicate check | `existing is None` $\rightarrow$ True | `[]` | Proceed |
| 1.3 | Create dictionary | `{roll_no: 101, name: "Alice Brown", ...}` | `[]` | Dict in RAM |
| 1.4 | `students.append(...)` | Append at index 0 | `[{101: Alice}]` | Length becomes 1 |
| 1.5 | Finish | — | `[{101: Alice}]` | Returns `True` |

---

### Trace 2: Insert Student 102
- **Input:** `roll_no = 102, name = "Bob Smith", branch = "AI-ML", semester = 2`
- **Initial Array:** `students = [{101: Alice}]` ($n = 1$)

| Step | Operation | Condition Evaluated | State of Array | Result |
|---|---|---|---|---|
| 2.1 | `search_student(102)` | Check index 0: `101 == 102` $\rightarrow$ False | `[{101: Alice}]` | Loop ends |
| 2.2 | Search result | Loop ended without match | `[{101: Alice}]` | Returns `None` |
| 2.3 | Duplicate check | `existing is None` $\rightarrow$ True | `[{101: Alice}]` | Proceed |
| 2.4 | `students.append(...)` | Append at index 1 | `[{101: Alice}, {102: Bob}]` | Length becomes 2 |
| 2.5 | Finish | — | `[{101: Alice}, {102: Bob}]` | Returns `True` |

---

### Trace 3: Insert Student 103
- **Input:** `roll_no = 103, name = "Charlie Davis", branch = "IT", semester = 6`
- **Initial Array:** `students = [{101: Alice}, {102: Bob}]` ($n = 2$)

| Step | Operation | Condition Evaluated | State of Array | Result |
|---|---|---|---|---|
| 3.1 | `search_student(103)` | Index 0: `101 == 103` $\rightarrow$ False<br>Index 1: `102 == 103` $\rightarrow$ False | `[{101}, {102}]` | Loop ends |
| 3.2 | Duplicate check | Returns `None` | `[{101}, {102}]` | Proceed |
| 3.3 | `students.append(...)` | Append at index 2 | `[{101}, {102}, {103}]` | Length becomes 3 |
| 3.4 | Finish | — | `[{101}, {102}, {103}]` | Returns `True` |

---

### Trace 4: Duplicate Insertion Attempt (Roll No: 101)
- **Input:** `roll_no = 101, name = "Alice Clone", branch = "IT", semester = 1`
- **Initial Array:** `students = [{101: Alice}, {102: Bob}, {103: Charlie}]` ($n = 3$)

| Step | Operation | Condition Evaluated | State of Array | Result |
|---|---|---|---|---|
| 4.1 | `search_student(101)` | Check index 0: `students[0].roll_no == 101` $\rightarrow$ **MATCH FOUND!** | `[{101}, {102}, {103}]` | Returns `students[0]` |
| 4.2 | Duplicate check | `existing is not None` $\rightarrow$ **True (Duplicate detected)** | `[{101}, {102}, {103}]` | **Rejects insert** |
| 4.3 | Finish | Abort insertion | `[{101}, {102}, {103}]` | Returns `False` |

*Outcome:* The array remains completely unchanged with length 3. A flash error is displayed to the user.

---

### Trace 5: Linear Search for Existing Record (Target: 102)
- **Target:** `roll_no = 102`
- **Array:** `[Index 0: 101, Index 1: 102, Index 2: 103]`

| Loop Iteration | Array Index | Candidate Roll No | Comparison (`== 102`) | Action |
|:---:|:---:|:---:|:---:|---|
| Iteration 1 | `i = 0` | 101 | $101 == 102 \rightarrow$ False | Continue to next index |
| Iteration 2 | `i = 1` | 102 | $102 == 102 \rightarrow$ **TRUE** | **Terminate loop; return record!** |

- **Total Comparisons Made:** 2
- **Result:** Successfully returned `{roll_no: 102, name: "Bob Smith", ...}`.

---

### Trace 6: Linear Search for Nonexistent Record (Target: 999)
- **Target:** `roll_no = 999`
- **Array:** `[Index 0: 101, Index 1: 102, Index 2: 103]`

| Loop Iteration | Array Index | Candidate Roll No | Comparison (`== 999`) | Action |
|:---:|:---:|:---:|:---:|---|
| Iteration 1 | `i = 0` | 101 | $101 == 999 \rightarrow$ False | Continue |
| Iteration 2 | `i = 1` | 102 | $102 == 999 \rightarrow$ False | Continue |
| Iteration 3 | `i = 2` | 103 | $103 == 999 \rightarrow$ False | Continue |
| — | End of List | — | Loop exhausted ($i = n$) | Return `None` |

- **Total Comparisons Made:** 3 ($= n$, worst case)
- **Result:** Returns `None`. The UI presents the not-found alert.

---

### Trace 7: Delete Middle Record (Roll No: 102) Demonstrating Memory Shift
- **Target:** `roll_no = 102`
- **Initial Array:** `[Index 0: 101, Index 1: 102, Index 2: 103]` ($n = 3$)

#### Step 1: Locating Index
- Check `i = 0`: `101 == 102` (False)
- Check `i = 1`: `102 == 102` (True, target found at `index = 1`)

#### Step 2: Contiguous Memory Shift during `pop(1)`
```
Before pop:
Index 0: [ 101 ]
Index 1: [ 102 ]  <-- TARGET TO REMOVE
Index 2: [ 103 ]

Memory Shift:
Slot 1 receives pointer from Slot 2:  students[1] = students[2]  (Record 103 shifts left)

After pop:
Index 0: [ 101 ]
Index 1: [ 103 ]  <-- (Was previously at index 2)
Length:  2
```

- **Result:** Returns `True`. Length decrements from 3 to 2.

---

### Trace 8: Traversal of Final Array
- **Array:** `[Index 0: 101, Index 1: 103]` ($n = 2$)

| Render Step | Table Row | Rendered Data |
|:---:|:---:|---|
| Row 1 | `index = 0` | `Roll No: #101 \| Name: Alice Brown \| Branch: CSE \| Sem: 4` |
| Row 2 | `index = 1` | `Roll No: #103 \| Name: Charlie Davis \| Branch: IT \| Sem: 6` |

- Total table rows rendered: 2.
- Dashboard counter dynamically displays **Total Students: 2**.

---

## 4. Complexity Comparison Matrix

| Algorithm | Best-Case Time | Worst-Case Time | Space Complexity | Why It Was Chosen |
|---|---|---|---|---|
| **Dynamic Array Append** | $\Omega(1)$ | $O(n)$ (Buffer resize) | $O(1)$ | Direct Python list implementation; amortized $O(1)$ efficiency. |
| **Linear Search** | $\Omega(1)$ | $O(n)$ | $O(1)$ | Academic clarity; does not require presorted array. |
| **Duplicate Checking** | $\Omega(1)$ | $O(n)$ | $O(1)$ | Guarantees entity integrity in primary key without database constraints. |
| **Deletion with Shift** | $\Omega(1)$ (Last item) | $O(n)$ (First/Middle) | $O(1)$ | Illustrates how contiguous array memory is maintained. |
| **Binary Search (Alternative)** | $\Omega(1)$ | $O(\log n)$ | $O(1)$ | *Not chosen* because it requires maintaining strict sort order on every insert. |
| **Hash Table Lookup (Alternative)** | $\Omega(1)$ | $O(n)$ | $O(n)$ | *Not chosen* because it bypasses fundamental array iteration teaching goals. |
