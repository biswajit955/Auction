# Django Auction App

## Overview

Django Auction App is a real-time bidding application built with Django, Django Channels, and Celery. It enables users to create and bid on auctions while receiving instant notifications about bid updates.

## Features

- **Real-time Bidding**: Users can bid on auctions, and bidding updates are broadcasted in real-time to other users.
- **WebSocket Notifications**: Instant notifications for new bids and auction updates using Django Channels.
- **User Authentication**: Secure user authentication using Django's built-in authentication system.
- **Django REST Framework**: API endpoints for managing auctions, bids, and user-related actions.
- **Celery for Periodic Tasks**: Use Celery for handling periodic tasks, such as closing auctions.

## Prerequisites

- **Python 3.9**: Make sure you have Python 3.9 installed on your machine.
- **Django 4.x**: This app is built with Django 4.x. You can install it using `pip install django`.
- **PostgreSQL**: Create a PostgreSQL database and update the `DATABASES` settings in `settings.py`.
- **Redis**: Required for Celery and Django Channels. Install and configure Redis according to your system.

## Setup

### 1. Clone the Repository & Install Packages

```bash
git clone https://github.com/biswajit955/Auction.git
```

### 2. Setup Virtual Environment

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Migrate & Start Server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Additional Steps
### 4. Create Superuser
```
python manage.py createsuperuser
```
Follow the prompts to create a superuser account, which will allow you to access the Django admin panel.

### 5. Access Admin Panel
Visit http://localhost:8000/admin/ in your browser and log in using the superuser credentials.

### 7. Explore Frontend
Navigate to http://localhost:8000/ in your browser to explore the frontend of the E-commerce site.


## Customization
Update settings.py with your specific configuration details.
Customize frontend templates and styles in the templates and static directories.

## Contribute
If you would like to contribute to this project, please follow the Contribution Guidelines.

## Issues and Bug Reports
If you encounter any issues or find bugs, please open an issue on the Issues page.