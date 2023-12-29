# emodjis

Emojis is a work inspired from [custom-emoji-server](https://github.com/dsmiller95/custom-emoji-server/blob/master/src/emoticons.ts) with the objective of using our Slack emoticons into Teams.
The backend is only a part of the project and more is going on to use the service in Teams on the frontend side.

## Dependencies

- [Django](https://www.djangoproject.com/) for fast app development
- [Django Rest Framework](https://www.django-rest-framework.org) for APIs
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html) for API documentation

## Install

pip install emodjis

## Configure for development

### settings.py

Add the following values to INSTALLED_APPS

```
[
  "rest_framework",
  "django_filters",
  "drf_spectacular",
  "corsheaders",
  "emodjis",
]
```

Set SPECTACULAR_SETTINGS and REST_FRAMEWORK in your settings.

### environment variables

Set the following environment variables (you can use a .env file)
```
SERVER_URL=http://127.0.0.1:8000
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8000
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=emojis.sqlite3
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_PORT=
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
```

# Configure for production

Add `emodjis` to your INSTALLED_APPS migrate and collect static files.
