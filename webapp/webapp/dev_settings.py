# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DB_DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db-pg',
        'PORT': 5432,
        'NAME': 'web_db',
        'USER': 'pttapp',
        'PASSWORD': 'pttapp'
    }
}

ALLOWED_HOSTS = ["*"]
