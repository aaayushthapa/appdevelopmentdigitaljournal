import mysql.connector

# --- Database Configuration ---
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'app_dev1',
    'raise_on_warnings': True
}

def update_role_column():
    """Updates the role column to include all required values."""
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Drop the existing ENUM constraint and create new one with all roles
        cursor.execute("""
            ALTER TABLE users 
            MODIFY COLUMN role ENUM('student', 'teacher', 'admin', 'parent') NOT NULL
        """)
        
        print("Role column updated successfully to include all 4 role types.")
        db.commit()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"Error updating role column: {err}")

if __name__ == '__main__':
    update_role_column()