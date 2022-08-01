# django-drf-crm

## Purpose.
The main idea is to create a customer relation management platform that can be used by both 
advertisers and sellers.

The API should be mostly used by the advertisers in order to create new Lead instances.

Sellers will be using regular website while operating.

## Technology used
For this project I used:
- python as the main language
- django as the main framework
- django-rest-framework for api
- pytest for testing
- css for styling

## Setup
The first thing to do is to clone the repository:
```
$ git clone https://github.com/ARROM2405/django-drf-crm.git
$ cd crm_project
```

Create virtual environment and activate it:
```
$ pip install --user pipenv
$ source env/bin/activate
```

Then install the dependencies:
```
$ pipenv install
```

Create superuser:
```
$ python manage.py createsuperuser
```

Make migrations and migrate:
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Runserver with:
```
$ python manage.py runserver
```

You should be good to go!