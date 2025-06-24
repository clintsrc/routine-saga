# Production Deployment (and Dev environment)

## Setup the environment variables
### env file
- Prepare the ./.env.EXAMPLE file (e.g.):
```env
DJANGO_SECRET_KEY=password   # openssl rand -base64 50, (strip the trailing =)
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/mydb
```

### core/settings.py
- Update the core/settings.py file to read the dev env or else to use the variables set
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
Add one to the core/urls.py file:
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
## Issue: New user registration fails:
```bash
Forbidden (403)
CSRF verification failed. Request aborted.
```
## Soln: Cross-Site Request Forgery: Django blocks if CSRF is not properly configured
Add another env variable to core/settings.py:
```python
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
```
(see .env.EXAMPLE for the local dev environment)
Production:
```bash
CSRF_TRUSTED_ORIGINS = https://<app_name>.onrender.com
```


## Configure GitHub Actions Builds
.github/workflows/build.yml
TODO