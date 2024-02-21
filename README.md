# Django ChatAPP
You can take advantage of the chatapp project I made according to your wishes.

## Description
The purpose of my project is that users can chat with their friends online.
<br>
Users can create their own accounts, add friends and chat with them online. People can add each other by username. In chat, users can share photos, videos, audio and more files with each other.
<br>
I used the Django framework of the python programming language in the backend of the project. I used Django channels for asynchronous messaging.
<br>
I used javascript on frontend and jquery for connection with backend.
<br>

## Installation

```bash
git clone https://github.com/ibrahimmuradov/django_chatapp.git .
pip install -r requirements.txt
django-admin startproject core . 
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```
