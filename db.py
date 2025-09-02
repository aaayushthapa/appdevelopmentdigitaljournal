import mysql.connector
from flask import g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="digital_journal"
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    return cursor.fetchone()

def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    return cursor.fetchone()

def add_user(name, email, password, role):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)', (name, email, password, role))
    db.commit()

def update_user_profile(user_id, name, email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, user_id))
    db.commit()

def get_courses(teacher_id=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if teacher_id:
        cursor.execute('SELECT * FROM courses WHERE teacher_id = %s', (teacher_id,))
    else:
        cursor.execute('SELECT * FROM courses')
    return cursor.fetchall()

def get_projects_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT
            p.id,
            p.name,
            p.description,
            p.creator_id,
            p.created_at,
            u.name as creator_name,
            pm.role
        FROM projects p
        JOIN users u ON p.creator_id = u.id
        LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = %s
        WHERE p.creator_id = %s OR p.id IN (SELECT project_id FROM project_members WHERE user_id = %s)
    ''', (user_id, user_id, user_id))
    return cursor.fetchall()

def get_all_projects():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT
            p.id,
            p.name,
            p.description,
            p.creator_id,
            p.created_at,
            u.name as creator_name
        FROM projects p
        JOIN users u ON p.creator_id = u.id
    ''')
    return cursor.fetchall()

def get_project_progress(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.id, p.name, COUNT(l.id) as log_count, MIN(l.created_at) as first_log, MAX(l.created_at) as last_log
        FROM projects p
        LEFT JOIN logs l ON p.id = l.project_id
        WHERE p.creator_id = %s OR p.id IN (SELECT project_id FROM project_members WHERE user_id = %s)
        GROUP BY p.id, p.name
    ''', (user_id, user_id))
    return cursor.fetchall()

def create_project(name, description, creator_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO projects (name, description, creator_id) VALUES (%s, %s, %s)', (name, description, creator_id))
    project_id = cursor.lastrowid
    cursor.execute('INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)', (project_id, creator_id, 'admin'))
    db.commit()
    return project_id

def get_groups_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.id, p.name, pm.role, (SELECT COUNT(*) FROM project_members WHERE project_id = p.id) as member_count
        FROM projects p
        JOIN project_members pm ON p.id = pm.project_id
        WHERE pm.user_id = %s
    ''', (user_id,))
    return cursor.fetchall()

def get_logs_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT l.*, p.name as project_name
        FROM logs l
        JOIN projects p ON l.project_id = p.id
        WHERE l.user_id = %s
        ORDER BY l.created_at DESC
    ''', (user_id,))
    return cursor.fetchall()

def get_project_by_id(project_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    return cursor.fetchone()

def get_project_members(project_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
        SELECT u.id, u.name, u.avatar_url
        FROM users u
        JOIN project_members pm ON u.id = pm.user_id
        WHERE pm.project_id = %s
    ''', (project_id,))
    return cursor.fetchall()

def get_logs_by_project(project_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM logs WHERE project_id = %s ORDER BY created_at DESC', (project_id,))
    return cursor.fetchall()

def get_assignments_by_course(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM assignments WHERE course_id = %s', (course_id,))
    return cursor.fetchall()

def get_submissions_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM submissions WHERE user_id = %s', (user_id,))
    return cursor.fetchall()

def get_assignment_by_id(assignment_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM assignments WHERE id = %s', (assignment_id,))
    return cursor.fetchone()

def get_submission(user_id, assignment_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM submissions WHERE user_id = %s AND assignment_id = %s', (user_id, assignment_id))
    return cursor.fetchone()

def get_reports_by_user(user_id):
    # This is a placeholder. You'll need to define what a 'report' is.
    return []

def get_submissions_by_assignment(assignment_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, u.name as student_name
        FROM submissions s
        JOIN users u ON s.user_id = u.id
        WHERE s.assignment_id = %s
    """, (assignment_id,))
    return cursor.fetchall()

def add_log(project_id, user_id, title, content, media_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO logs (project_id, user_id, title, content, media_path) VALUES (%s, %s, %s, %s, %s)', (project_id, user_id, title, content, media_path))
    db.commit()

def submit_assignment(assignment_id, user_id, file_path, comments):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO submissions (assignment_id, user_id, file_path, comments) VALUES (%s, %s, %s, %s)', (assignment_id, user_id, file_path, comments))
    db.commit()

def grade_submission(submission_id, grade, feedback):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE submissions SET grade = %s, feedback = %s WHERE id = %s', (grade, feedback, submission_id))
    db.commit()