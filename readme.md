# PassGuard - By Racer OP

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Initialization](#database-initialization)
- [Security](#security)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Introduction
PassGuard is a secure password manager built with Flask that allows users to store, retrieve, and manage their passwords securely. It uses encryption to protect stored passwords and requires a passphrase for various operations, ensuring that your sensitive information remains protected.

## Features
- **Secure Storage**: Passwords are encrypted using strong encryption algorithms.
- **Passphrase Protection**: A user-defined passphrase is required to access, add, edit, or delete passwords.
- **User-Friendly Interface**: A clean and intuitive web interface for managing passwords.
- **Dark Mode**: A sleek dark theme to reduce eye strain.
- **Hidden Storage**: Sensitive files are stored in a hidden directory to enhance security.

## Installation
### Prerequisites
- Python 3.6 or higher
- `pip` (Python package installer)

### Clone the Repository
```bash
git clone https://github.com/instax-dutta/FlaskPasswordManagerApp.git
cd FlaskPasswordManagerApp
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Initialize the Database
The database is automatically initialized when you first run the application. If you need to manually initialize the database, follow these steps:
1. Ensure the `.hidden` directory exists.
2. Run the application once to trigger database creation.

## Usage
### Running the Application
Start the Flask application using the following command:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:7777`.

### Accessing the Application
1. Open a web browser and navigate to `http://127.0.0.1:7777`.
2. Enter the passphrase to log in. The passphrase is stored in the `passphrase.txt` file in the root directory.

### Managing Passwords
- **Add Password**: Click on "Add New Password" and fill in the details.
- **Edit Password**: Click on the "Edit" button next to a password entry, enter the passphrase, and update the details.
- **Delete Password**: Click on the "Delete" button next to a password entry and confirm by entering the passphrase.

## Project Structure
```plaintext
PassGuard/
│
├── .hidden/
│   └── passwords.db       # SQLite database file (hidden)
│
├── templates/
│   ├── add.html           # Template for adding a new password
│   ├── edit.html          # Template for editing a password
│   ├── index.html         # Main template for displaying passwords
│   └── login.html         # Template for passphrase login
│
├── app.py                 # Main application script
├── passphrase.txt         # File storing the passphrase and salt
├── passguard.spec         # PyInstaller specification file
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## API Endpoints
### GET /
Displays the main page with a list of stored passwords. Requires authentication via the passphrase.

### GET /login
Displays the passphrase login page.

### POST /login
Authenticates the user using the provided passphrase.

### GET /logout
Logs the user out by clearing the session.

### POST /validate_passphrase
Validates the passphrase provided in the request body. Returns a JSON response indicating whether the passphrase is valid.

### GET /add
Displays the page for adding a new password. Requires authentication.

### POST /add
Adds a new password to the database. Requires authentication.

### GET /edit/<id>
Displays the page for editing an existing password. Requires authentication.

### POST /edit/<id>
Updates an existing password in the database. Requires authentication.

### GET /delete/<id>
Deletes a password from the database. Requires authentication.

## Database Initialization
The database is automatically initialized when the application starts if it does not already exist. The database file is stored in a hidden directory `.hidden/passwords.db`.

## Security
- **Encryption**: Passwords are encrypted using the `Fernet` symmetric encryption provided by the `cryptography` library.
- **Passphrase**: A passphrase is required for accessing, adding, editing, or deleting passwords. The passphrase is stored securely in the `passphrase.txt` file.
- **Hidden Directory**: Sensitive files, including the database, are stored in a hidden directory to prevent unauthorized access.

## Future Enhancements
- **Two-Factor Authentication**: Add an additional layer of security with 2FA.
- **Password Strength Checker**: Implement a feature to check the strength of passwords being added.
- **Backup and Restore**: Enable users to backup and restore their password data securely.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them with clear messages.
4. Push your changes to your fork.
5. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

For any questions or support, please contact [contact@sdad.pro].

Happy Password Managing!
