"""
test_student_manager.py
=======================
Automated Test Suite for Student Record Management System.

Covers:
1. Unit tests for core Data Structure operations in `student_manager.py` (Tests 1 - 10).
2. Integration & route tests for Flask web application in `app.py`.
"""

import unittest
import sys
import os

# Ensure parent directory is on sys.path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import student_manager
from app import app


class TestStudentManagerDataStructures(unittest.TestCase):
    """
    Unit test cases for the in-memory Dynamic Array and Linear Search algorithms.
    """

    def setUp(self):
        """Clean slate before every individual test case."""
        student_manager.clear_all_students()

    def tearDown(self):
        """Clean slate after every individual test case."""
        student_manager.clear_all_students()

    # Requirement 1: Inserting a valid student
    def test_01_insert_valid_student(self):
        result = student_manager.insert_student(101, "Alice Brown", "CSE", 4)
        self.assertTrue(result)
        students = student_manager.get_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["roll_no"], 101)
        self.assertEqual(students[0]["name"], "Alice Brown")
        self.assertEqual(students[0]["branch"], "CSE")
        self.assertEqual(students[0]["semester"], 4)

    # Requirement 2: Inserting multiple students
    def test_02_insert_multiple_students(self):
        self.assertTrue(student_manager.insert_student(101, "Alice Brown", "CSE", 4))
        self.assertTrue(student_manager.insert_student(102, "Bob Smith", "AI-ML", 2))
        self.assertTrue(student_manager.insert_student(103, "Charlie Davis", "IT", 6))
        students = student_manager.get_all_students()
        self.assertEqual(len(students), 3)
        self.assertEqual([s["roll_no"] for s in students], [101, 102, 103])

    # Requirement 3: Rejecting duplicate roll numbers
    def test_03_reject_duplicate_roll_number(self):
        self.assertTrue(student_manager.insert_student(101, "Alice Brown", "CSE", 4))
        # Attempt to insert same roll number with different details
        duplicate_result = student_manager.insert_student(101, "Alice Clone", "IT", 1)
        self.assertFalse(duplicate_result)
        # Verify length remains 1
        self.assertEqual(len(student_manager.get_all_students()), 1)

    # Requirement 4: Searching for an existing student (Linear Search)
    def test_04_search_existing_student(self):
        student_manager.insert_student(101, "Alice Brown", "CSE", 4)
        student_manager.insert_student(102, "Bob Smith", "AI-ML", 2)
        
        found = student_manager.search_student(102)
        self.assertIsNotNone(found)
        self.assertEqual(found["roll_no"], 102)
        self.assertEqual(found["name"], "Bob Smith")
        self.assertEqual(found["branch"], "AI-ML")

    # Requirement 5: Searching for a nonexistent student
    def test_05_search_nonexistent_student(self):
        student_manager.insert_student(101, "Alice Brown", "CSE", 4)
        not_found = student_manager.search_student(999)
        self.assertIsNone(not_found)

    # Requirement 6: Deleting an existing student
    def test_06_delete_existing_student(self):
        student_manager.insert_student(101, "Alice Brown", "CSE", 4)
        student_manager.insert_student(102, "Bob Smith", "AI-ML", 2)
        student_manager.insert_student(103, "Charlie Davis", "IT", 6)

        deleted = student_manager.delete_student(102)
        self.assertTrue(deleted)
        
        students = student_manager.get_all_students()
        self.assertEqual(len(students), 2)
        self.assertEqual([s["roll_no"] for s in students], [101, 103])
        # Ensure searching for deleted student returns None
        self.assertIsNone(student_manager.search_student(102))

    # Requirement 7: Deleting a nonexistent student
    def test_07_delete_nonexistent_student(self):
        student_manager.insert_student(101, "Alice Brown", "CSE", 4)
        deleted = student_manager.delete_student(888)
        self.assertFalse(deleted)
        self.assertEqual(len(student_manager.get_all_students()), 1)

    # Requirement 8: Deleting the only record
    def test_08_delete_only_record(self):
        student_manager.insert_student(101, "Solo Student", "CSE", 1)
        self.assertEqual(len(student_manager.get_all_students()), 1)
        
        deleted = student_manager.delete_student(101)
        self.assertTrue(deleted)
        self.assertEqual(len(student_manager.get_all_students()), 0)

    # Requirement 9: Operating on an empty list
    def test_09_operations_on_empty_list(self):
        # Empty list searching
        self.assertIsNone(student_manager.search_student(101))
        # Empty list deleting
        self.assertFalse(student_manager.delete_student(101))
        # Empty list traversal
        self.assertEqual(student_manager.get_all_students(), [])

    # Requirement 10: Ensuring student count changes correctly
    def test_10_student_count_transitions(self):
        self.assertEqual(len(student_manager.get_all_students()), 0)
        
        student_manager.insert_student(101, "Student 1", "CSE", 1)
        self.assertEqual(len(student_manager.get_all_students()), 1)

        student_manager.insert_student(102, "Student 2", "IT", 2)
        self.assertEqual(len(student_manager.get_all_students()), 2)

        # Duplicate attempt does not change count
        student_manager.insert_student(101, "Student 1 Duplicate", "CSE", 1)
        self.assertEqual(len(student_manager.get_all_students()), 2)

        # Delete decreases count
        student_manager.delete_student(101)
        self.assertEqual(len(student_manager.get_all_students()), 1)

        student_manager.delete_student(102)
        self.assertEqual(len(student_manager.get_all_students()), 0)


class TestFlaskRoutesAndIntegration(unittest.TestCase):
    """
    Integration tests verifying Flask routes, HTTP methods, PRG redirects, and HTML rendering.
    """

    def setUp(self):
        student_manager.clear_all_students()
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        student_manager.clear_all_students()

    def test_dashboard_empty_state(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Record Management System", response.data)
        self.assertIn(b"No student records found in memory", response.data)
        self.assertIn(b"Dynamic Array", response.data)

    def test_add_student_get_form(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Insert Student Record", response.data)
        self.assertIn(b"Roll Number", response.data)

    def test_add_student_post_success(self):
        response = self.client.post('/add', data={
            'roll_no': '201',
            'name': 'Grace Hopper',
            'branch': 'Computer Science (CSE)',
            'semester': '6'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"added successfully!", response.data)
        self.assertIn(b"Grace Hopper", response.data)
        self.assertIn(b"201", response.data)

    def test_add_student_post_duplicate(self):
        # Insert initial
        student_manager.insert_student(201, "Grace Hopper", "CSE", 6)
        # Attempt duplicate
        response = self.client.post('/add', data={
            'roll_no': '201',
            'name': 'Duplicate Grace',
            'branch': 'CSE',
            'semester': '6'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"already exists", response.data)

    def test_add_student_post_missing_fields(self):
        response = self.client.post('/add', data={
            'roll_no': '201',
            'name': '',
            'branch': 'CSE',
            'semester': '6'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All fields are mandatory", response.data)

    def test_add_student_post_invalid_numbers(self):
        # Negative roll number
        response = self.client.post('/add', data={
            'roll_no': '-5',
            'name': 'Invalid Roll',
            'branch': 'CSE',
            'semester': '4'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"must be a positive integer greater than 0", response.data)

        # Invalid semester (> 12)
        response = self.client.post('/add', data={
            'roll_no': '202',
            'name': 'Invalid Sem',
            'branch': 'CSE',
            'semester': '15'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Semester must be between 1 and 12", response.data)

    def test_search_get_and_post_found(self):
        student_manager.insert_student(301, "Ada Lovelace", "Information Technology (IT)", 3)

        # GET search page
        get_res = self.client.get('/search')
        self.assertEqual(get_res.status_code, 200)

        # POST search found
        post_res = self.client.post('/search', data={'roll_no': '301'})
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"Match Found", post_res.data)
        self.assertIn(b"Ada Lovelace", post_res.data)

    def test_search_post_not_found(self):
        post_res = self.client.post('/search', data={'roll_no': '777'})
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"No Match Found", post_res.data)
        self.assertIn(b"No student record found with Roll Number 777", post_res.data)

    def test_search_post_invalid_input(self):
        post_res = self.client.post('/search', data={'roll_no': 'abc'})
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"Please enter a valid positive integer", post_res.data)

    def test_delete_post_success(self):
        student_manager.insert_student(401, "Alan Turing", "CSE", 8)
        self.assertEqual(len(student_manager.get_all_students()), 1)

        response = self.client.post('/delete/401', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"deleted successfully", response.data)
        self.assertEqual(len(student_manager.get_all_students()), 0)

    def test_delete_post_nonexistent(self):
        response = self.client.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cannot delete: Student with Roll Number 999 was not found", response.data)

    def test_delete_get_rejected(self):
        # Verification that GET requests are rejected
        response = self.client.get('/delete/101', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Deletion must be performed via a POST request", response.data)


if __name__ == '__main__':
    unittest.main()
