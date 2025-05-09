# Hogwarts Database Manager - GUI
# -------------------------------
# This script provides a graphical user interface (GUI) to manage Students, Teachers, and Courses at Hogwarts.
# Features: Add, View, and Delete records, with integrated logging for all actions.


# - MODULES -
import os
import tkinter as tk
from tkinter import messagebox, ttk
import database_design as d
from logger import log_event

class HogwartsGUI:
    # - INITIALIZE THE GUI -
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hogwarts Management System")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.option_add("*Font", "Arial 11")

    # - STYLE FOR THE GUI - CONFIGURATION -
        style = ttk.Style()
        style.theme_use("clam")  # or 'default', 'alt', etc.
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Arial", 11))
        style.configure("TButton", background="#444", foreground="white", font=("Arial", 10, "bold"))
        style.map("TButton", background=[("active", "#555")])
        
        self.setup_main_menu()  # - Setup main menu
        self.center_window()    # - Center window

    # - START TKINTER MAIN LOOP -
    def run(self):
        self.root.mainloop()
        
    # - MAIN MENU -
    def setup_main_menu(self):
        ttk.Label(self.root, text="Hogwarts Management", font=("Arial", 16)).pack(pady=10)
        options = [ 
            ("Add Student"      , self.add_student),            # - OPTIONS FOR MAIN MENU -
            ("Add Teacher"      , self.add_teacher),
            ("Add Course"       , self.add_course),
            ("View Students"    , self.view_students),
            ("View Professors"  , self.view_professors),
            ("View Courses"     , self.view_courses),
            ("Delete Record"    , self.delete_record),
            ("Exit"             , self.root.quit)]

        for label, command in options:
            ttk.Button(self.root, text=label, width=30, command=command).pack(pady=5)   # - Buttons for the main menu

    # - CENTER WINDOW ON SCREEN -
    def center_window(self, width=400, height=500):             # V - FOR WINDOW POSITION - V
        screen_width  = self.root.winfo_screenwidth()                   #Width
        screen_height = self.root.winfo_screenheight()                  #Height
        x = int((screen_width  / 2) - (width / 2))                      #X coordinate
        y = int((screen_height / 2) - (height / 2))                     #Y coordinate
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # - ADD and SUBTMIT [ STUDENT ] -
    def add_student(self):
        fields = [("Name", ""), ("House", ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]), ("Year", "")]        # - Fields for student
        self.open_form("Add Student", fields, self.submit_student)
    
    def submit_student(self, inputs):
        name, house, year = inputs                                  
        if year not in ['1', '2', '3', '4', '5', '6', '7']:
            messagebox.showerror("Error", "Invalid year.")          # - - VALIDATION
            return
        if house not in ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']:
            messagebox.showerror("Error", "Invalid house.")         # - - VALIDATION
            return
        
        d.cur.execute(d.insert_student_query, (name, house, year))    # - - insert student into database
        d.con.commit()
        
        d.l.log_event("Student Added!", {"Name": name, "House": house, "Year": year})  # - - LOGGING
        messagebox.showinfo("Success", f"Student '{name}' added.")

    # - ADD and SUBMIT [ TEACHER ] -
    def add_teacher(self):
        self.open_form("Add Teacher", [("Name", ""), ("Course ID", "")], self.submit_teacher)   # - - Fields for teacher

    def submit_teacher(self, inputs):
        name, course_id = inputs
        
        d.cur.execute(d.insert_admin_query, (name, course_id))        # - - insert teacher into database
        d.con.commit()
        
        d.l.log_event("Teacher Added!", {"Name": name, "Course ID": course_id})        # - - LOGGING
        messagebox.showinfo("Success", f"Teacher '{name}' added.")

    # - ADD and SUBMIT [ COURSE ] -
    def add_course(self):
        self.open_form("Add Course", [("Course Name", "")], self.submit_course)                 # - - Fields for course

    def submit_course(self, inputs):
        course_name = inputs[0] 
        
        d.cur.execute(d.insert_course_query, (course_name,))          # - - insert course into database
        d.con.commit()
        
        d.l.log_event("Course Added!", {"Course Name": course_name})                   # - - LOGGING
        messagebox.showinfo("Success", f"Course '{course_name}' added.")

    
    # - FOR RECORD DELETION -
    def delete_record(self):
        delete_window = tk.Toplevel(self.root)                      # - - Creates new window for deleting
        delete_window.title("Delete Record")
        delete_window.geometry("500x150")
        delete_window.resizable(False, False)

        frame = ttk.Frame(delete_window, padding=10, style="TFrame")    # - - Frame for layout
        frame.pack(fill="both", expand=True)                            # - - Fill the window with the frame

        # - DROPDOWN BOX FOR TABLE SELECTION -
        ttk.Label(frame, text="Select Table:", style="TLabel").grid(row=0, column=0, padx=10, pady=10, sticky="e")      # - - Label for dropdown
        
        table_var      = tk.StringVar()
        table_dropdown = ttk.Combobox(frame, textvariable=table_var, state="readonly",
                                    values=["Students", "Courses", "HogwartAdmin"])                                     # - - Dropdown options
        table_dropdown.current(0)                      # - - default value
        table_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # - - ENTRY FOR NAME TO DELETE -
        ttk.Label(frame, text="Enter Name to Delete:", style="TLabel").grid(row=1, column=0, padx=10, pady=10, sticky="e")   # - - Label for entry
        
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        # - SUBMIT BUTTON FOR DELETION -
        def perform_deletion():
            table = table_var.get()                     # - - Get selected table
            name  = name_entry.get().strip()            # - - Get name from entry
            
            if not name:
                messagebox.showerror("Error", "Please enter a name.")       # - - VALIDATION
                return

            # - DELETE RECORD CONFIRMATION -
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{name}' from {table}?")
            if not confirm:         # - - Cancel Deletion
                messagebox.showinfo("Cancelled", "Deletion cancelled.")
                return

            try:
                if table   == "Students":
                    d.cur.execute("DELETE FROM Students WHERE Name = ?;", (name,))         # - - Delete student
                elif table == "Courses":
                    d.cur.execute("DELETE FROM Courses WHERE CourseName = ?;", (name,))    # - - Delete course
                elif table == "HogwartAdmin":
                    d.cur.execute("DELETE FROM HogwartAdmin WHERE Name = ?;", (name,))     # - - Delete teacher
                d.con.commit()

                messagebox.showinfo("Success", f"{table[:-1]} '{name}' deleted successfully.")  
                log_event(f"{table[:-1]} Deleted", {"Name": name})  # - - LOGGING
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")     # - - ERROR HANDLING

            delete_window.destroy()     # - - Closes deletion window
            
        # - BUTTON TO PERFORM DELETION -
        ttk.Button(frame, text="Delete", style="TButton", command=perform_deletion).grid(row=2, column=1, pady=20, sticky="e")  # - - Button for delete record

    # - CREATE NEW WINDOW WITH FIELDS FOR DATA ENTRY -
    def open_form(self, title, fields, callback):
        form    = tk.Toplevel(self.root)           # - - Creates new window for form
        form.title(title)
        form.geometry("300x150")
        form.resizable(False, False)
        entries = []                               # - - List to store entry fields

        for i, (label, default) in enumerate(fields):   # - - Enumerate through fields
            ttk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")      # - - Label for each field

            if isinstance(default, list):  # - - Dropdown box for options
                combo = ttk.Combobox(form, values=default, state="readonly")                    # - - Dropdown options
                combo.current(0)
                combo.grid(row=i, column=1, padx=10, pady=5)                    
                entries.append(combo)
                
            else:  # - - Regular text entry
                entry = ttk.Entry(form)
                entry.insert(0, default)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries.append(entry)
                
        # - SUBMIT BUTTON FOR FORM -
        def submit():
            inputs = [e.get() for e in entries]  # - - Get values from entry fields
            callback(inputs)    
            form.destroy()                       # - - Close form window

        ttk.Button(form, text="Submit", command=submit).grid(row=len(fields), column=1, pady=10)    # - - Button to submit form
    
    # - DISPLAY LIST OF STUDENTS, TEACHERS, OR COURSES -
    def display_list(self, title, data, headers):
        window = tk.Toplevel(self.root)             # - - Create new window for list display
        window.title(title)

        outer_frame = ttk.Frame(window, padding=10) # - - Padding
        outer_frame.pack(fill="both", expand=True)  # - - Fill the window with the frame
    
        for i, header in enumerate(headers):        # - - Enumerate through the headers
            ttk.Label(outer_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=10, pady=5)    # - - Header labels

        for r, row in enumerate(data, start=1):                                                 # - - Data rows
            for c, item in enumerate(row):          # - - Enumerate through EACH ITEM in the row
                ttk.Label(outer_frame, text=str(item)).grid(row=r, column=c, padx=10, pady=5)   # - - Data labels
                          
    def view_students(self):
        d.cur.execute(d.student_list_query)
        self.display_list("Students", d.cur.fetchall(), ["Name", "House", "Year"])             # - DISPLAY STUDENT LIST

    def view_professors(self):
        d.cur.execute(d.admin_list_query)
        self.display_list("Professors", d.cur.fetchall(), ["WizardID", "Name", "CourseID"])    # - DISPLAY ADMIN LIST

    def view_courses(self):
        d.cur.execute(d.course_list_query)
        self.display_list("Courses", d.cur.fetchall(), ["CourseID", "CourseName"])             # - DISPLAY COURSE LIST
