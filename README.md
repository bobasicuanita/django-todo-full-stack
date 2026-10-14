# Django Todo App

A task management web application built with Django and PostgreSQL. The project includes user authentication, email verification, filtering, password recovery and CRUD operations.

## Features

* User registration and email verification
* User login and logout
* Forgot password and password reset functionality
* Task management
* Filtering
* CRUD

## Tech Stack

* **Backend:** Python, Django
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, Django Templates

## Installation

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file using `.env.example` and configure your database credentials.

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/ in your browser.

## Status

This project is under development and for educational purposes only.

## Acknowledgements

The CSS styling was generated using AI tools. The Django backend, application logic, and authentication flows were developed by me.
