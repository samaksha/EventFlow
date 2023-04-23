# Event Flow

This Django backend provides an authentication and API integration with Google Calendar to allow users to log in and view all the events in their Google Calendar. It uses the Google Calendar API and OAuth2 for authentication and authorization.

## Features

- Google OAuth2 authentication for user login
- Fetches and displays all events from the user's Google Calendar
- Handles token storage and refresh for authenticated requests
- Supports Django 3.x and Python 3.x

## Requirements

- Python 3.x
- Django 3.x
- Google API credentials file (JSON format) for OAuth2 authentication

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/google-calendar-backend.git
```
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Add your Google API credentials file to the project directory and update the GOOGLE_CREDENTIALS_FILE setting in settings.py with the path to your credentials file:
python
```bash
GOOGLE_CREDENTIALS_FILE = 'client_secret.json'
```
4. Set up Django database and run migrations:
```bash
python manage.py migrate
```
5. Start the Django development server:
```bash
python manage.py runserver
```
6. Access the backend at http://localhost:8000/ in your web browser.
