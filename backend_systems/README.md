# Backend System - README

## 1. Choices of Framework

This backend system is built using Python and Django, a popular web framework that provides a robust and scalable infrastructure for building web applications and APIs. Django offers a wide range of built-in features like ORM, authentication, serialization, and routing, which makes it easy to implement the required functionalities efficiently. Additionally, Django's ecosystem has excellent community support and a vast number of third-party packages that can be used to extend the application further.

## 2. DB Schema

The backend system uses a simple database schema with two models:

1. User: Represents the registered users in the system. The fields include username, email, password, full_name, age, and gender.

2. Data: Stores key-value pairs of data. The fields include key (unique identifier) and value (data_value).

The DB schema is implemented using Django's ORM, allowing easy management and querying of the database through Python code.

## 3. Instructions to Run the Code

To run the backend system, follow these steps:

1. Ensure you have Python and Django installed on your machine. If not, install them by running:

2. Clone the repository or download the source code.

3. Navigate to the project directory containing `manage.py` in the terminal.

4. Run the following command to apply the database migrations:
    python manage.py migrate

5. Start the development server by running:
    python manage.py runserver

6. The backend system will now be accessible at `http://127.0.0.1:8000/`.

## 4. Instructions to Setup the Code

To set up the backend system for development or production, follow these steps:

1. Clone the repository or download the source code.

2. Create a virtual environment to isolate the project dependencies. Run:
    python -m venv myVenv

3. Activate the virtual environment:
- On Windows:
  ```
  myVenv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source myVenv/bin/activate
  ```

4. Install the required dependencies using `pip`:
    pip install -r requirements.txt

5. Set up the database by applying migrations:
    python manage.py migrate

6. (Optional) Load initial data (if any) using fixtures or custom management commands.

7. Start the development server:
    python manage.py runserver

8. The backend system will now be accessible at `http://127.0.0.1:8000/`.

That's it! The backend system is now set up and ready to be used.
