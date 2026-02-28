# 🎓 Attendance Management System

A professional, feature-rich attendance management system built with Python Tkinter and MySQL. Designed for educational institutions to efficiently track and manage student attendance.

## ✨ Features

### For Students:
- 📊 **View Attendance Records**: See complete attendance history with date, status, and remarks
- 📈 **Attendance Statistics**: Track total days, present days, absent days, and attendance percentage
- 🔔 **Real-time Notifications**: Get instant notifications when attendance is marked
- 📱 **Clean, Modern UI**: Professional and intuitive interface

### For Teachers:
- ✅ **Mark Attendance**: Easy-to-use interface for marking daily attendance
- 👥 **Student Management**: Add new students and remove existing ones
- 📝 **Batch Operations**: Mark all students present/absent with one click
- 📅 **Date Selection**: Mark attendance for any date
- 💬 **Add Remarks**: Add notes or comments for individual attendance entries
- 🔄 **Real-time Updates**: All changes reflected immediately

### General Features:
- 🔐 **Secure Authentication**: Login/Signup with password hashing
- 👤 **Role-based Access**: Separate interfaces for students and teachers
- 🎨 **Professional Design**: Modern color scheme and clean layout
- 📧 **Notification System**: Automated notifications for students

## 🎨 Color Scheme

- **Primary**: #2C3E50 (Dark Blue)
- **Secondary**: #3498DB (Bright Blue)
- **Success**: #27AE60 (Green)
- **Danger**: #E74C3C (Red)
- **Warning**: #F39C12 (Orange)
- **Light**: #ECF0F1 (Light Gray)

## 📸 Screen Shots

## Login screen
<img width="1250" height="776" alt="image" src="https://github.com/user-attachments/assets/97722cf1-903a-4ebf-8266-f062cfb9da8c" />

## Signup screen
<img width="1246" height="785" alt="image" src="https://github.com/user-attachments/assets/23a3a832-3343-4dc8-afe9-bc3bc8e8b8c3" />

## Student Dashboard screen
<img width="1499" height="909" alt="image" src="https://github.com/user-attachments/assets/81d96932-0040-42df-9e04-2b3103932fb0" />

## Teacher Dashboard screen
<img width="1747" height="1011" alt="image" src="https://github.com/user-attachments/assets/3f0cdc75-f3a2-4342-b2b2-1afbb1ba4571" />

## Student Management screen
<img width="1750" height="1004" alt="image" src="https://github.com/user-attachments/assets/f559864c-c63c-4225-9fc5-8435534096c8" />






## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** - GUI Framework
- **MySQL** - Database Management
- **mysql-connector-python** - Database Connectivity

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.7 or higher** installed
2. **MySQL Server** installed and running
3. Required Python packages (see Installation section)

## 📦 Installation

### Step 1: Install Python Packages

```bash
pip install mysql-connector-python
```

### Step 2: Configure MySQL

1. Start your MySQL server
2. Update the database credentials in the files if needed:
   - In `database_setup.py`: Update password on line 13
   - In `main.py`: Update DB_CONFIG on lines 14-18
   - In `student_dashboard.py` and `teacher_dashboard.py`: Update get_db_connection()

### Step 3: Setup Database

Run the database setup script to create the database and tables:

```bash
python database_setup.py
```

This will:
- Create the `attendance_system` database
- Create all necessary tables (users, students, teachers, attendance, notifications)
- Create demo accounts for testing

### Step 4: Run the Application

```bash
python main.py
```

## 👥 Demo Accounts

After running `database_setup.py`, you can use these demo accounts:

### Teacher Account
- **Username**: `teacher_demo`
- **Password**: `teacher123`

### Student Account
- **Username**: `student_demo`
- **Password**: `student123`

## 📊 Database Schema

### Users Table
- user_id (Primary Key)
- username
- password (hashed)
- full_name
- email
- user_type (student/teacher)
- created_at

### Students Table
- student_id (Primary Key)
- user_id (Foreign Key)
- roll_number
- class
- phone

### Teachers Table
- teacher_id (Primary Key)
- user_id (Foreign Key)
- employee_id
- department
- phone

### Attendance Table
- attendance_id (Primary Key)
- student_id (Foreign Key)
- date
- status (Present/Absent/Late)
- marked_by (Foreign Key to teacher)
- marked_at
- remarks

### Notifications Table
- notification_id (Primary Key)
- user_id (Foreign Key)
- message
- is_read
- created_at

## 🚀 Usage Guide

### For Students:

1. **Login**: Use your username and password
2. **View Dashboard**: See your attendance statistics on the left panel
3. **Check Notifications**: View attendance notifications in the notifications panel
4. **View Records**: See detailed attendance history in the main table
5. **Refresh**: Click the refresh button to update data

### For Teachers:

1. **Login**: Use your teacher credentials
2. **Mark Attendance**:
   - Select the date (default is today)
   - Double-click on any student to change their status
   - Use bulk actions to mark all present/absent
   - Add remarks for individual students
   - Click "Save Attendance" to submit
3. **Manage Students**:
   - Switch to "Student Management" tab
   - Add new students with "Add Student" button
   - Remove students with "Remove Student" button
4. **View Reports**: (Coming soon)

### Creating a New Account:

1. Click "Sign Up" on the login screen
2. Fill in your details:
   - Username (must be unique)
   - Password
   - Full Name
   - Email
   - Select role (Student/Teacher)
   - Fill role-specific fields
3. Click "SIGN UP"
4. Login with your new credentials

## 🔧 Configuration

### Changing MySQL Password

If your MySQL has a password, update it in three places:

1. **database_setup.py** (line 13):
```python
self.password = "your_mysql_password"
```

2. **main.py** (line 16):
```python
'password': 'your_mysql_password',
```

3. **student_dashboard.py** and **teacher_dashboard.py**:
```python
password="your_mysql_password"
```

### Changing Port or Host

Update the `host` and add `port` in DB_CONFIG:
```python
DB_CONFIG = {
    'host': 'your_host',
    'port': 3306,  # or your custom port
    'user': 'root',
    'password': '',
    'database': 'attendance_system'
}
```

## 🐛 Troubleshooting

### "Cannot connect to database" Error
- Ensure MySQL server is running
- Check credentials in the configuration
- Verify the database exists (run database_setup.py)

### "No module named 'mysql.connector'" Error
- Install the required package: `pip install mysql-connector-python`

### "Table doesn't exist" Error
- Run `database_setup.py` to create tables

### UI Elements Not Showing
- Ensure Tkinter is properly installed with Python
- On Linux: `sudo apt-get install python3-tk`

## 📝 File Structure

```
attendance-system/
│
├── database_setup.py       # Database initialization script
├── main.py                 # Main application entry point
├── student_dashboard.py    # Student interface module
├── teacher_dashboard.py    # Teacher interface module
└── README.md              # This file
```

## 🔐 Security Features

- Password hashing using SHA-256
- SQL injection prevention with parameterized queries
- Role-based access control
- Session management

## 🎯 Future Enhancements

- [ ] Reports and analytics dashboard
- [ ] Export attendance to Excel/PDF
- [ ] Email notifications
- [ ] Attendance trends and graphs
- [ ] Multi-class support for teachers
- [ ] Biometric integration
- [ ] Mobile app version
- [ ] Cloud database support

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Developer

Created as a professional attendance management solution for educational institutions.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all prerequisites are installed
3. Ensure database is properly configured


### Login Screen
Professional login interface with branding

### Student Dashboard
- Attendance statistics cards
- Notifications panel
- Detailed attendance records table

### Teacher Dashboard
- Mark attendance interface
- Student management
- Bulk operations

---

**Note**: Make sure to keep your database credentials secure and never share them publicly!
