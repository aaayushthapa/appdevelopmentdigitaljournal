import mysql.connector
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# --- Database Configuration ---
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'app_dev1',
    'raise_on_warnings': True
}

def populate_sample_data():
    """Populates the database with comprehensive sample data for testing."""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Clear existing data (except users)
        cursor.execute("DELETE FROM submissions")
        cursor.execute("DELETE FROM logs")
        cursor.execute("DELETE FROM project_members")
        cursor.execute("DELETE FROM projects")
        cursor.execute("DELETE FROM assignments")
        
        # Get existing user IDs
        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        if not user_ids:
            print("No users found. Please run test_registration.py first.")
            return
        
        # Create sample projects
        projects = [
            ("Web Development Project", "Create a responsive website for a local business", user_ids[0]),
            ("Database Design Assignment", "Design and implement a normalized database schema", user_ids[1]),
            ("Mobile App Development", "Build a simple mobile app using React Native", user_ids[0]),
            ("AI Research Paper", "Write a research paper on machine learning applications", user_ids[1])
        ]
        
        project_ids = []
        for name, description, creator_id in projects:
            cursor.execute(
                "INSERT INTO projects (name, description, creator_id) VALUES (%s, %s, %s)",
                (name, description, creator_id)
            )
            project_ids.append(cursor.lastrowid)
        
        # Add project members
        for project_id in project_ids:
            # Add creator as admin
            cursor.execute(
                "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)",
                (project_id, user_ids[0], "admin")
            )
            # Add other users as members
            for user_id in user_ids[1:]:
                cursor.execute(
                    "INSERT INTO project_members (project_id, user_id, role) VALUES (%s, %s, %s)",
                    (project_id, user_id, "member")
                )
        
        # Create sample assignments
        assignments = [
            ("Python Programming Basics", "Complete exercises 1-5 in the Python textbook", datetime.now() + timedelta(days=7)),
            ("Database Normalization", "Normalize the given database schema to 3NF", datetime.now() + timedelta(days=14)),
            ("Web Security Report", "Write a report on common web security vulnerabilities", datetime.now() + timedelta(days=21)),
            ("Mobile UI Design", "Design mockups for a mobile application interface", datetime.now() + timedelta(days=10))
        ]
        
        assignment_ids = []
        for title, description, due_date in assignments:
            cursor.execute(
                "INSERT INTO assignments (title, description, due_date) VALUES (%s, %s, %s)",
                (title, description, due_date)
            )
            assignment_ids.append(cursor.lastrowid)
        
        # Create sample logs
        logs = [
            (project_ids[0], user_ids[0], "Project Setup", "Set up the development environment and created initial project structure", None),
            (project_ids[0], user_ids[1], "UI Design", "Created wireframes and mockups for the website", "static/uploads/mockup.png"),
            (project_ids[1], user_ids[0], "Database Schema", "Designed the initial database schema with proper relationships", None),
            (project_ids[2], user_ids[1], "Mobile App UI", "Implemented the basic mobile app interface", "static/uploads/mobile_ui.png")
        ]
        
        for project_id, user_id, title, content, media_path in logs:
            cursor.execute(
                "INSERT INTO logs (project_id, user_id, title, content, media_path) VALUES (%s, %s, %s, %s, %s)",
                (project_id, user_id, title, content, media_path)
            )
        
        # Create sample submissions
        submissions = [
            (assignment_ids[0], user_ids[0], "static/uploads/python_exercises.pdf", "Completed all exercises with detailed comments"),
            (assignment_ids[1], user_ids[1], "static/uploads/database_schema.pdf", "Normalized schema with detailed documentation"),
            (assignment_ids[2], user_ids[0], "static/uploads/security_report.pdf", "Comprehensive security analysis report"),
            (assignment_ids[3], user_ids[1], "static/uploads/ui_mockups.pdf", "Mobile app UI mockups with annotations")
        ]
        
        for assignment_id, user_id, file_path, comments in submissions:
            cursor.execute(
                "INSERT INTO submissions (assignment_id, user_id, file_path, comments) VALUES (%s, %s, %s, %s)",
                (assignment_id, user_id, file_path, comments)
            )
        
        db.commit()
        print(f"Successfully populated database with:")
        print(f"- {len(project_ids)} projects")
        print(f"- {len(assignment_ids)} assignments")
        print(f"- {len(logs)} log entries")
        print(f"- {len(submissions)} submissions")
        
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error populating sample data: {err}")

if __name__ == '__main__':
    populate_sample_data()