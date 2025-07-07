<!-- markdownlint-disable MD014 -->

# Development and Production Deployments

## I. Dev and a 'starter' Production deployment

NOTE: The Production environment uses a non-production-grade and SQLLite server: this is not the final production-quality server, just something for early infrastructure. Follow up (see section II below) for a true production deployment.

## Setup the environment variables

### env file

- Prepare the .env.EXAMPLE file (e.g.):

### config/settings.py

- Update the config/settings.py file to read the dev env or else to use the variables set
  for the production deployment

```python
from dotenv import load_dotenv
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)  # load env variables first!

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY environment variable not set!")

# SECURITY WARNING: don't run with debug turned on in
#   production! Defaults to False
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")
```

### Create a Minimal View

- The production environment requires a minimal view to serve as the default page (
  similar to a react component).
  Add one to the config/urls.py file:

```python
...
from django.http import HttpResponse


# A minimal view to verify the deployment
def home_view(request):
    return HttpResponse("Forthcoming! A Django Routine Saga app!")


urlpatterns = [
    ...
    path("", home_view),
]
```

## Render Deployment

- Configure a render deployment

1. Set the repository and branch
1. Build Command:

```bash
pip install -r requirements.txt
```

1. Start Command:
   NOTE: the checked-in migrations must be applied to the production database

```bash
python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
```

1. Set the Environment variables, e.g.:

```env
DJANGO_SECRET_KEY=<password>   # openssl rand -base64 50, (strip the trailing =)
DJANGO_ALLOWED_HOSTS=https://<app_name>.onrender.com
```

## Issue: New user registration fails

```bash
Forbidden (403)
CSRF verification failed. Request aborted.
```

## Soln: Cross-Site Request Forgery: Django blocks if CSRF is not properly configured

Add another env variable to config/settings.py:

```python
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
```

(see .env.EXAMPLE for the local dev environment)
Production:

```bash
CSRF_TRUSTED_ORIGINS = https://<app_name>.onrender.com
```

## Capture Dependencies

Update the requirements file with all of the current requirements

```bash
$ pip freeze > requirements.txt
```

## Configure GitHub Actions Builds

.github/workflows/build.yml
TODO

## II. Production Deployment

For a true production deployment you need to address these areas

### Server Environment

- WGSI: This is similar to Node.js. WGSI is the core HTTP server module. Django automatically includes it with the initial project configuration.
- App server:
  - runserver: this is a local dev server built into Django (similar to React)
  - gunicorn: a production-grade server package similar to Node.js. It runs the code and manages worker processes in production. Adding gunicorn to WSGI makes it production ready.
    - It can be used in a local dev stack in docker, but you'd want to enable hot reloading (command: gunicorn myproject.wsgi:application --reload --bind 0.0.0.0:8000)
- SQL server:
  - SQLite: local dev server, not producton-grade, automatically installed by Django
  - PostgreSQL: typically used in the production environment. It may also be used in the local dev environment instead of SQLite

### Requirements files

Typically you'll want to manage multiple requirements.txt files:
requirements.txt: the base app requirements
requirements_dev.txt: additional dev tools (e.g. pettier, lint)
requirements_prod.txt: production tools (e.g. gunicorn, psycopg2)
You can add an entry in a requirements file to include another requirements file!
requirements_dev.txt -- this would import the app requirements before the dev packages:

#### Requirements for the Development environment

Requirements.txt files can include other requirements.txt files. This local.txt file includes the production (requirements.txt) package, meaning it has all production as well as dev packages.
<proj_root>/local.txt:

```bash
-r requirements.txt
black
pylint
pytest
```

### Gunicorn

NOTE: no code change is required because gunicorn communicates through the WSGI that Django provides by default.

NOTE: fcntl is required for gunicorn but it is not supported for Windows/Cygwin

#### Requirements for production environment

1. Create a <proj_root>/production.txt

```bash
-r base.txt
gunicorn
```

1. Test by installing a fresh venv for production:
   $ python -m pip install --upgrade pip
   $ pip install -r production.txt
1. Try running it locally (only on _on nonwindows hosts_):
   $ gunicorn config.wsgi:application --bind 127.0.0.1:8000
1. Update the hosting service's Start command:
   Start: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

### PostgreSQL

Use your local PostgreSQL server

#### In Development

1. Update dev environment wtih psycopg2-binary (a precompiled binary for the os)

<proj_root>/local.txt

```bash
-r production.txt
psycopg2-binary
black
pylint
pytest
```

1. Configure the .envs/.env:

``` bash
DB_NAME='routinesaga_db'
DB_USER='<user>'
DB_PASSWORD='<password>'
```

1. Update config/settings.py to read the env settings:

```python
import dj_database_url
...
#### Database info

DB_URL = os.getenv("DB_URL")
if not DB_URL:
DB_NAME = os.getenv("DB_NAME", "routinesaga_db")
DB_USER = os.getenv("DB_USER", "my_default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_default_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
...
DATABASES = {
    "default": dj_database_url.parse(DB_URL, conn_max_age=600),
}
```

1. Create a simple schema script

db/schema.sql:

```bash
-- DROP DATABASE
DROP DATABASE IF EXISTS routinesaga_db;

-- CREATE DATABASE
CREATE DATABASE routinesaga_db;
```

1. Create the database:
   psql -U postgres -f db/schema.sql

1. python manage.py migrate

1. python manage.py runserver # the dev server will use the postgres server

#### For Production

1. Create database using the <External Database URL>. Connect to default db then create the new one:

```bash
   psql "postgresql://<primary_db>:PWxxxxxxxxxxxxx@dpg-<server>-postgres.render.com/<primary_db>" -c "CREATE DATABASE routinesaga_db;"
```

3. Set the production Environment variable on the hosting site:
DB_URL='<Internal Database URL>/routinesaga_db'


#### WhiteNoies static file management

The built-in dev server (runserver) serves static files for the dev environment.

In production you're expected to use something like Nginx which also supports compression, caching, and versioned filenames. For smaller projects you can use the WhiteNoise package instead. It uses the Django WSGI middleware

```python
# wsgi.py
from whitenoise import WhiteNoise
application = WhiteNoise(application, root='staticfiles/')
```

```python
MIDDLEWARE = [
   ...
    "whitenoise.middleware.WhiteNoiseMiddleware",
   ...
]
...
# collectstatic gathers static assets for production here
STATIC_ROOT = BASE_DIR / "staticfiles"
#  Render has no CDN: WhiteNoise will collect and manage compression and caching here
#     python manage.py collectstatic --noinput
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

