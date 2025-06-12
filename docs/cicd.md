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
- The production environment requires a minimal view to serve as the default page.
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

TODO:
Set repo and branch
Choose python3
Build command:
Run command:
Environment variables

## Configure GitHub Actions Builds
.github/workflows/build.yml