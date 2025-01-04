# spam_checker

# Project Setup Instructions

## Install Dependencies

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Set Up the Database

Run these commands to set up and migrate the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Development Server

Start the development server using:

```bash
python manage.py runserver
```

# Open Client.ipynb file for testing the APIs

## Notes

- **ACCESS TOKEN**: After logging in, you will receive an ACCESS TOKEN. This token must be included in the headers (`Authorization: Bearer <access_token>`) for all subsequent API requests.
- **Testing File**: Modify the `client.ipynb` file to add your own data and test the APIs as needed.

## Testing the APIs with `client.ipynb`

### Registration

First, register a new user by changing data in client file in the following format:

```python
import uuid

registration_data = {
    "name": "Ritesh Patidar",
    "phone_number": "+918821918000",
    "email": f"ritesh{uuid.uuid4()}@example.com",  
    "password": "securepassword"
}
```

### Login
 
Change the login data in the following format:


```python
login_data = {
    "phone_number": "+918821918000",
    "password": "securepassword"
}
```

### Add Contact

Change the contact details in the following format in the client file:

```python
if __name__ == '__main__':
    contact_name = "Ritesh"
    contact_phone_number = "+918821918000"
    contact_email = None  # Set to None if no email is provided
    print("Adding Contact...")
    add_contact(contact_name, contact_phone_number, contact_email)
```

### Report Spam

To report a phone number as spam in the client file:

```python
if __name__ == '__main__':
    phone_number_to_report = '+918821918000'
    print("Testing Report Spam...")
    report_spam(phone_number_to_report)
```

### Search Functionality

Search by name or phone number in the client file:

```python
if __name__ == '__main__':
    print("Testing Search by Name...")
    search_by_name('Patidar')
    
    print("\nTesting Search by Phone Number...")
    search_by_phone_number('+918821918000')
```


