# Project Management Application

This is a simple project management application built with Flask and MySQL.

## Features

- User authentication (login, logout)
- View projects by user
- Add logs to projects

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Create a MySQL database named `app-db`.**
3.  **Create the following tables in the `app-db` database:**
    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        created_by INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users(id)
    );

    CREATE TABLE logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        project_id INT,
        user_id INT,
        log TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```

## Bug Fixes

### "Unknown column 'creator_id' in 'field list'" error

-   **Finding:** The application was using `creator_id` to refer to the creator of a project, but the database schema used `created_by`.
-   **Fix:** Replaced all instances of `creator_id` with `created_by` in `db.py`.

### "Unknown column 'p.course_id' in 'field list'" error

-   **Finding:** The application was trying to select a `course_id` column from the `projects` table, but this column does not exist in the database schema.
-   **Fix:** Removed the `course_id` column from the `SELECT` statements in the `get_projects_by_user` and `get_all_projects` functions in `db.py`.

### `werkzeug.routing.exceptions.BuildError`

-   **Finding:** The `dashboard.html` template was trying to build a URL for the `add_log` endpoint without providing the required `project_id` parameter.
-   **Fix:** Added JavaScript to `dashboard.html` to dynamically update the `add_log` form's `action` attribute with the selected project's ID when the user selects a project from the dropdown menu.

