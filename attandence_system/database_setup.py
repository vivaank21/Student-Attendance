"""
Database Setup for Attendance Management System
Creates all necessary tables and initial configuration
"""

import mysql.connector
from mysql.connector import Error
import hashlib

class DatabaseSetup:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # Change this to your MySQL password
        self.database = "attendance_system"
    
    def create_database(self):
        """Create the main database"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print("✓ Database created successfully")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error creating database: {e}")
    
    def get_connection(self):
        """Get database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def create_tables(self):
        """Create all necessary tables"""
        connection = self.get_connection()
        if not connection:
            return
        
        cursor = connection.cursor()
        
        # Users table (for authentication)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                user_type ENUM('student', 'teacher') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Students table (additional student info)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE,
                roll_number VARCHAR(20) UNIQUE NOT NULL,
                class VARCHAR(50) NOT NULL,
                phone VARCHAR(15),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Teachers table (additional teacher info)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE,
                employee_id VARCHAR(20) UNIQUE NOT NULL,
                department VARCHAR(50),
                phone VARCHAR(15),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                date DATE NOT NULL,
                status ENUM('Present', 'Absent', 'Late') NOT NULL,
                marked_by INT NOT NULL,
                marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                remarks TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (marked_by) REFERENCES teachers(teacher_id),
                UNIQUE KEY unique_attendance (student_id, date)
            )
        """)
        
        # Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("✓ All tables created successfully")
        cursor.close()
        connection.close()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_demo_accounts(self):
        """Create demo teacher and student accounts"""
        connection = self.get_connection()
        if not connection:
            return
        
        cursor = connection.cursor()
        
        try:
            # Create demo teacher
            teacher_pass = self.hash_password("teacher123")
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """, ("teacher_demo", teacher_pass, "Demo Teacher", "teacher@demo.com", "teacher"))
            
            teacher_user_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO teachers (user_id, employee_id, department, phone)
                VALUES (%s, %s, %s, %s)
            """, (teacher_user_id, "T001", "Computer Science", "1234567890"))
            
            # Create demo student
            student_pass = self.hash_password("student123")
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """, ("student_demo", student_pass, "Demo Student", "student@demo.com", "student"))
            
            student_user_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO students (user_id, roll_number, class, phone)
                VALUES (%s, %s, %s, %s)
            """, (student_user_id, "S001", "Class 10A", "9876543210"))
            
            connection.commit()
            print("✓ Demo accounts created successfully")
            print("\nDemo Credentials:")
            print("Teacher - Username: teacher_demo, Password: teacher123")
            print("Student - Username: student_demo, Password: student123")
            
        except Error as e:
            print(f"Note: Demo accounts may already exist - {e}")
        
        cursor.close()
        connection.close()
    
    def setup_all(self):
        """Run complete setup"""
        print("Starting database setup...")
        self.create_database()
        self.create_tables()
        self.create_demo_accounts()
        print("\n✓ Setup completed successfully!")

if __name__ == "__main__":
    setup = DatabaseSetup()
    setup.setup_all()
