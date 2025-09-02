import mysql.connector

# --- Database Configuration ---
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
}

# --- Database and Table Creation ---

def create_database():
    """Creates the database if it doesn't exist."""
    try:
        # Connect to MySQL server
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS app_dev1")
        print("Database 'app_dev1' created or already exists.")

        db.close()

    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def create_tables():
    """Creates the necessary tables in the database."""
    try:
        # Connect to the app_dev1 database
        db = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='app_dev1'
        )
        cursor = db.cursor()

        # Table creation queries
        queries = [
            """CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('student', 'teacher') NOT NULL,
                avatar_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                creator_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(id)
            )""",
            """CREATE TABLE IF NOT EXISTS project_members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT NOT NULL,
                user_id INT NOT NULL,
                role VARCHAR(50) NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )""",
            """CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT NOT NULL,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                media_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )""",
            """CREATE TABLE IF NOT EXISTS assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATETIME,
                course_id INT,  -- Assuming a courses table exists
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                assignment_id INT NOT NULL,
                user_id INT NOT NULL,
                file_path VARCHAR(255),
                comments TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                grade VARCHAR(10),
                feedback TEXT,
                FOREIGN KEY (assignment_id) REFERENCES assignments(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )"""
        ]

        # Execute all table creation queries
        for query in queries:
            cursor.execute(query)
        
        print("All tables created successfully.")
        db.commit()
        db.close()

    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")

if __name__ == '__main__':
    create_database()
    create_tables()