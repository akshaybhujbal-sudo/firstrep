"""
app.py
======
Flask Web Application for the Student Record Management System.

Serves as the Presentation and Controller layer, connecting user HTTP requests
to the in-memory Data Structure operations in `student_manager.py`.

Routes:
- GET  /                     -> Dashboard with stats and full student table
- GET, POST /add             -> Student insertion form and processing
- GET, POST /search          -> Linear search form and result card
- POST /delete/<int:roll_no> -> Record deletion (POST only)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from student_manager import (
    insert_student,
    search_student,
    delete_student,
    get_all_students
)

app = Flask(__name__)

# Development secret key loaded from environment variable with fallback
app.secret_key = os.environ.get("SECRET_KEY", "student-project-secret-key-dev-only")


@app.route("/")
def index():
    """
    Dashboard route.
    Retrieves all records from the dynamic array and passes them to the template.
    """
    students = get_all_students()
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    """
    Insert student route.
    GET:  Renders student insertion form.
    POST: Validates inputs, checks for duplicates, and appends to the array.
          Implements the Post/Redirect/Get (PRG) pattern.
    """
    if request.method == "POST":
        roll_text = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        branch = request.form.get("branch", "").strip()
        semester_text = request.form.get("semester", "").strip()

        # 1. Validation: Ensure all fields are provided
        if not all([roll_text, name, branch, semester_text]):
            flash("All fields are mandatory. Please fill in every field.", "error")
            return redirect(url_for("add_student"))

        # 2. Validation: Name length check
        if len(name) < 2 or len(name) > 100:
            flash("Student name must be between 2 and 100 characters.", "error")
            return redirect(url_for("add_student"))

        # 3. Validation: Positive integer checks for roll_no and semester
        try:
            roll_no = int(roll_text)
            semester = int(semester_text)

            if roll_no <= 0:
                flash("Roll number must be a positive integer greater than 0.", "error")
                return redirect(url_for("add_student"))

            if semester < 1 or semester > 12:
                flash("Semester must be between 1 and 12.", "error")
                return redirect(url_for("add_student"))

        except ValueError:
            flash("Roll number and semester must be valid positive whole numbers.", "error")
            return redirect(url_for("add_student"))

        # 4. Insert into dynamic array
        success = insert_student(roll_no, name, branch, semester)

        if success:
            flash(f"Student '{name}' (Roll No: {roll_no}) added successfully!", "success")
            # Post/Redirect/Get pattern
            return redirect(url_for("index"))
        else:
            flash(f"Error: A student with Roll Number {roll_no} already exists.", "error")
            return redirect(url_for("add_student"))

    return render_template("add_student.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search student route.
    GET:  Renders search form.
    POST: Executes linear search by roll number and displays matching record or error.
    """
    student = None
    searched = False
    searched_roll = ""

    if request.method == "POST":
        roll_text = request.form.get("roll_no", "").strip()
        searched_roll = roll_text

        # Validate search input
        if not roll_text:
            flash("Please enter a roll number to search.", "error")
        elif not roll_text.isdigit() or int(roll_text) <= 0:
            flash("Please enter a valid positive integer for the roll number.", "error")
        else:
            roll_no = int(roll_text)
            student = search_student(roll_no)
            searched = True

            if student is None:
                flash(f"No student record found with Roll Number {roll_no}.", "error")

    return render_template(
        "search_student.html",
        student=student,
        searched=searched,
        searched_roll=searched_roll
    )


@app.route("/delete/<int:roll_no>", methods=["POST"])
def delete(roll_no):
    """
    Delete student route (POST only).
    Locates and removes the record from the in-memory array.
    """
    if delete_student(roll_no):
        flash(f"Student record with Roll Number {roll_no} deleted successfully.", "success")
    else:
        flash(f"Cannot delete: Student with Roll Number {roll_no} was not found.", "error")

    # Post/Redirect/Get pattern back to dashboard
    return redirect(url_for("index"))


# Explicitly handle GET on /delete/<roll_no> to reject non-POST deletion requests
@app.route("/delete/<int:roll_no>", methods=["GET"])
def delete_get_rejected(roll_no):
    """
    Rejects accidental or unauthorized GET deletion requests to enforce safe HTTP method semantics.
    """
    flash("Deletion must be performed via a POST request.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() in ["true", "1"]
    print("=" * 60)
    print(" Student Record Management System — Python DS Mini Project")
    print(" Running locally on http://127.0.0.1:5000")
    print(" Storage: In-memory dynamic array (Python list)")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
