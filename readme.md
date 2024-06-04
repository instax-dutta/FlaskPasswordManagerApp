# PassGuard - By RacerOP

PassGuard is a secure and user-friendly password manager application built using Flask. This application stores your passwords securely and allows you to access them with ease. The passwords are encrypted using a passphrase that is generated and stored securely.

## Features

- **Add New Password**: Add a new password with website, username, and password fields.
- **View Passwords**: View your stored passwords. Passwords are hidden by default and can be revealed by entering the passphrase.
- **Edit Passwords**: Edit the details of an existing password entry.
- **Delete Passwords**: Delete an existing password entry.
- **Secure Passphrase**: Uses a generated passphrase to encrypt and decrypt passwords.
- **Automatic Hide**: Passwords are automatically hidden again after 20 seconds.

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/instax-dutta/FlaskPasswordManagerApp.git
    cd FlaskPasswordManagerApp
    ```

2. **Install Dependencies**

    Ensure you have Python installed. Then, install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. **Setup the Database**

    Initialize the database:

    ```sh
    python app.py
    ```

    This will create the necessary database file and generate a passphrase if it doesn't already exist.

## Running the Application

To run the application, execute:

```sh
python app.py
```

The application will start and you will see a popup message indicating that the password manager is running on `localhost:7777`. Open your web browser and go to:

```
http://localhost:7777
```

## Using the Executable

1. **Download the Executable**

    Download the latest version of the executable from the [releases](https://github.com/instax-dutta/FlaskPasswordManagerApp/releases) section of the repository.

2. **Run the Executable**

    Navigate to the directory where you downloaded the executable and run it:

    ```sh
    PassGuard.exe
    ```

    The application will start and you will see a popup message indicating that the password manager is running on `localhost:7777`.

3. **Access the Application**

    Open your web browser and go to:

    ```
    http://localhost:7777
    ```

## Usage

- **Login**: Enter the passphrase to access the password manager.
- **Add Password**: Click on "Add New Password" to add a new password entry.
- **View Password**: Click the eye icon next to a password field and enter the passphrase to view the password. The password will be hidden again after 20 seconds.
- **Edit Password**: Click "Edit" next to a password entry to edit its details.
- **Delete Password**: Click "Delete" next to a password entry to delete it.

## Passphrase Management

- The passphrase is generated and stored in a file named `passphrase.txt` in the root directory of the project.
- Ensure you keep this passphrase secure as it is used to encrypt and decrypt your passwords.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
