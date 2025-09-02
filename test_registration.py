import mysql.connector
from werkzeug.security import generate_password_hash

# --- Database Configuration ---
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'app_dev1',
    'raise_on_warnings': True
}

def add_sample_users():
    """Adds sample users for testing purposes."""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Sample users data
        users = [
            ("John Doe", "john@example.com", generate_password_hash("password123"), "student"),
            ("Jane Smith", "jane@example.com", generate_password_hash("password123"), "teacher"),
            ("Admin User", "admin@example.com", generate_password_hash("admin123"), "admin"),
            ("Parent User", "parent@example.com", generate_password_hash("parent123"), "parent")
        ]
        
        # Insert sample users
        cursor.executemany(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            users
        )
        
        db.commit()
        print(f"Successfully added {cursor.rowcount} sample users.")
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error adding sample users: {err}")

def test_registration():
    """Tests the registration functionality by adding a test user."""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Test user
        test_user = ("Test Student", "test@example.com", generate_password_hash("test123"), "student")
        
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            test_user
        )
        
        db.commit()
        print("Registration test successful - test user added.")
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Registration test failed: {err}")

if __name__ == '__main__':
    add_sample_users()
    test_registration()