"""
Attendance Management System - Main Integrated Application
Run this file to start the application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, date
import sys

# ==================== CONFIGURATION ====================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change this to your MySQL password
    'database': 'attendance_system'
}

# ==================== COLOR SCHEME ====================
COLORS = {
    'primary': '#2C3E50',      # Dark Blue
    'secondary': '#3498DB',    # Bright Blue
    'success': '#27AE60',      # Green
    'danger': '#E74C3C',       # Red
    'warning': '#F39C12',      # Orange
    'light': '#ECF0F1',        # Light Gray
    'dark': '#34495E',         # Dark Gray
    'white': '#FFFFFF',
    'text_dark': '#2C3E50',
    'hover': '#5DADE2'
}

# ==================== DATABASE CLASS ====================
class Database:
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            messagebox.showerror("Database Error", f"Cannot connect to database: {e}")
            return None
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

# ==================== LOGIN WINDOW ====================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System - Login")
        self.root.geometry("1000x600")
        self.root.configure(bg=COLORS['light'])
        self.root.resizable(False, False)
        
        self.center_window()
        self.create_login_ui()
        self.is_login_mode = True
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_login_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Branding
        left_frame = tk.Frame(main_frame, bg=COLORS['primary'], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)
        
        branding_frame = tk.Frame(left_frame, bg=COLORS['primary'])
        branding_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(branding_frame, text="🎓", font=("Arial", 80), 
                bg=COLORS['primary'], fg=COLORS['white']).pack(pady=20)
        
        tk.Label(branding_frame, text="Attendance\nManagement\nSystem", 
                font=("Arial", 28, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white'], justify='center').pack()
        
        tk.Label(branding_frame, text="Track. Manage. Excel.", 
                font=("Arial", 14), bg=COLORS['primary'], 
                fg=COLORS['light']).pack(pady=10)
        
        # Right side - Login/Signup Form
        right_frame = tk.Frame(main_frame, bg=COLORS['white'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Form container
        form_frame = tk.Frame(right_frame, bg=COLORS['white'])
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        self.form_title = tk.Label(form_frame, text="Welcome Back!", 
                                   font=("Arial", 24, "bold"), 
                                   bg=COLORS['white'], fg=COLORS['primary'])
        self.form_title.pack(pady=(0, 10))
        
        self.form_subtitle = tk.Label(form_frame, text="Login to your account", 
                                      font=("Arial", 11), bg=COLORS['white'], 
                                      fg=COLORS['dark'])
        self.form_subtitle.pack(pady=(0, 30))
        
        # Username
        tk.Label(form_frame, text="Username", font=("Arial", 10, "bold"), 
                bg=COLORS['white'], fg=COLORS['text_dark'], 
                anchor='w').pack(fill=tk.X, padx=40)
        
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), 
                                       relief=tk.FLAT, bg=COLORS['light'])
        self.username_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
        
        # Password
        tk.Label(form_frame, text="Password", font=("Arial", 10, "bold"), 
                bg=COLORS['white'], fg=COLORS['text_dark'], 
                anchor='w').pack(fill=tk.X, padx=40)
        
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), 
                                       show="●", relief=tk.FLAT, 
                                       bg=COLORS['light'])
        self.password_entry.pack(fill=tk.X, padx=40, pady=(5, 10), ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Additional fields for signup (initially hidden)
        self.signup_fields_frame = tk.Frame(form_frame, bg=COLORS['white'])
        
        # Login button
        self.action_button = tk.Button(form_frame, text="LOGIN", 
                                       font=("Arial", 12, "bold"), 
                                       bg=COLORS['secondary'], fg=COLORS['white'], 
                                       relief=tk.FLAT, cursor='hand2',
                                       command=self.login)
        self.action_button.pack(fill=tk.X, padx=40, pady=(20, 10), ipady=10)
        
        # Toggle button
        toggle_frame = tk.Frame(form_frame, bg=COLORS['white'])
        toggle_frame.pack(pady=10)
        
        tk.Label(toggle_frame, text="Don't have an account?", 
                font=("Arial", 10), bg=COLORS['white'], 
                fg=COLORS['dark']).pack(side=tk.LEFT, padx=5)
        
        self.toggle_button = tk.Button(toggle_frame, text="Sign Up", 
                                       font=("Arial", 10, "bold"), 
                                       bg=COLORS['white'], 
                                       fg=COLORS['secondary'], 
                                       relief=tk.FLAT, cursor='hand2',
                                       command=self.toggle_mode)
        self.toggle_button.pack(side=tk.LEFT)
    
    def toggle_mode(self):
        if self.is_login_mode:
            self.form_title.config(text="Create Account")
            self.form_subtitle.config(text="Sign up for a new account")
            self.action_button.config(text="SIGN UP", command=self.signup)
            self.toggle_button.config(text="Login")
            self.show_signup_fields()
        else:
            self.form_title.config(text="Welcome Back!")
            self.form_subtitle.config(text="Login to your account")
            self.action_button.config(text="LOGIN", command=self.login)
            self.toggle_button.config(text="Sign Up")
            self.hide_signup_fields()
        
        self.is_login_mode = not self.is_login_mode
    
    def show_signup_fields(self):
        # Full Name
        tk.Label(self.signup_fields_frame, text="Full Name", 
                font=("Arial", 10, "bold"), bg=COLORS['white'], 
                fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
        
        self.fullname_entry = tk.Entry(self.signup_fields_frame, 
                                       font=("Arial", 12), relief=tk.FLAT, 
                                       bg=COLORS['light'])
        self.fullname_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
        
        # Email
        tk.Label(self.signup_fields_frame, text="Email", 
                font=("Arial", 10, "bold"), bg=COLORS['white'], 
                fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
        
        self.email_entry = tk.Entry(self.signup_fields_frame, 
                                    font=("Arial", 12), relief=tk.FLAT, 
                                    bg=COLORS['light'])
        self.email_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
        
        # User Type
        tk.Label(self.signup_fields_frame, text="I am a", 
                font=("Arial", 10, "bold"), bg=COLORS['white'], 
                fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
        
        self.user_type_var = tk.StringVar(value="student")
        type_frame = tk.Frame(self.signup_fields_frame, bg=COLORS['white'])
        type_frame.pack(fill=tk.X, padx=40, pady=(5, 15))
        
        tk.Radiobutton(type_frame, text="Student", variable=self.user_type_var, 
                      value="student", font=("Arial", 11), bg=COLORS['white'], 
                      command=self.toggle_type_fields).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(type_frame, text="Teacher", variable=self.user_type_var, 
                      value="teacher", font=("Arial", 11), bg=COLORS['white'],
                      command=self.toggle_type_fields).pack(side=tk.LEFT)
        
        # Type specific fields
        self.type_specific_frame = tk.Frame(self.signup_fields_frame, 
                                           bg=COLORS['white'])
        self.type_specific_frame.pack(fill=tk.X)
        
        self.toggle_type_fields()
        
        self.signup_fields_frame.pack(after=self.password_entry, 
                                      fill=tk.X, pady=(10, 0))
    
    def toggle_type_fields(self):
        for widget in self.type_specific_frame.winfo_children():
            widget.destroy()
        
        if self.user_type_var.get() == "student":
            tk.Label(self.type_specific_frame, text="Roll Number", 
                    font=("Arial", 10, "bold"), bg=COLORS['white'], 
                    fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
            
            self.roll_entry = tk.Entry(self.type_specific_frame, 
                                      font=("Arial", 12), relief=tk.FLAT, 
                                      bg=COLORS['light'])
            self.roll_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
            
            tk.Label(self.type_specific_frame, text="Class", 
                    font=("Arial", 10, "bold"), bg=COLORS['white'], 
                    fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
            
            self.class_entry = tk.Entry(self.type_specific_frame, 
                                       font=("Arial", 12), relief=tk.FLAT, 
                                       bg=COLORS['light'])
            self.class_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
        else:
            tk.Label(self.type_specific_frame, text="Employee ID", 
                    font=("Arial", 10, "bold"), bg=COLORS['white'], 
                    fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
            
            self.emp_id_entry = tk.Entry(self.type_specific_frame, 
                                        font=("Arial", 12), relief=tk.FLAT, 
                                        bg=COLORS['light'])
            self.emp_id_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
            
            tk.Label(self.type_specific_frame, text="Department", 
                    font=("Arial", 10, "bold"), bg=COLORS['white'], 
                    fg=COLORS['text_dark'], anchor='w').pack(fill=tk.X, padx=40)
            
            self.dept_entry = tk.Entry(self.type_specific_frame, 
                                      font=("Arial", 12), relief=tk.FLAT, 
                                      bg=COLORS['light'])
            self.dept_entry.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=8)
    
    def hide_signup_fields(self):
        self.signup_fields_frame.pack_forget()
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        conn = Database.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor(dictionary=True)
        hashed_password = Database.hash_password(password)
        
        cursor.execute("""
            SELECT user_id, username, full_name, user_type 
            FROM users 
            WHERE username = %s AND password = %s
        """, (username, hashed_password))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            messagebox.showinfo("Success", f"Welcome back, {user['full_name']}!")
            self.root.destroy()
            self.open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        fullname = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        user_type = self.user_type_var.get()
        
        if not all([username, password, fullname, email]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        conn = Database.get_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        hashed_password = Database.hash_password(password)
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, hashed_password, fullname, email, user_type))
            
            user_id = cursor.lastrowid
            
            if user_type == "student":
                roll = self.roll_entry.get().strip()
                class_name = self.class_entry.get().strip()
                cursor.execute("""
                    INSERT INTO students (user_id, roll_number, class)
                    VALUES (%s, %s, %s)
                """, (user_id, roll, class_name))
            else:
                emp_id = self.emp_id_entry.get().strip()
                dept = self.dept_entry.get().strip()
                cursor.execute("""
                    INSERT INTO teachers (user_id, employee_id, department)
                    VALUES (%s, %s, %s)
                """, (user_id, emp_id, dept))
            
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.toggle_mode()
            
        except Error as e:
            messagebox.showerror("Error", f"Signup failed: {e}")
        
        cursor.close()
        conn.close()
    
    def open_dashboard(self, user):
        root = tk.Tk()
        if user['user_type'] == 'student':
            # Import and run student dashboard
            from student_dashboard import StudentDashboard
            StudentDashboard(root, user)
        else:
            # Import and run teacher dashboard
            from teacher_dashboard import TeacherDashboard
            TeacherDashboard(root, user)
        root.mainloop()

# ==================== MAIN ENTRY POINT ====================
def main():
    # Check database connection
    conn = Database.get_connection()
    if not conn:
        messagebox.showerror("Error", 
                           "Cannot connect to database!\n\n"
                           "Please ensure:\n"
                           "1. MySQL is running\n"
                           "2. Database 'attendance_system' exists\n"
                           "3. Run database_setup.py first")
        sys.exit(1)
    conn.close()
    
    # Start the application
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
