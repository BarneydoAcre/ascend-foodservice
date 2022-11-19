# CloudSys

## Build Setup

```bash
# install dependencies
$ pip install django
$ pip install django-cors-headers
$ pip install djoser
$ pip install psycopg2-binary (if linux)
$ pip install reportlab

$ INSTALED_APPS = [
$    ...
$    'corsheaders',
$    'rest_framework',
$    'rest_framework.authtoken',
$    'rest_framework_simplejwt.token_blacklist',
$    'djoser',
$    ...
$ ]

$ MIDDLEWARE = [
$    ...
$    "corsheaders.middleware.CorsMiddleware",
$    ...
$ ]

$ DATABASES = {
$    'default': {
$        'ENGINE': 'django.db.backends.postgresql_psycopg2',
$        'NAME': 'foodservice',
$        'USER': 'postgres',
$        'PASSWORD': 'postgres',
$        'HOST': 'localhost',
$        'PORT': '5432',
$    }
$ }

$ LANGUAGE_CODE = 'pt-br'
$ TIME_ZONE = 'America/Manaus'

$ REST_FRAMEWORK = {
$    'DEFAULT_AUTHENTICATION_CLASSES': (
$        'rest_framework_simplejwt.authentication.JWTAuthentication',
$    ),
$ }
$ SIMPLE_JWT = {
$   'AUTH_HEADER_TYPES': ('JWT',),
$ }

# serve with hot reload at localhost:8000
$ py manage.py runserver

# build for production and launch server
$ py manage.py 0.0.0.0:80

# configuration for HTTP STATUS
403 - NOT A POST
402 - TOKEN INVALID
401 - INTERNAL ERROR
200 - OK
```

