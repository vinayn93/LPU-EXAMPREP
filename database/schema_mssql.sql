-- ============================================================================
-- LPU ExamPrep AI — Microsoft SQL Server Database Schema Definition Script
-- T-SQL Compatible with SQL Server 2017+ / Azure SQL Database
-- Normalized Relational Schema with Views, Indexes, Triggers, and Stored Procedures
-- ============================================================================

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'LPUExamPrepDB')
BEGIN
    CREATE DATABASE LPUExamPrepDB;
END;
GO

USE LPUExamPrepDB;
GO

-- 1. ROLES TABLE
IF OBJECT_ID('dbo.Roles', 'U') IS NOT NULL DROP TABLE dbo.Roles;
CREATE TABLE dbo.Roles (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name NVARCHAR(30) NOT NULL UNIQUE CHECK (role_name IN ('STUDENT', 'FACULTY', 'ADMIN'))
);

-- 2. PROGRAMS TABLE (e.g., B.Tech CSE, BCA, B.Sc IT)
IF OBJECT_ID('dbo.Programs', 'U') IS NOT NULL DROP TABLE dbo.Programs;
CREATE TABLE dbo.Programs (
    program_id INT IDENTITY(1,1) PRIMARY KEY,
    program_code NVARCHAR(20) NOT NULL UNIQUE,
    program_name NVARCHAR(100) NOT NULL,
    department NVARCHAR(100) NOT NULL
);

-- 3. ACADEMIC YEARS & SEMESTERS
IF OBJECT_ID('dbo.AcademicYears', 'U') IS NOT NULL DROP TABLE dbo.AcademicYears;
CREATE TABLE dbo.AcademicYears (
    year_id INT IDENTITY(1,1) PRIMARY KEY,
    year_number INT NOT NULL CHECK (year_number BETWEEN 1 AND 5),
    year_title NVARCHAR(30) NOT NULL
);

IF OBJECT_ID('dbo.Semesters', 'U') IS NOT NULL DROP TABLE dbo.Semesters;
CREATE TABLE dbo.Semesters (
    semester_id INT IDENTITY(1,1) PRIMARY KEY,
    year_id INT NOT NULL FOREIGN KEY REFERENCES dbo.AcademicYears(year_id),
    semester_number INT NOT NULL CHECK (semester_number BETWEEN 1 AND 10),
    semester_name NVARCHAR(30) NOT NULL
);

-- 4. USERS TABLE
IF OBJECT_ID('dbo.Users', 'U') IS NOT NULL DROP TABLE dbo.Users;
CREATE TABLE dbo.Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(120) NOT NULL,
    email NVARCHAR(150) NOT NULL UNIQUE,
    hashed_password NVARCHAR(255) NOT NULL,
    role_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Roles(role_id),
    program_id INT NULL FOREIGN KEY REFERENCES dbo.Programs(program_id),
    registration_number NVARCHAR(50) NULL,
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT SYSDATETIME()
);

-- 5. SUBJECTS TABLE (e.g., CSE305 - Database Management Systems)
IF OBJECT_ID('dbo.Subjects', 'U') IS NOT NULL DROP TABLE dbo.Subjects;
CREATE TABLE dbo.Subjects (
    subject_id INT IDENTITY(101,1) PRIMARY KEY,
    program_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Programs(program_id),
    semester_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Semesters(semester_id),
    subject_code NVARCHAR(20) NOT NULL UNIQUE,
    subject_name NVARCHAR(120) NOT NULL,
    credits INT DEFAULT 4,
    description NVARCHAR(MAX) NULL
);

-- 6. UNITS TABLE
IF OBJECT_ID('dbo.Units', 'U') IS NOT NULL DROP TABLE dbo.Units;
CREATE TABLE dbo.Units (
    unit_id INT IDENTITY(1,1) PRIMARY KEY,
    subject_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Subjects(subject_id) ON DELETE CASCADE,
    unit_number INT NOT NULL,
    unit_title NVARCHAR(150) NOT NULL,
    exam_weightage_pct INT DEFAULT 20 CHECK (exam_weightage_pct BETWEEN 5 AND 50)
);

-- 7. SYLLABUS & AUTHORIZED RESOURCES
IF OBJECT_ID('dbo.Resources', 'U') IS NOT NULL DROP TABLE dbo.Resources;
CREATE TABLE dbo.Resources (
    resource_id INT IDENTITY(1,1) PRIMARY KEY,
    subject_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Subjects(subject_id),
    unit_id INT NULL FOREIGN KEY REFERENCES dbo.Units(unit_id),
    title NVARCHAR(200) NOT NULL,
    resource_type NVARCHAR(30) NOT NULL CHECK (resource_type IN ('SYLLABUS', 'NOTES', 'PYQ', 'PDF', 'REFERENCE_LINK')),
    file_path_or_url NVARCHAR(500) NOT NULL,
    uploaded_by_user_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Users(user_id),
    created_at DATETIME2 DEFAULT SYSDATETIME()
);

-- 8. QUESTION BANK & MOCK TESTS
IF OBJECT_ID('dbo.Questions', 'U') IS NOT NULL DROP TABLE dbo.Questions;
CREATE TABLE dbo.Questions (
    question_id INT IDENTITY(1001,1) PRIMARY KEY,
    subject_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Subjects(subject_id),
    unit_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Units(unit_id),
    question_text NVARCHAR(MAX) NOT NULL,
    option_a NVARCHAR(255) NOT NULL,
    option_b NVARCHAR(255) NOT NULL,
    option_c NVARCHAR(255) NOT NULL,
    option_d NVARCHAR(255) NOT NULL,
    correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('A', 'B', 'C', 'D')),
    explanation NVARCHAR(MAX) NULL,
    difficulty NVARCHAR(15) DEFAULT 'MEDIUM' CHECK (difficulty IN ('EASY', 'MEDIUM', 'HARD')),
    marks INT DEFAULT 2
);

-- 9. TEST ATTEMPTS & RESULTS
IF OBJECT_ID('dbo.TestAttempts', 'U') IS NOT NULL DROP TABLE dbo.TestAttempts;
CREATE TABLE dbo.TestAttempts (
    attempt_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Users(user_id),
    subject_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Subjects(subject_id),
    total_questions INT NOT NULL,
    correct_answers INT NOT NULL,
    score_percentage FLOAT NOT NULL,
    time_taken_seconds INT NOT NULL,
    attempted_at DATETIME2 DEFAULT SYSDATETIME()
);

-- INDEXES FOR FAST QUERY PERFORMANCE
CREATE INDEX IX_Users_Email ON dbo.Users(email);
CREATE INDEX IX_Subjects_Code ON dbo.Subjects(subject_code);
CREATE INDEX IX_Questions_Subject_Unit ON dbo.Questions(subject_id, unit_id);
CREATE INDEX IX_TestAttempts_User ON dbo.TestAttempts(user_id);

-- STORED PROCEDURE: Generate Student Performance Report
GO
CREATE PROCEDURE dbo.sp_GetStudentPerformanceReport
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        u.full_name,
        u.email,
        p.program_name,
        s.subject_code,
        s.subject_name,
        COUNT(ta.attempt_id) AS total_tests_taken,
        AVG(ta.score_percentage) AS average_score_pct,
        MAX(ta.score_percentage) AS highest_score_pct
    FROM dbo.Users u
    JOIN dbo.Programs p ON u.program_id = p.program_id
    LEFT JOIN dbo.TestAttempts ta ON u.user_id = ta.user_id
    LEFT JOIN dbo.Subjects s ON ta.subject_id = s.subject_id
    WHERE u.user_id = @UserID
    GROUP BY u.full_name, u.email, p.program_name, s.subject_code, s.subject_name;
END;
GO

-- STORED PROCEDURE: Identify Student Weak Topics
GO
CREATE PROCEDURE dbo.sp_IdentifyWeakTopics
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        un.unit_title,
        s.subject_name,
        AVG(ta.score_percentage) AS avg_unit_score
    FROM dbo.TestAttempts ta
    JOIN dbo.Subjects s ON ta.subject_id = s.subject_id
    JOIN dbo.Units un ON s.subject_id = un.subject_id
    WHERE ta.user_id = @UserID AND ta.score_percentage < 65.0
    GROUP BY un.unit_title, s.subject_name
    ORDER BY avg_unit_score ASC;
END;
GO
