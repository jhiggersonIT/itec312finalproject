# Hogwarts Main Application
# --------------------------
# This script launches the Hogwarts Management System GUI.
# Features: Access to add, view, and delete students, teachers, and courses.


import database_design as d
from gui import HogwartsGUI
import logger as l


def run_terminal():
    print("\nHogwarts School of Witchcraft and Wizardry")
    print("Welcome to the Student/Teacher Management System")
    print("=========================================")
    print("Student/Teacher Management System")
    print("1. Add a Student")
    print("2. Add a Teacher")
    print("3. Add a Course")
    print("4. View all Students")
    print("5. View all Admins")
    print("6. View all Courses")
    print("7. Delete a Record")
    print("8. Exit")

    try:
        validation = True
        while validation:
            start = input("Enter your choice (1-8): ")
            if start   == "1":
                d.insert_student()
            elif start == "2":
                d.insert_admin()
            elif start == "3":
                d.add_course()
            elif start == "4":
                d.student_list()
            elif start == "5":
                d.admin_list()
            elif start == "6":
                d.course_list()
            elif start == "7":
                d.delete_record()
            elif start == "8":
                validation = False
                print("Exiting the program.")
            else:
                print("Invalid choice. Please try again.")
                run_terminal()
    except Exception as e:
        print("An error occurred while accessing terminal menu. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to access terminal menu", details={"Exception": str(e)})

def main():
    print("\nWelcome to Hogwarts Management System")
    print("=========================================")
    print("Choose an interface:")
    print("1. Terminal")
    print("2. GUI")
    choice = input("Enter 1 or 2: ")

    try:
        if choice == "1":
            run_terminal()
        elif choice == "2":
            app = HogwartsGUI()
            app.run()
        else:
            print("Invalid option.")
            main()
    except Exception as e:    
        print("An error occurred while accessing visual menu. Please check the hogwarts_error_log file for more information.")
        l.log_error("Failed to access visual menu", details={"Exception": str(e)})

if __name__ == "__main__":
    main()
