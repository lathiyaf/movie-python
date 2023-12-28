# Movie Blog Project

# Overview
- This project is a Django-based web application that allows users to register, sign in, create movie blogs, and update their content. The project utilizes PostgreSQL for data storage and management.

# Key Feature
- User registration and authentication
- Movie blog creation with poster upload, title, and release year
- Movie blog update functionality

# Technologies
- Python
- Django REST Framework
- PostgreSQL

# Installation and Setup
## 1. Create a virtual environment and activate it:
- <code>python -m venv venv</code>
- <code>source venv/bin/activate</code>

## 2. Install dependencies:
- <code>pip install -r requirements.txt</code>

## 3. Create a PostgreSQL database and configure its settings in movie_page/settings.py:
- DATABASES = {
-    	'default': {
-         ENGINE': 'django.db.backends.postgresql',
-         'NAME': 'your_database_name',
-        	'USER': 'your_database_user',
-         'PASSWORD': 'your_database_password',
-        	'HOST': 'localhost',
-        	'PORT': '5432',
-     	}
- }

## 4. Apply database migrations:
- <code>python manage.py makemigrations</code>
- <code>python manage.py migrate</code>

# Running the Application

## 1. Start the development server:
- <code>python manage.py runserver</code>

## 2. Access the admin portal of backend in your web browser, typically at http://127.0.0.1:8000/admin/

## 3. Create a superuser:
- <code>python manage.py createsuperuser</code>