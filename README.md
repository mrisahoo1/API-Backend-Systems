# API-Backend-Systems -- README

Welcome to the Backend System for User Data Management. This project provides a robust backend system developed in Python and Django to manage user data through a set of APIs.

## Frameworks Used

This project leverages the following technologies:

- **Python**: The programming language that forms the foundation of the backend logic.
- **Django**: A powerful and versatile web framework used for building web applications.
- **Django REST framework**: An extension to Django that simplifies the creation of RESTful APIs.

## Database Schema

The backend system employs a well-structured database schema with the following main models:

1. **User**:
   - `username` (CharField): The unique username of the user.
   - `email` (EmailField): The email address of the user.
   - `password` (CharField): The hashed password of the user.
   - `full_name` (CharField): The full name of the user.
   - `age` (PositiveIntegerField): The age of the user.
   - `gender` (CharField): The gender of the user.

2. **KeyValueData**:
   - `key` (CharField): The key associated with the data.
   - `value` (TextField): The corresponding value of the data.

## Getting Started

### Prerequisites

To run this system on your local machine, you need:

- Python (3.6+)
- pip (package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mrisahoo1/API-Backend-Systems.git
   cd backend-systems
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Running the System

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Access the API endpoints at `http://localhost:8000/api/`.


## Contributing

We welcome contributions to enhance and improve this project. If you have suggestions or find issues, please open an issue or submit a pull request.

## Contact

If you have any questions or feedback, feel free to reach out to me at mrityunjay.sahoo6@gmail.com

## License

This project is licensed under the [MIT License](LICENSE).
