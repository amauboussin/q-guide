import os
DEBUG = True

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'qdata',        # Or path to database file if using sqlite3.
        'USER': 'qdata',        # Not used with sqlite3.
        'PASSWORD': 'password', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}