-- ============================================
-- ATTENDANCE MANAGEMENT SYSTEM DATABASE
-- Complete SQL Database Setup
-- ============================================

-- Create Database
DROP DATABASE IF EXISTS attendance_system;
CREATE DATABASE attendance_system;
USE attendance_system;

-- ============================================
-- TABLE: users
-- Stores all user authentication data
-- ============================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_type ENUM('student', 'teacher') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE: students
-- Additional student-specific information
-- ============================================
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    class VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_roll_number (roll_number),
    INDEX idx_class (class)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE: teachers
-- Additional teacher-specific information
-- ============================================
CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50),
    phone VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_employee_id (employee_id),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE: attendance
-- Stores all attendance records
-- ============================================
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    marked_by INT NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES teachers(teacher_id),
    UNIQUE KEY unique_attendance (student_id, date),
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_student_date (student_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABLE: notifications
-- Stores user notifications
-- ============================================
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- INSERT SAMPLE DATA
-- Demo accounts and initial data
-- ============================================

-- Demo Teacher Account
-- Username: teacher_demo
-- Password: teacher123 (hashed with SHA-256)
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('teacher_demo', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Demo Teacher', 'teacher@demo.com', 'teacher');

SET @teacher_user_id = LAST_INSERT_ID();

INSERT INTO teachers (user_id, employee_id, department, phone) VALUES
(@teacher_user_id, 'T001', 'Computer Science', '1234567890');

SET @teacher_id = LAST_INSERT_ID();

-- Demo Student Account
-- Username: student_demo
-- Password: student123 (hashed with SHA-256)
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('student_demo', '6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918', 'Demo Student', 'student@demo.com', 'student');

SET @student_user_id = LAST_INSERT_ID();

INSERT INTO students (user_id, roll_number, class, phone) VALUES
(@student_user_id, 'S001', 'Class 10A', '9876543210');

-- ============================================
-- ADDITIONAL SAMPLE STUDENTS
-- More students for demonstration
-- ============================================

-- Student 2
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('john_smith', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'John Smith', 'john.smith@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S002', 'Class 10A', '9876543211');

-- Student 3
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('emma_johnson', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Emma Johnson', 'emma.johnson@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S003', 'Class 10A', '9876543212');

-- Student 4
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('michael_brown', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Michael Brown', 'michael.brown@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S004', 'Class 10A', '9876543213');

-- Student 5
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('sophia_davis', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Sophia Davis', 'sophia.davis@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S005', 'Class 10B', '9876543214');

-- Student 6
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('william_miller', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'William Miller', 'william.miller@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S006', 'Class 10B', '9876543215');

-- Student 7
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('olivia_wilson', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Olivia Wilson', 'olivia.wilson@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S007', 'Class 10B', '9876543216');

-- Student 8
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('james_moore', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'James Moore', 'james.moore@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S008', 'Class 10B', '9876543217');

-- Student 9
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('ava_taylor', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Ava Taylor', 'ava.taylor@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S009', 'Class 11A', '9876543218');

-- Student 10
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('alexander_anderson', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Alexander Anderson', 'alexander.anderson@school.com', 'student');
INSERT INTO students (user_id, roll_number, class, phone) VALUES
(LAST_INSERT_ID(), 'S010', 'Class 11A', '9876543219');

-- ============================================
-- ADDITIONAL TEACHERS
-- ============================================

-- Teacher 2
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('sarah_jones', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Sarah Jones', 'sarah.jones@school.com', 'teacher');
INSERT INTO teachers (user_id, employee_id, department, phone) VALUES
(LAST_INSERT_ID(), 'T002', 'Mathematics', '1234567891');

-- Teacher 3
INSERT INTO users (username, password, full_name, email, user_type) VALUES
('robert_garcia', '6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', 'Robert Garcia', 'robert.garcia@school.com', 'teacher');
INSERT INTO teachers (user_id, employee_id, department, phone) VALUES
(LAST_INSERT_ID(), 'T003', 'Physics', '1234567892');

-- ============================================
-- SAMPLE ATTENDANCE RECORDS
-- Last 30 days of attendance for demo
-- ============================================

-- Get student IDs for attendance records
SET @s1 = (SELECT student_id FROM students WHERE roll_number = 'S001');
SET @s2 = (SELECT student_id FROM students WHERE roll_number = 'S002');
SET @s3 = (SELECT student_id FROM students WHERE roll_number = 'S003');
SET @s4 = (SELECT student_id FROM students WHERE roll_number = 'S004');
SET @s5 = (SELECT student_id FROM students WHERE roll_number = 'S005');

-- Attendance for past 30 days (for S001 - Demo Student)
INSERT INTO attendance (student_id, date, status, marked_by, remarks) VALUES
-- Last week
(@s1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Present', @teacher_id, 'On time'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', @teacher_id, 'Active participation'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 'Absent', @teacher_id, 'Medical leave'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Present', @teacher_id, 'Excellent work'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Late', @teacher_id, 'Arrived 15 minutes late'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Present', @teacher_id, NULL),

-- Week 2
(@s1, DATE_SUB(CURDATE(), INTERVAL 8 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 9 DAY), 'Present', @teacher_id, 'Good participation'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 11 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 12 DAY), 'Absent', @teacher_id, 'Family emergency'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 13 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 14 DAY), 'Present', @teacher_id, NULL),

-- Week 3
(@s1, DATE_SUB(CURDATE(), INTERVAL 15 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 16 DAY), 'Present', @teacher_id, 'Submitted assignment'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 17 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 18 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 19 DAY), 'Present', @teacher_id, NULL),
(@s1, DATE_SUB(CURDATE(), INTERVAL 20 DAY), 'Late', @teacher_id, 'Traffic issue'),
(@s1, DATE_SUB(CURDATE(), INTERVAL 21 DAY), 'Present', @teacher_id, NULL);

-- Attendance for other students (last 7 days)
INSERT INTO attendance (student_id, date, status, marked_by, remarks) VALUES
-- S002
(@s2, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Present', @teacher_id, NULL),
(@s2, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', @teacher_id, NULL),
(@s2, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 'Present', @teacher_id, NULL),
(@s2, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Present', @teacher_id, NULL),
(@s2, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Absent', @teacher_id, 'Sick leave'),
(@s2, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Present', @teacher_id, NULL),
(@s2, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Present', @teacher_id, NULL),

-- S003
(@s3, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Present', @teacher_id, 'Excellent work'),
(@s3, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', @teacher_id, NULL),
(@s3, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 'Present', @teacher_id, NULL),
(@s3, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Late', @teacher_id, 'Bus was late'),
(@s3, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Present', @teacher_id, NULL),
(@s3, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Present', @teacher_id, NULL),
(@s3, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Present', @teacher_id, NULL),

-- S004
(@s4, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Absent', @teacher_id, 'Not well'),
(@s4, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', @teacher_id, NULL),
(@s4, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 'Present', @teacher_id, NULL),
(@s4, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Present', @teacher_id, NULL),
(@s4, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Present', @teacher_id, NULL),
(@s4, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Present', @teacher_id, NULL),
(@s4, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Present', @teacher_id, 'Good participation'),

-- S005
(@s5, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Present', @teacher_id, NULL),
(@s5, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Present', @teacher_id, NULL),
(@s5, DATE_SUB(CURDATE(), INTERVAL 3 DAY), 'Present', @teacher_id, NULL),
(@s5, DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Present', @teacher_id, NULL),
(@s5, DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Present', @teacher_id, NULL),
(@s5, DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Absent', @teacher_id, 'School trip'),
(@s5, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 'Present', @teacher_id, NULL);

-- ============================================
-- SAMPLE NOTIFICATIONS
-- ============================================

INSERT INTO notifications (user_id, message, is_read) VALUES
-- For demo student
(@student_user_id, 'Attendance marked as Present for ' || DATE_SUB(CURDATE(), INTERVAL 1 DAY), FALSE),
(@student_user_id, 'Attendance marked as Present for ' || DATE_SUB(CURDATE(), INTERVAL 2 DAY) || ' - Active participation', TRUE),
(@student_user_id, 'Attendance marked as Absent for ' || DATE_SUB(CURDATE(), INTERVAL 3 DAY) || ' - Medical leave', TRUE),
(@student_user_id, 'Attendance marked as Present for ' || DATE_SUB(CURDATE(), INTERVAL 4 DAY), TRUE),
(@student_user_id, 'Attendance marked as Present for ' || DATE_SUB(CURDATE(), INTERVAL 5 DAY) || ' - Excellent work', TRUE);

-- ============================================
-- USEFUL VIEWS
-- Create views for common queries
-- ============================================

-- View: Student Attendance Summary
CREATE VIEW v_student_attendance_summary AS
SELECT 
    s.student_id,
    u.full_name,
    s.roll_number,
    s.class,
    COUNT(a.attendance_id) as total_days,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_days,
    ROUND((SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id) * 100), 2) as attendance_percentage
FROM students s
JOIN users u ON s.user_id = u.user_id
LEFT JOIN attendance a ON s.student_id = a.student_id
GROUP BY s.student_id, u.full_name, s.roll_number, s.class;

-- View: Recent Attendance
CREATE VIEW v_recent_attendance AS
SELECT 
    a.attendance_id,
    s.roll_number,
    u.full_name as student_name,
    s.class,
    a.date,
    a.status,
    t_user.full_name as marked_by_teacher,
    a.marked_at,
    a.remarks
FROM attendance a
JOIN students s ON a.student_id = s.student_id
JOIN users u ON s.user_id = u.user_id
JOIN teachers t ON a.marked_by = t.teacher_id
JOIN users t_user ON t.user_id = t_user.user_id
ORDER BY a.date DESC, a.marked_at DESC
LIMIT 100;

-- View: Daily Attendance Report
CREATE VIEW v_daily_attendance AS
SELECT 
    a.date,
    COUNT(DISTINCT a.student_id) as total_students,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
    SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_count,
    ROUND((SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(DISTINCT a.student_id) * 100), 2) as attendance_percentage
FROM attendance a
GROUP BY a.date
ORDER BY a.date DESC;

-- ============================================
-- STORED PROCEDURES
-- ============================================

DELIMITER //

-- Procedure: Get Student Attendance Report
CREATE PROCEDURE sp_get_student_report(IN p_student_id INT)
BEGIN
    SELECT 
        a.date,
        a.status,
        a.remarks,
        u.full_name as marked_by,
        a.marked_at
    FROM attendance a
    JOIN teachers t ON a.marked_by = t.teacher_id
    JOIN users u ON t.user_id = u.user_id
    WHERE a.student_id = p_student_id
    ORDER BY a.date DESC;
END //

-- Procedure: Mark Bulk Attendance
CREATE PROCEDURE sp_mark_bulk_attendance(
    IN p_date DATE,
    IN p_status VARCHAR(10),
    IN p_teacher_id INT,
    IN p_class VARCHAR(50)
)
BEGIN
    INSERT INTO attendance (student_id, date, status, marked_by)
    SELECT s.student_id, p_date, p_status, p_teacher_id
    FROM students s
    WHERE s.class = p_class
    ON DUPLICATE KEY UPDATE 
        status = p_status,
        marked_by = p_teacher_id,
        marked_at = NOW();
END //

-- Procedure: Get Attendance Statistics
CREATE PROCEDURE sp_get_attendance_stats(IN p_student_id INT)
BEGIN
    SELECT 
        COUNT(*) as total_days,
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_days,
        SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
        SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late_days,
        ROUND((SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) / COUNT(*) * 100), 2) as percentage
    FROM attendance
    WHERE student_id = p_student_id;
END //

DELIMITER ;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Additional composite indexes
CREATE INDEX idx_attendance_student_date_status ON attendance(student_id, date, status);
CREATE INDEX idx_attendance_date_status ON attendance(date, status);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);

-- ============================================
-- TRIGGERS
-- ============================================

DELIMITER //

-- Trigger: Auto-create notification when attendance is marked
CREATE TRIGGER tr_attendance_notification
AFTER INSERT ON attendance
FOR EACH ROW
BEGIN
    DECLARE student_user_id INT;
    DECLARE notification_message TEXT;
    
    -- Get student's user_id
    SELECT user_id INTO student_user_id
    FROM students
    WHERE student_id = NEW.student_id;
    
    -- Create notification message
    SET notification_message = CONCAT(
        'Attendance marked as ', NEW.status, 
        ' for ', DATE_FORMAT(NEW.date, '%d %b %Y'),
        CASE 
            WHEN NEW.remarks IS NOT NULL AND NEW.remarks != '' 
            THEN CONCAT(' - ', NEW.remarks)
            ELSE ''
        END
    );
    
    -- Insert notification
    INSERT INTO notifications (user_id, message, is_read)
    VALUES (student_user_id, notification_message, FALSE);
END //

-- Trigger: Update notification on attendance update
CREATE TRIGGER tr_attendance_update_notification
AFTER UPDATE ON attendance
FOR EACH ROW
BEGIN
    DECLARE student_user_id INT;
    DECLARE notification_message TEXT;
    
    IF NEW.status != OLD.status OR NEW.remarks != OLD.remarks THEN
        SELECT user_id INTO student_user_id
        FROM students
        WHERE student_id = NEW.student_id;
        
        SET notification_message = CONCAT(
            'Attendance updated to ', NEW.status, 
            ' for ', DATE_FORMAT(NEW.date, '%d %b %Y'),
            CASE 
                WHEN NEW.remarks IS NOT NULL AND NEW.remarks != '' 
                THEN CONCAT(' - ', NEW.remarks)
                ELSE ''
            END
        );
        
        INSERT INTO notifications (user_id, message, is_read)
        VALUES (student_user_id, notification_message, FALSE);
    END IF;
END //

DELIMITER ;

-- ============================================
-- GRANT PERMISSIONS (Optional - for specific user)
-- ============================================

-- If you want to create a specific database user:
-- CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'your_password';
-- GRANT ALL PRIVILEGES ON attendance_system.* TO 'attendance_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Count users by type
SELECT user_type, COUNT(*) as count FROM users GROUP BY user_type;

-- Count students
SELECT COUNT(*) as total_students FROM students;

-- Count teachers
SELECT COUNT(*) as total_teachers FROM teachers;

-- Count attendance records
SELECT COUNT(*) as total_attendance_records FROM attendance;

-- View student attendance summary
SELECT * FROM v_student_attendance_summary;

-- ============================================
-- BACKUP RECOMMENDATION
-- To backup this database, use:
-- mysqldump -u root -p attendance_system > attendance_backup.sql
--
-- To restore:
-- mysql -u root -p attendance_system < attendance_backup.sql
-- ============================================

-- Database setup complete!
SELECT 'Database setup completed successfully!' as Status;
