# Hogwarts Database Manager
# --------------------------
# This script manages Students, Courses, and Admins for Hogwarts using SQLite.
# Features: Add, View, and Delete records with logging events.

import os
import sqlite3
import logger as l

# --- Set up database connection ---
con = sqlite3.connect('Hogwarts.db')
cur = con.cursor()


# --- Create tables if they don't exist ---
create_admin_table = """CREATE TABLE IF NOT EXISTS HogwartAdmin (
    WizardID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    CourseID INT
);"""

create_course_table = """CREATE TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL
);"""

create_student_table = """CREATE TABLE IF NOT EXISTS Students (
    WizardID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    House TEXT NOT NULL,
    Year INTEGER NOT NULL
);"""

# --- Executes create table queries ---
cur.execute(create_admin_table)
cur.execute(create_course_table)
cur.execute(create_student_table)

# --- SQL Insert Statements ---
insert_admin_query = "INSERT INTO HogwartAdmin (Name, CourseID) VALUES (?,?);"
insert_student_query = "INSERT INTO Students (Name, House, Year) VALUES (?, ?, ?);"
insert_course_query = "INSERT INTO Courses (CourseName) VALUES (?);"

# --- Predefined queries ---
student_list_query = "SELECT Name, House, Year FROM Students;"
student_count_query = "SELECT COUNT(*) FROM Students;"
admin_list_query = "SELECT WizardID, Name, CourseID FROM HogwartAdmin;"
course_list_query = "SELECT CourseID, CourseName FROM Courses;"

# --- Pre-filled data ---
course_data = [
    ('Astronomy',), ('Charms',), ('Defense Against the Dark Arts',), ('Flying',),
    ('Herbology',), ('History of Magic',), ('Potions',), ('Transfiguration',),
    ('Care of Magical Creatures',), ('Divination',), ('Muggle Studies',),
    ('Study of Ancient Runes',), ('Alchemy',), ('Other Staff',),
]

admin_data = [
    ('Albus Dumbledore', 14), ('Minerva McGonagall', 8), ('Severus Snape', 7),
    ('Filius Flitwick', 2), ('Pomona Sprout', 5), ('Rubeus Hagrid', 9),
    ('Gilderoy Lockhart', 10), ('Horace Slughorn', 11), ('Sybill Trelawney', 12),
    ('Remus Lupin', 13), ('Alastor Moody', 4), ('Firenze', 1),
]

# --- Insert initial course data if table is empty ---
try:
    cur.execute("SELECT COUNT(*) FROM Courses;")
    if cur.fetchone()[0] == 0:
        cur.executemany(insert_course_query, course_data)
except Exception as e:
    print("An error occurred while populating the Courses table. Please check the hogwarts_error_log file for more information.")
    l.log_error("Failed to populate the Courses table", details={"Exception": str(e)})

# --- Insert initial admin data if table is empty ---
try:
    cur.execute("SELECT COUNT(*) FROM HogwartAdmin;")
    if cur.fetchone()[0] == 0:
        cur.executemany(insert_admin_query, admin_data)
except Exception as e:
    print("An error occurred while populating the HogwartAdmin table. Please check the hogwarts_error_log file for more information.")
    l.log_error("Failed to populate the HogwartAdmin table", details={"Exception": str(e)})

con.commit()

# --- Functions ---

def insert_student():
    # --- Adds a new student to the Students table ---
    try:
        name = input("Enter the student's name: ")
        year = input("Enter the student's year (1-7): ")
        house = input("Enter the student's house (Gryffindor, Slytherin, Hufflepuff, Ravenclaw): ")

        if year not in ['1', '2', '3', '4', '5', '6', '7']:
            print("Invalid year. Please enter a number between 1 and 7.")
            return
        elif house not in ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']:
            print("Invalid house. Please enter one of the four houses.")
            return
        else:
            cur.execute(insert_student_query, (name, house, year))
            con.commit()
            print(f"Student {name} added successfully!")
            l.log_event("Student Added!", {"Name": name, "House": house, "Year": year})
    except Exception as e:
        print("An error occurred while adding student data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to add student data", details={"Exception": str(e)})

def add_course():
    # --- Adds a new course to the Courses table ---
    try:
        course_name = input("Enter the course name: ")
        cur.execute(insert_course_query, (course_name,))
        con.commit()
        print(f"Course {course_name} added successfully!")
        l.log_event("Course Added!", {"Course Name": course_name})
    except Exception as e:
        print("An error occurred while adding course data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to add course data", details={"Exception": str(e)})

def insert_admin():
    # --- Adds a new admin/teacher to the HogwartAdmin table ---
    try:
        name = input("Enter the admin's name: ")
        course_id = input("Enter the course/occupation ID: ")
        cur.execute(insert_admin_query, (name, course_id))
        con.commit()
        print(f"Admin {name} added successfully!")
        l.log_event("Teacher Added!", {"Name": name, "Course ID": course_id})
    except Exception as e:
        print("An error occurred while adding admin data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to add admin data", details={"Exception": str(e)})

def all_students():
    # --- Lists all students in the database ---
    try:
        cur.execute("SELECT Name, House, Year FROM Students;")
        students = cur.fetchall()
        if students:
            print("List of all students:")
            for student in students:
                print(f"Name: {student[0]}, House: {student[1]}, Year: {student[2]}")
        else:
            print("No students found.")
    except Exception as e:
        print("An error occurred while iterating student data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to iterate student data", details={"Exception": str(e)})

def student_by_year():
    # --- Lists students filtered by year ---
    try:
        year = input("Enter the year (1-7): ")
        cur.execute("SELECT Name, House, Year FROM Students WHERE Year = ?;", (year,))
        students = cur.fetchall()
        if students:
            print(f"Students in Year {year}:")
            for student in students:
                print(f"Name: {student[0]}, House: {student[1]}, Year: {student[2]}")
        else:
            print(f"No students found in Year {year}.")
    except Exception as e:
        print("An error occurred while searching student data by year. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to search student data by year", details={"Exception": str(e)})

def student_by_house():
    # --- Lists students filtered by house ---
    try:
        house = input("Enter the house name: ")
        cur.execute("SELECT Name, House, Year FROM Students WHERE House = ?;", (house,))
        students = cur.fetchall()
        if students:
            print(f"Students in House {house}:")
            for student in students:
                print(f"Name: {student[0]}, House: {student[1]}, Year: {student[2]}")
        else:
            print("No students found in that house.")
    except Exception as e:
        print("An error occurred while searching student data by house. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to search student data by house", details={"Exception": str(e)})

def student_list():
    # --- Menu for listing students by different filters ---
    try:
        while True:
            print("1. View all students")
            print("2. View students by year")
            print("3. View students by house")
            print("4. Exit")

            student_choice = input("Enter your choice (1-4): ")
            if student_choice == "1":
                all_students()
            elif student_choice == "2":
                student_by_year()
            elif student_choice == "3":
                student_by_house()
            elif student_choice == "4":
                print("Exiting student list.")
                break
            else:
                print("Invalid choice. Please try again.")
                student_list()
    except Exception as e:
        print("An error occurred while accessing the student sorting menu. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to access student sorting menu", details={"Exception": str(e)})

def admin_list():
    # --- Lists all admins/teachers ---
    try:
        cur.execute(admin_list_query)
        admins = cur.fetchall()
        if admins:
            print("List of all admins:")
            for admin in admins:
                print(f"WizardID: {admin[0]}, Name: {admin[1]}, CourseID: {admin[2]}")
        else:
            print("No admins found.")
    except Exception as e:
        print("An error occurred while accessing admin data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to access admin list", details={"Exception": str(e)})

def course_list():
    # --- Lists all courses ---
    try:
        cur.execute(course_list_query)
        courses = cur.fetchall()
        if courses:
            print("List of all courses:")
            for course in courses:
                print(f"CourseID: {course[0]}, CourseName: {course[1]}")
        else:
            print("No courses found.")
    except Exception as e:
        print("An error occurred while accessing course data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to access course list", details={"Exception": str(e)})

def delete_record():
    # --- Allows the user to delete a record from Students, Courses, or HogwartAdmin ---
    print("Which table would you like to delete from?")
    print("1. Students")
    print("2. Courses")
    print("3. HogwartAdmin")
    choice = input("Enter the number corresponding to the table: ").strip()
    try:
        if choice == "1":
            # --- Delete student ---
            name = input("Enter the student's name you want to delete: ").strip()
            if not name:
                print("No name entered. Deletion cancelled.")
                return

            cur.execute("SELECT * FROM Students WHERE Name = ?;", (name,))
            student = cur.fetchone()
            if student:
                confirm = input(f"Are you sure you want to delete student '{name}'? (Y/N): ").strip().lower()
                if confirm == 'y' or confirm == 'Y':
                    cur.execute("DELETE FROM Students WHERE Name = ?;", (name,))
                    con.commit()
                    print(f"Student '{name}' deleted successfully!")
                    l.log_event("Student Deleted!", {"Name": name})
                else:
                    print("Deletion cancelled.")
            else:
                print(f"No student found with the name '{name}'.")

        elif choice == "2":
            # --- Delete course ---
            course_name = input("Enter the course name you want to delete: ").strip()
            if not course_name:
                print("No course name entered. Deletion cancelled.")
                return

            cur.execute("SELECT * FROM Courses WHERE CourseName = ?;", (course_name,))
            course = cur.fetchone()
            if course:
                confirm = input(f"Are you sure you want to delete course '{course_name}'? (Y/N): ").strip().lower()
                if confirm == 'y' or confirm == 'Y':
                    cur.execute("DELETE FROM Courses WHERE CourseName = ?;", (course_name,))
                    con.commit()
                    print(f"Course '{course_name}' deleted successfully.")
                    l.log_event("Course Deleted!", {"Course Name": course_name})
                else:
                    print("Deletion cancelled.")
            else:
                print(f"No course found with the name '{course_name}'.")

        elif choice == "3":
            # --- Delete admin ---
            name = input("Enter the admin's name you want to delete: ").strip()
            if not name:
                print("No admin name entered. Deletion cancelled.")
                return

            cur.execute("SELECT * FROM HogwartAdmin WHERE Name = ?;", (name,))
            admin = cur.fetchone()
            if admin:
                confirm = input(f"Are you sure you want to delete admin '{name}'? (Y/N): ").strip().lower()
                if confirm == 'y' or confirm == 'Y':
                    cur.execute("DELETE FROM HogwartAdmin WHERE Name = ?;", (name,))
                    con.commit()
                    print(f"Admin '{name}' deleted successfully!")
                    l.log_event("Admin Deleted!", {"Name": name})
                else:
                    print("Deletion cancelled.")
            else:
                print(f"No admin found with the name '{name}'.")
        else:
            print("Invalid choice. No records deleted.")
    except Exception as e:
        print("An error occurred while removing data. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to remove data", details={"Exception": str(e)})
