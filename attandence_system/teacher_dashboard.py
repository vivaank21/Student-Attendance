"""
Teacher Dashboard - Mark attendance, manage students
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, date
import hashlib

COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#27AE60',
    'danger': '#E74C3C',
    'warning': '#F39C12',
    'light': '#ECF0F1',
    'dark': '#34495E',
    'white': '#FFFFFF',
    'text_dark': '#2C3E50',
    'hover': '#5DADE2'
}

class TeacherDashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.root.title("Teacher Dashboard - Attendance Management")
        self.root.geometry("1400x800")
        self.root.configure(bg=COLORS['light'])
        
        # Database connection
        self.db = self.get_db_connection()
        
        # Get teacher details
        self.get_teacher_info()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_dashboard_ui()
        
        # Load initial data
        self.load_students()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_db_connection(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="attendance_system"
            )
        except:
            return None
    
    def get_teacher_info(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.teacher_id, t.employee_id, t.department
            FROM teachers t
            WHERE t.user_id = %s
        """, (self.user_data['user_id'],))
        self.teacher_info = cursor.fetchone()
        cursor.close()
    
    def create_dashboard_ui(self):
        # Top Bar
        top_bar = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo and title
        tk.Label(top_bar, text="👨‍🏫 Teacher Dashboard", 
                font=("Arial", 20, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white']).pack(side=tk.LEFT, padx=30, pady=20)
        
        # User info
        user_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        user_frame.pack(side=tk.RIGHT, padx=30)
        
        tk.Label(user_frame, text=self.user_data['full_name'], 
                font=("Arial", 12, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white']).pack(anchor='e')
        
        tk.Label(user_frame, 
                text=f"{self.teacher_info['department']} | ID: {self.teacher_info['employee_id']}", 
                font=("Arial", 10), bg=COLORS['primary'], 
                fg=COLORS['light']).pack(anchor='e')
        
        # Navigation Tabs
        tab_frame = tk.Frame(self.root, bg=COLORS['white'])
        tab_frame.pack(fill=tk.X)
        
        self.current_tab = tk.StringVar(value="attendance")
        
        tabs = [
            ("Mark Attendance", "attendance"),
            ("Student Management", "students"),
            ("Reports", "reports")
        ]
        
        for text, value in tabs:
            btn = tk.Button(tab_frame, text=text, font=("Arial", 11, "bold"),
                          bg=COLORS['secondary'] if value == "attendance" 
                          else COLORS['white'],
                          fg=COLORS['white'] if value == "attendance" 
                          else COLORS['text_dark'],
                          relief=tk.FLAT, cursor='hand2',
                          command=lambda v=value: self.switch_tab(v))
            btn.pack(side=tk.LEFT, padx=2, pady=10, ipadx=20, ipady=10)
            
            if value == "attendance":
                self.attendance_tab_btn = btn
            elif value == "students":
                self.students_tab_btn = btn
            else:
                self.reports_tab_btn = btn
        
        # Content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['light'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show default tab
        self.show_attendance_tab()
    
    def switch_tab(self, tab_name):
        # Update button colors
        for btn in [self.attendance_tab_btn, self.students_tab_btn, 
                    self.reports_tab_btn]:
            btn.config(bg=COLORS['white'], fg=COLORS['text_dark'])
        
        if tab_name == "attendance":
            self.attendance_tab_btn.config(bg=COLORS['secondary'], 
                                          fg=COLORS['white'])
            self.show_attendance_tab()
        elif tab_name == "students":
            self.students_tab_btn.config(bg=COLORS['secondary'], 
                                        fg=COLORS['white'])
            self.show_students_tab()
        else:
            self.reports_tab_btn.config(bg=COLORS['secondary'], 
                                       fg=COLORS['white'])
            self.show_reports_tab()
        
        self.current_tab.set(tab_name)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_attendance_tab(self):
        self.clear_content()
        
        # Main container
        main = tk.Frame(self.content_frame, bg=COLORS['light'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main, bg=COLORS['white'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="📝 Mark Attendance", 
                font=("Arial", 16, "bold"), bg=COLORS['white'], 
                fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Date selector
        date_frame = tk.Frame(header, bg=COLORS['white'])
        date_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(date_frame, text="Date:", font=("Arial", 11), 
                bg=COLORS['white']).pack(side=tk.LEFT, padx=5)
        
        self.attendance_date = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        
        tk.Entry(date_frame, textvariable=self.attendance_date, 
                font=("Arial", 11), width=12, justify='center').pack(
                    side=tk.LEFT, padx=5)
        
        # Student list with checkboxes
        list_frame = tk.Frame(main, bg=COLORS['white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table
        columns = ('Roll No', 'Name', 'Class', 'Status', 'Remarks')
        
        self.attendance_tree = ttk.Treeview(list_frame, columns=columns, 
                                           show='headings', height=20)
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
        
        self.attendance_tree.column('Roll No', width=100, anchor='center')
        self.attendance_tree.column('Name', width=200, anchor='w')
        self.attendance_tree.column('Class', width=150, anchor='center')
        self.attendance_tree.column('Status', width=150, anchor='center')
        self.attendance_tree.column('Remarks', width=300, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscroll=scrollbar.set)
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, 
                                 expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))
        
        # Double click to edit
        self.attendance_tree.bind('<Double-1>', self.edit_attendance_status)
        
        # Action buttons
        btn_frame = tk.Frame(main, bg=COLORS['light'])
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(btn_frame, text="✓ Mark All Present", 
                 font=("Arial", 11, "bold"), bg=COLORS['success'], 
                 fg=COLORS['white'], relief=tk.FLAT, cursor='hand2',
                 command=lambda: self.mark_all_students('Present')).pack(
                     side=tk.LEFT, padx=5, ipadx=15, ipady=10)
        
        tk.Button(btn_frame, text="✗ Mark All Absent", 
                 font=("Arial", 11, "bold"), bg=COLORS['danger'], 
                 fg=COLORS['white'], relief=tk.FLAT, cursor='hand2',
                 command=lambda: self.mark_all_students('Absent')).pack(
                     side=tk.LEFT, padx=5, ipadx=15, ipady=10)
        
        tk.Button(btn_frame, text="💾 Save Attendance", 
                 font=("Arial", 11, "bold"), bg=COLORS['secondary'], 
                 fg=COLORS['white'], relief=tk.FLAT, cursor='hand2',
                 command=self.save_attendance).pack(
                     side=tk.RIGHT, padx=5, ipadx=20, ipady=10)
        
        # Load students for attendance
        self.load_students_for_attendance()
    
    def load_students_for_attendance(self):
        # Clear existing
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.student_id, s.roll_number, s.class, u.full_name
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            ORDER BY s.roll_number
        """)
        
        students = cursor.fetchall()
        
        # Check if attendance already marked for today
        selected_date = self.attendance_date.get()
        
        for student in students:
            cursor.execute("""
                SELECT status, remarks FROM attendance
                WHERE student_id = %s AND date = %s
            """, (student['student_id'], selected_date))
            
            existing = cursor.fetchone()
            status = existing['status'] if existing else 'Not Marked'
            remarks = existing['remarks'] if existing and existing['remarks'] else ''
            
            self.attendance_tree.insert('', tk.END,
                                       values=(student['roll_number'],
                                              student['full_name'],
                                              student['class'],
                                              status,
                                              remarks),
                                       tags=(student['student_id'],))
        
        cursor.close()
    
    def edit_attendance_status(self, event):
        selected = self.attendance_tree.selection()
        if not selected:
            return
        
        item = selected[0]
        values = list(self.attendance_tree.item(item, 'values'))
        
        # Create popup to edit
        popup = tk.Toplevel(self.root)
        popup.title("Edit Attendance")
        popup.geometry("400x300")
        popup.configure(bg=COLORS['white'])
        popup.transient(self.root)
        popup.grab_set()
        
        # Center popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        tk.Label(popup, text=f"Student: {values[1]}", 
                font=("Arial", 12, "bold"), bg=COLORS['white']).pack(pady=20)
        
        tk.Label(popup, text="Status:", font=("Arial", 11), 
                bg=COLORS['white']).pack()
        
        status_var = tk.StringVar(value=values[3])
        
        for status in ['Present', 'Absent', 'Late']:
            tk.Radiobutton(popup, text=status, variable=status_var, 
                          value=status, font=("Arial", 11), 
                          bg=COLORS['white']).pack()
        
        tk.Label(popup, text="Remarks:", font=("Arial", 11), 
                bg=COLORS['white']).pack(pady=(10, 5))
        
        remarks_entry = tk.Text(popup, height=4, width=40, 
                               font=("Arial", 10))
        remarks_entry.pack(padx=20)
        remarks_entry.insert('1.0', values[4])
        
        def save_changes():
            new_status = status_var.get()
            new_remarks = remarks_entry.get('1.0', 'end-1c')
            
            values[3] = new_status
            values[4] = new_remarks
            
            self.attendance_tree.item(item, values=values)
            popup.destroy()
        
        tk.Button(popup, text="Save", font=("Arial", 11, "bold"), 
                 bg=COLORS['secondary'], fg=COLORS['white'], 
                 relief=tk.FLAT, cursor='hand2',
                 command=save_changes).pack(pady=20, ipadx=30, ipady=8)
    
    def mark_all_students(self, status):
        for item in self.attendance_tree.get_children():
            values = list(self.attendance_tree.item(item, 'values'))
            values[3] = status
            self.attendance_tree.item(item, values=values)
    
    def save_attendance(self):
        selected_date = self.attendance_date.get()
        
        try:
            # Validate date format
            datetime.strptime(selected_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        cursor = self.db.cursor()
        saved_count = 0
        
        for item in self.attendance_tree.get_children():
            values = self.attendance_tree.item(item, 'values')
            tags = self.attendance_tree.item(item, 'tags')
            
            student_id = tags[0]
            status = values[3]
            remarks = values[4]
            
            if status == 'Not Marked':
                continue
            
            try:
                # Check if attendance exists
                cursor.execute("""
                    SELECT attendance_id FROM attendance
                    WHERE student_id = %s AND date = %s
                """, (student_id, selected_date))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update
                    cursor.execute("""
                        UPDATE attendance
                        SET status = %s, remarks = %s, marked_by = %s, 
                            marked_at = NOW()
                        WHERE attendance_id = %s
                    """, (status, remarks, self.teacher_info['teacher_id'], 
                         existing[0]))
                else:
                    # Insert
                    cursor.execute("""
                        INSERT INTO attendance 
                        (student_id, date, status, marked_by, remarks)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (student_id, selected_date, status, 
                         self.teacher_info['teacher_id'], remarks))
                
                # Create notification for student
                cursor.execute("""
                    SELECT user_id FROM students WHERE student_id = %s
                """, (student_id,))
                user_id = cursor.fetchone()[0]
                
                message = f"Attendance marked as {status} for {selected_date}"
                if remarks:
                    message += f" - {remarks}"
                
                cursor.execute("""
                    INSERT INTO notifications (user_id, message)
                    VALUES (%s, %s)
                """, (user_id, message))
                
                saved_count += 1
                
            except Exception as e:
                print(f"Error saving attendance: {e}")
        
        self.db.commit()
        cursor.close()
        
        messagebox.showinfo("Success", 
                          f"Attendance saved for {saved_count} students!")
        self.load_students_for_attendance()
    
    def show_students_tab(self):
        self.clear_content()
        
        # Main container
        main = tk.Frame(self.content_frame, bg=COLORS['light'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with action buttons
        header = tk.Frame(main, bg=COLORS['white'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="👥 Student Management", 
                font=("Arial", 16, "bold"), bg=COLORS['white'], 
                fg=COLORS['text_dark']).pack(side=tk.LEFT, padx=20, pady=15)
        
        btn_frame = tk.Frame(header, bg=COLORS['white'])
        btn_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(btn_frame, text="➕ Add Student", 
                 font=("Arial", 11, "bold"), bg=COLORS['success'], 
                 fg=COLORS['white'], relief=tk.FLAT, cursor='hand2',
                 command=self.add_student_dialog).pack(
                     side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        
        tk.Button(btn_frame, text="🗑️ Remove Student", 
                 font=("Arial", 11, "bold"), bg=COLORS['danger'], 
                 fg=COLORS['white'], relief=tk.FLAT, cursor='hand2',
                 command=self.remove_student).pack(
                     side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        
        # Student list
        list_frame = tk.Frame(main, bg=COLORS['white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Roll No', 'Name', 'Class', 'Email', 'Phone')
        
        self.students_tree = ttk.Treeview(list_frame, columns=columns, 
                                         show='headings', height=20)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
        
        self.students_tree.column('Roll No', width=100, anchor='center')
        self.students_tree.column('Name', width=250, anchor='w')
        self.students_tree.column('Class', width=150, anchor='center')
        self.students_tree.column('Email', width=250, anchor='w')
        self.students_tree.column('Phone', width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                 command=self.students_tree.yview)
        self.students_tree.configure(yscroll=scrollbar.set)
        
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, 
                               expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20, padx=(0, 20))
        
        # Load students
        self.load_students()
    
    def load_students(self):
        if not hasattr(self, 'students_tree'):
            return
        
        # Clear existing
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.student_id, s.roll_number, s.class, s.phone,
                   u.full_name, u.email
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            ORDER BY s.roll_number
        """)
        
        students = cursor.fetchall()
        cursor.close()
        
        for student in students:
            phone = student['phone'] if student['phone'] else 'N/A'
            self.students_tree.insert('', tk.END,
                                     values=(student['roll_number'],
                                            student['full_name'],
                                            student['class'],
                                            student['email'],
                                            phone),
                                     tags=(student['student_id'],))
    
    def add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("500x650")
        dialog.configure(bg=COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Title
        tk.Label(dialog, text="Add New Student", font=("Arial", 16, "bold"), 
                bg=COLORS['white'], fg=COLORS['text_dark']).pack(pady=20)
        
        # Form fields
        fields_frame = tk.Frame(dialog, bg=COLORS['white'])
        fields_frame.pack(padx=40, fill=tk.BOTH, expand=True)
        
        fields = {
            'Username': tk.StringVar(),
            'Password': tk.StringVar(),
            'Full Name': tk.StringVar(),
            'Email': tk.StringVar(),
            'Roll Number': tk.StringVar(),
            'Class': tk.StringVar(),
            'Phone': tk.StringVar()
        }
        
        for label, var in fields.items():
            tk.Label(fields_frame, text=label, font=("Arial", 10, "bold"), 
                    bg=COLORS['white'], fg=COLORS['text_dark'], 
                    anchor='w').pack(fill=tk.X, pady=(10, 5))
            
            entry = tk.Entry(fields_frame, textvariable=var, 
                           font=("Arial", 11), relief=tk.FLAT, 
                           bg=COLORS['light'])
            
            if label == 'Password':
                entry.config(show='●')
            
            entry.pack(fill=tk.X, ipady=8)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=COLORS['white'])
        btn_frame.pack(pady=20)
        
        def save_student():
            # Validate
            for label, var in fields.items():
                if not var.get().strip():
                    messagebox.showerror("Error", f"{label} is required!")
                    return
            
            cursor = self.db.cursor()
            
            try:
                # Hash password
                hashed_password = hashlib.sha256(
                    fields['Password'].get().encode()).hexdigest()
                
                # Insert user
                cursor.execute("""
                    INSERT INTO users 
                    (username, password, full_name, email, user_type)
                    VALUES (%s, %s, %s, %s, 'student')
                """, (fields['Username'].get(), hashed_password,
                     fields['Full Name'].get(), fields['Email'].get()))
                
                user_id = cursor.lastrowid
                
                # Insert student
                cursor.execute("""
                    INSERT INTO students 
                    (user_id, roll_number, class, phone)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, fields['Roll Number'].get(),
                     fields['Class'].get(), fields['Phone'].get()))
                
                self.db.commit()
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                self.load_students()
                
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to add student: {e}")
            
            cursor.close()
        
        tk.Button(btn_frame, text="Save", font=("Arial", 11, "bold"), 
                 bg=COLORS['success'], fg=COLORS['white'], 
                 relief=tk.FLAT, cursor='hand2',
                 command=save_student).pack(side=tk.LEFT, padx=10, 
                                          ipadx=30, ipady=10)
        
        tk.Button(btn_frame, text="Cancel", font=("Arial", 11, "bold"), 
                 bg=COLORS['dark'], fg=COLORS['white'], 
                 relief=tk.FLAT, cursor='hand2',
                 command=dialog.destroy).pack(side=tk.LEFT, padx=10, 
                                            ipadx=30, ipady=10)
    
    def remove_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to remove")
            return
        
        item = selected[0]
        values = self.students_tree.item(item, 'values')
        tags = self.students_tree.item(item, 'tags')
        student_id = tags[0]
        
        confirm = messagebox.askyesno("Confirm", 
                                     f"Remove student {values[1]}?\n"
                                     "This will also delete all attendance records.")
        
        if not confirm:
            return
        
        cursor = self.db.cursor()
        
        try:
            # Get user_id
            cursor.execute("""
                SELECT user_id FROM students WHERE student_id = %s
            """, (student_id,))
            user_id = cursor.fetchone()[0]
            
            # Delete user (cascade will delete student and attendance)
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            
            self.db.commit()
            messagebox.showinfo("Success", "Student removed successfully!")
            self.load_students()
            
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to remove student: {e}")
        
        cursor.close()
    
    def show_reports_tab(self):
        self.clear_content()
        
        tk.Label(self.content_frame, 
                text="📊 Reports Feature\n\nComing Soon!", 
                font=("Arial", 18, "bold"), bg=COLORS['light'], 
                fg=COLORS['text_dark']).pack(expand=True)
