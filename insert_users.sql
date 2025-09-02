INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@test.com', 'pbkdf2:sha256:600000$Vv2ODvFj8q3RzW2g$9c3f2b9f7a6e2c5d5f6e5f4a3b9a3e4d1b2c8a7c6b5d4e3f2a1b0c9d8e7f6a5b', 'admin'),
('Teacher User', 'teacher@test.com', 'pbkdf2:sha256:600000$Vv2ODvFj8q3RzW2g$9c3f2b9f7a6e2c5d5f6e5f4a3b9a3e4d1b2c8a7c6b5d4e3f2a1b0c9d8e7f6a5b', 'teacher'),
('Student User', 'student@test.com', 'pbkdf2:sha256:600000$Vv2ODvFj8q3RzW2g$9c3f2b9f7a6e2c5d5f6e5f4a3b9a3e4d1b2c8a7c6b5d4e3f2a1b0c9d8e7f6a5b', 'student');