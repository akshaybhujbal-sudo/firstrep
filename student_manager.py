"""
student_manager.py
==================
Core Data Structure Module for the Student Record Management System.

Academic Purpose:
-----------------
Demonstrates fundamental operations on Dynamic Arrays (Python lists) and Linear Search:
1. Insertion (append to dynamic array) - O(1) amortized, O(n) with duplicate check.
2. Searching (Linear Search) - O(n) worst/average case, O(1) best case.
3. Deletion (Linear search + pop/shift) - O(n) worst/average case.
4. Traversal (Display all records) - O(n).

Data Structure:
---------------
- The primary storage is `students`, an in-memory Python list serving as a dynamic array.
- Each student is an element in the array, structured as a dictionary:
    {
        "roll_no": int,     # Unique identifier (key for search/delete)
        "name": str,        # Student full name
        "branch": str,      # Academic department
        "semester": int     # Current semester of study
    }
"""

# Primary in-memory storage: Python list acting as a dynamic array.
# Memory Note: Records reside in RAM and reset whenever the application restarts.
students = []


def insert_student(roll_no, name, branch, semester):
    """
    Inserts a new student record into the dynamic array.

    Algorithm & Complexity:
    -----------------------
    1. First traverses the array using `search_student(roll_no)` to check
       for duplicates. This search takes O(n) time.
    2. If duplicate is found, returns False.
    3. If unique, constructs the student record and appends it to the end
       of the list. `list.append()` runs in amortized O(1) time because
       Python dynamically reallocates buffer capacity in geometric chunks.
    Total Time Complexity: O(n) due to duplicate validation.
    Space Complexity: O(1) auxiliary space (O(n) overall storage).
    """
    # Reject duplicate roll numbers by scanning the array first
    if search_student(roll_no) is not None:
        return False

    student = {
        "roll_no": int(roll_no),
        "name": str(name).strip(),
        "branch": str(branch).strip(),
        "semester": int(semester)
    }

    # Dynamic array insertion at the end: amortized O(1)
    students.append(student)
    return True


def search_student(roll_no):
    """
    Searches for a student by roll number using Linear Search.

    Algorithm & Complexity:
    -----------------------
    Sequentially traverses each element in the `students` list from index 0
    to len(students) - 1. Compares each record's "roll_no" with the target.
    - Best Case: O(1) if target is at index 0.
    - Worst Case: O(n) if target is at the last index or not present.
    - Average Case: O(n) for n elements.
    Auxiliary Space Complexity: O(1).
    """
    target = int(roll_no)
    for student in students:
        if student["roll_no"] == target:
            return student  # Target found

    return None  # Target not found after complete traversal


def delete_student(roll_no):
    """
    Deletes a student record by roll number.

    Algorithm & Complexity:
    -----------------------
    1. Linear scan to locate the index of the student with the matching roll_no.
       Takes O(n) time.
    2. Once found, calls `students.pop(index)`.
       In a dynamic array, removing an element at `index` requires shifting all
       subsequent elements (from index + 1 to n - 1) one slot to the left
       to maintain contiguous memory.
       This shift takes O(n - index) time.
    Total Time Complexity: O(n).
    Auxiliary Space Complexity: O(1).
    """
    target = int(roll_no)
    for index, student in enumerate(students):
        if student["roll_no"] == target:
            # pop(index) removes element and shifts subsequent elements left
            students.pop(index)
            return True

    return False  # Record not found


def get_all_students():
    """
    Returns all student records in the dynamic array.

    Algorithm & Complexity:
    -----------------------
    Traverses and returns the list of students for rendering.
    Time Complexity: O(1) to return reference / O(n) when iterated for rendering.
    Space Complexity: O(1) auxiliary space.
    """
    return students


def clear_all_students():
    """
    Resets the in-memory dynamic array to an empty list.
    Helper function used for clean unit testing and test isolation.
    """
    global students
    students.clear()
