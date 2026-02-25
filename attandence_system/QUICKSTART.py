"""
QUICK START GUIDE
=================

Follow these steps to get your Attendance Management System running:

STEP 1: Install Dependencies
-----------------------------
Run this command in your terminal:
    pip install -r requirements.txt

Or manually install:
    pip install mysql-connector-python


STEP 2: Configure Database
---------------------------
1. Make sure MySQL is installed and running
2. Open 'database_setup.py' and update line 13 with your MySQL password:
   self.password = "your_password_here"

3. Also update the password in:
   - main.py (line 16)
   - student_dashboard.py (line 61)
   - teacher_dashboard.py (line 63)


STEP 3: Setup Database
----------------------
Run the setup script:
    python database_setup.py

This will create:
- Database 'attendance_system'
- All required tables
- Demo accounts for testing


STEP 4: Run the Application
----------------------------
Start the application:
    python main.py


DEMO CREDENTIALS
================

Teacher Account:
- Username: teacher_demo
- Password: teacher123

Student Account:
- Username: student_demo
- Password: student123


FEATURES TO TRY
===============

As a Teacher:
1. Mark attendance for students
2. Add new students
3. Remove students
4. Add remarks to attendance

As a Student:
1. View attendance statistics
2. Check attendance records
3. Read notifications


COMMON ISSUES
=============

Issue: "Cannot connect to database"
Solution: 
- Start MySQL service
- Check password in configuration files
- Verify database exists

Issue: "No module named 'mysql.connector'"
Solution: 
- Run: pip install mysql-connector-python

Issue: Table doesn't exist
Solution: 
- Run: python database_setup.py


CUSTOMIZATION
=============

To change colors:
- Edit COLORS dictionary in main.py (lines 21-30)

To change database name:
- Update 'database' in DB_CONFIG in main.py


SUPPORT
=======

For help:
1. Read README.md for detailed documentation
2. Check troubleshooting section
3. Verify all configuration files


Enjoy your Attendance Management System! 🎓
"""

if __name__ == "__main__":
    print(__doc__)
