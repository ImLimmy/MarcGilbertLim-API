# FastAPI User Management System

This is a user management system built with FastAPI, providing functionalities for user registration, login, profile retrieval, updates, and deletion. It includes role-based access control (admin and user roles) to manage user profiles.

## Features

- User registration
- User login with JWT authentication
- Retrieve all user profiles (admin-only)
- Retrieve a single user profile
- Update a user profile
- Delete a user profile

## Requirements

- Python 3.7 or higher
- MongoDB (for database storage)

## Installation

1. Clone the repository:
   
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. python -m venv venv
venv\Scripts\activate

3. pip install -r requirements.txt

4. JWT_SECRET_KEY=S_KEY

5. uvicorn app.main:app --reload

6. Open your browser and navigate to http://localhost:8000/docs to view the interactive API documentation provided by FastAPI.

API Endpoints
POST /register: Register a new user.
POST /login: Login a user and receive a JWT token.
GET /users: Retrieve all user profiles (admin-only).
GET /users/{user_id}: Retrieve a single user profile.
PUT /users/{user_id}: Update a user profile.
DELETE /users/{user_id}: Delete a user profile.

