"""
Student Dashboard - View attendance and notifications
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
import calendar

# Import colors from main file
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

class StudentDashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.root.title("Student Dashboard - Attendance Management")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['light'])
        
        # Database connection
        self.db = self.get_db_connection()
        
        # Get student details
        self.get_student_info()
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_dashboard_ui()
        
        # Load initial data
        self.load_attendance_data()
        self.load_notifications()
    
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
    
    def get_student_info(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.student_id, s.roll_number, s.class
            FROM students s
            WHERE s.user_id = %s
        """, (self.user_data['user_id'],))
        self.student_info = cursor.fetchone()
        cursor.close()
    
    def create_dashboard_ui(self):
        # Top Bar
        top_bar = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo and title
        tk.Label(top_bar, text="🎓 Student Dashboard", 
                font=("Arial", 20, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white']).pack(side=tk.LEFT, padx=30, pady=20)
        
        # User info
        user_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        user_frame.pack(side=tk.RIGHT, padx=30)
        
        tk.Label(user_frame, text=self.user_data['full_name'], 
                font=("Arial", 12, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white']).pack(anchor='e')
        
        tk.Label(user_frame, text=f"Roll No: {self.student_info['roll_number']}", 
                font=("Arial", 10), bg=COLORS['primary'], 
                fg=COLORS['light']).pack(anchor='e')
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=COLORS['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Statistics
        left_panel = tk.Frame(content_frame, bg=COLORS['light'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_stats_cards(left_panel)
        self.create_notifications_panel(left_panel)
        
        # Right panel - Attendance details
        right_panel = tk.Frame(content_frame, bg=COLORS['white'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_attendance_panel(right_panel)
    
    def create_stats_cards(self, parent):
        # Stats container
        stats_frame = tk.Frame(parent, bg=COLORS['light'])
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(stats_frame, text="Attendance Summary", 
                font=("Arial", 14, "bold"), bg=COLORS['light'], 
                fg=COLORS['text_dark']).pack(anchor='w', pady=(0, 10))
        
        # Get statistics
        cursor = self.db.cursor(dictionary=True)
        
        # Total days
        cursor.execute("""
            SELECT COUNT(*) as total FROM attendance 
            WHERE student_id = %s
        """, (self.student_info['student_id'],))
        total_days = cursor.fetchone()['total']
        
        # Present days
        cursor.execute("""
            SELECT COUNT(*) as present FROM attendance 
            WHERE student_id = %s AND status = 'Present'
        """, (self.student_info['student_id'],))
        present_days = cursor.fetchone()['present']
        
        # Absent days
        cursor.execute("""
            SELECT COUNT(*) as absent FROM attendance 
            WHERE student_id = %s AND status = 'Absent'
        """, (self.student_info['student_id'],))
        absent_days = cursor.fetchone()['absent']
        
        cursor.close()
        
        # Calculate percentage
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Cards
        self.create_stat_card(stats_frame, "Total Days", str(total_days), 
                             COLORS['secondary'], "📅")
        self.create_stat_card(stats_frame, "Present", str(present_days), 
                             COLORS['success'], "✓")
        self.create_stat_card(stats_frame, "Absent", str(absent_days), 
                             COLORS['danger'], "✗")
        self.create_stat_card(stats_frame, "Percentage", 
                             f"{attendance_percentage:.1f}%", 
                             COLORS['warning'], "📊")
    
    def create_stat_card(self, parent, title, value, color, icon):
        card = tk.Frame(parent, bg=color, relief=tk.FLAT, bd=0)
        card.pack(fill=tk.X, pady=5)
        
        inner = tk.Frame(card, bg=color)
        inner.pack(fill=tk.BOTH, padx=15, pady=15)
        
        tk.Label(inner, text=icon, font=("Arial", 24), 
                bg=color, fg=COLORS['white']).pack(side=tk.LEFT, padx=(0, 15))
        
        text_frame = tk.Frame(inner, bg=color)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(text_frame, text=title, font=("Arial", 10), 
                bg=color, fg=COLORS['white'], anchor='w').pack(fill=tk.X)
        tk.Label(text_frame, text=value, font=("Arial", 20, "bold"), 
                bg=color, fg=COLORS['white'], anchor='w').pack(fill=tk.X)
    
    def create_notifications_panel(self, parent):
        notif_frame = tk.Frame(parent, bg=COLORS['white'], relief=tk.FLAT)
        notif_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(notif_frame, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📬 Notifications", font=("Arial", 12, "bold"), 
                bg=COLORS['primary'], fg=COLORS['white']).pack(
                    side=tk.LEFT, padx=15, pady=10)
        
        # Notifications list
        notif_canvas = tk.Canvas(notif_frame, bg=COLORS['white'], 
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(notif_frame, orient="vertical", 
                                 command=notif_canvas.yview)
        
        self.notif_list_frame = tk.Frame(notif_canvas, bg=COLORS['white'])
        
        self.notif_list_frame.bind(
            "<Configure>",
            lambda e: notif_canvas.configure(scrollregion=notif_canvas.bbox("all"))
        )
        
        notif_canvas.create_window((0, 0), window=self.notif_list_frame, 
                                   anchor="nw")
        notif_canvas.configure(yscrollcommand=scrollbar.set)
        
        notif_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                         padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_notifications(self):
        # Clear existing
        for widget in self.notif_list_frame.winfo_children():
            widget.destroy()
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM notifications 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 10
        """, (self.user_data['user_id'],))
        
        notifications = cursor.fetchall()
        cursor.close()
        
        if not notifications:
            tk.Label(self.notif_list_frame, text="No notifications yet", 
                    font=("Arial", 10), bg=COLORS['white'], 
                    fg=COLORS['dark']).pack(pady=20)
            return
        
        for notif in notifications:
            self.create_notification_item(notif)
    
    def create_notification_item(self, notif):
        item_frame = tk.Frame(self.notif_list_frame, 
                             bg=COLORS['light'] if not notif['is_read'] 
                             else COLORS['white'],
                             relief=tk.SOLID, bd=1)
        item_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Determine icon based on message
        icon = "🔔"
        if "Present" in notif['message']:
            icon = "✓"
            color = COLORS['success']
        elif "Absent" in notif['message']:
            icon = "✗"
            color = COLORS['danger']
        else:
            color = COLORS['secondary']
        
        # Icon
        tk.Label(item_frame, text=icon, font=("Arial", 16), 
                bg=item_frame['bg'], fg=color).pack(
                    side=tk.LEFT, padx=10, pady=10)
        
        # Message
        text_frame = tk.Frame(item_frame, bg=item_frame['bg'])
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(text_frame, text=notif['message'], font=("Arial", 10), 
                bg=item_frame['bg'], fg=COLORS['text_dark'], 
                wraplength=250, justify='left').pack(anchor='w')
        
        time_str = notif['created_at'].strftime("%d %b, %I:%M %p")
        tk.Label(text_frame, text=time_str, font=("Arial", 8), 
                bg=item_frame['bg'], fg=COLORS['dark']).pack(anchor='w')
    
    def create_attendance_panel(self, parent):
        # Header
        header = tk.Frame(parent, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📋 Attendance Records", 
                font=("Arial", 14, "bold"), bg=COLORS['primary'], 
                fg=COLORS['white']).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Refresh button
        refresh_btn = tk.Button(header, text="🔄 Refresh", 
                               font=("Arial", 10), bg=COLORS['secondary'], 
                               fg=COLORS['white'], relief=tk.FLAT, 
                               cursor='hand2', command=self.refresh_data)
        refresh_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Table frame
        table_frame = tk.Frame(parent, bg=COLORS['white'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create Treeview
        columns = ('Date', 'Status', 'Marked By', 'Time', 'Remarks')
        
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, 
                                           show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.attendance_tree.heading(col, text=col)
        
        # Define column widths
        self.attendance_tree.column('Date', width=120, anchor='center')
        self.attendance_tree.column('Status', width=100, anchor='center')
        self.attendance_tree.column('Marked By', width=150, anchor='w')
        self.attendance_tree.column('Time', width=150, anchor='center')
        self.attendance_tree.column('Remarks', width=200, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscroll=scrollbar.set)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=COLORS['white'], 
                       foreground=COLORS['text_dark'], 
                       fieldbackground=COLORS['white'], 
                       font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), 
                       background=COLORS['light'], 
                       foreground=COLORS['text_dark'])
        
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags for colors
        self.attendance_tree.tag_configure('Present', 
                                          background='#D4EDDA', 
                                          foreground=COLORS['success'])
        self.attendance_tree.tag_configure('Absent', 
                                          background='#F8D7DA', 
                                          foreground=COLORS['danger'])
        self.attendance_tree.tag_configure('Late', 
                                          background='#FFF3CD', 
                                          foreground=COLORS['warning'])
    
    def load_attendance_data(self):
        # Clear existing data
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.date, a.status, a.marked_at, a.remarks,
                   u.full_name as teacher_name
            FROM attendance a
            JOIN teachers t ON a.marked_by = t.teacher_id
            JOIN users u ON t.user_id = u.user_id
            WHERE a.student_id = %s
            ORDER BY a.date DESC
        """, (self.student_info['student_id'],))
        
        records = cursor.fetchall()
        cursor.close()
        
        for record in records:
            date_str = record['date'].strftime("%d %b %Y")
            time_str = record['marked_at'].strftime("%I:%M %p")
            remarks = record['remarks'] if record['remarks'] else '-'
            
            self.attendance_tree.insert('', tk.END, 
                                       values=(date_str, 
                                              record['status'],
                                              record['teacher_name'],
                                              time_str,
                                              remarks),
                                       tags=(record['status'],))
    
    def refresh_data(self):
        self.load_attendance_data()
        self.load_notifications()
        # Recreate stats cards
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for subchild in child.winfo_children():
                            if isinstance(subchild, tk.Frame):
                                # Find stats frame and recreate
                                pass
        messagebox.showinfo("Success", "Data refreshed!")
