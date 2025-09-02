from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
import json
from fpdf import FPDF
import io
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.teardown_appcontext
def teardown_db(exception):
    db.close_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role required decorator
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.get_user_by_email(email)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session['user_avatar'] = user['avatar_url'] if user['avatar_url'] else f"https://ui-avatars.com/api/?name={user['name']}&background=random"
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        hashed = generate_password_hash(password)
        
        try:
            db.add_user(name, email, hashed, role)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Email already exists or registration error.', 'danger')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    projects = db.get_projects_by_user(user_id)
    assignments = [] # Placeholder
    feedback = [] # Placeholder
    
    return render_template('dashboard.html', 
                          projects=projects, 
                          assignments=assignments, 
                          feedback=feedback)

@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user_id = session['user_id']
        
        # Since db.py does not have a create_project function, we add it.
        database = db.get_db()
        cursor = database.cursor()
        cursor.execute(
            "INSERT INTO projects (name, description, creator_id) VALUES (%s, %s, %s)",
            (name, description, user_id)
        )
        project_id = cursor.lastrowid
        
        # Add creator as project member
        cursor.execute(
            "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)",
            (project_id, user_id, 'admin')
        )
        
        database.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects'))

# Projects Route
@app.route('/projects')
@login_required
def projects():
    user_id = session['user_id']
    
    if session['user_role'] == 'teacher':
        projects = db.get_all_projects()
    else:
        projects = db.get_projects_by_user(user_id)

    return render_template('projects.html', projects=projects)

@app.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = db.get_project_by_id(project_id)
    members = db.get_project_members(project_id)
    logs = db.get_logs_by_project(project_id)
    return render_template('project_detail.html', project=project, members=members, logs=logs)

@app.route('/project/<int:project_id>/add_log', methods=['POST'])
@login_required
def add_log(project_id):
    user_id = session['user_id']
    title = request.form['title']
    content = request.form['content']
    media_path = None

    if 'media' in request.files:
        file = request.files['media']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            media_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(media_path)
            media_path = os.path.join(UPLOAD_FOLDER, filename)

    # Since db.py does not have an add_log function, we add it.
    database = db.get_db()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO logs (project_id, user_id, title, content, media_path) VALUES (%s, %s, %s, %s, %s)",
        (project_id, user_id, title, content, media_path)
    )
    database.commit()

    flash('Log entry added successfully!', 'success')
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/assignments')
@login_required
def assignments():
    user_id = session['user_id']
    # This is a placeholder. You'll need to fetch assignments based on user's courses.
    all_assignments = []
    submitted_assignments = []
    return render_template('assignments.html', all_assignments=all_assignments, submitted_assignments=submitted_assignments)

@app.route('/assignment/<int:assignment_id>')
@login_required
def assignment_detail(assignment_id):
    assignment = db.get_assignment_by_id(assignment_id)
    submission = db.get_submission(session['user_id'], assignment_id)
    return render_template('assignment_detail.html', assignment=assignment, submission=submission)

@app.route('/submit_assignment/<int:assignment_id>', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    user_id = session['user_id']
    comments = request.form['comments']
    file_path = None

    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Since db.py does not have a submit_assignment function, we add it.
    database = db.get_db()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO submissions (assignment_id, user_id, file_path, comments) VALUES (%s, %s, %s, %s)",
        (assignment_id, user_id, file_path, comments)
    )
    database.commit()

    flash('Assignment submitted successfully!', 'success')
    return redirect(url_for('assignment_detail', assignment_id=assignment_id))

@app.route('/submissions/<int:assignment_id>')
@login_required
@role_required(['teacher', 'admin'])
def view_submissions(assignment_id):
    submissions = db.get_submissions_by_assignment(assignment_id)
    return render_template('submissions.html', submissions=submissions)

@app.route('/grade_submission/<int:submission_id>', methods=['POST'])
@login_required
@role_required(['teacher', 'admin'])
def grade_submission(submission_id):
    grade = request.form['grade']
    feedback = request.form['feedback']

    # Since db.py does not have a grade_submission function, we add it.
    database = db.get_db()
    cursor = database.cursor()
    cursor.execute(
        "UPDATE submissions SET grade = %s, feedback = %s WHERE id = %s",
        (grade, feedback, submission_id)
    )
    database.commit()

    flash('Submission graded successfully!', 'success')
    return redirect(url_for('view_submissions', assignment_id=request.form['assignment_id']))

@app.route('/logs')
@login_required
def logs():
    user_id = session['user_id']
    logs = db.get_logs_by_user(user_id)
    return render_template('logs.html', logs=logs)

@app.route('/progress')
@login_required
def progress():
    user_id = session['user_id']
    project_progress = db.get_project_progress(user_id)
    return render_template('progress.html', project_progress=project_progress)

@app.route('/reports')
@login_required
def reports():
    user_id = session['user_id']
    reports = db.get_reports_by_user(user_id)
    return render_template('reports.html', reports=reports)

@app.route('/groups')
@login_required
def groups():
    user_id = session['user_id']
    groups = db.get_groups_by_user(user_id)
    return render_template('groups.html', groups=groups)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_id = session['user_id']
        db.update_user_profile(user_id, name, email)
        session['user_name'] = name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)