# Python Project Environment Setup (with pyenv and venv)

## Setup the environment

### 1. Set the Python Version (with pyenv)

```bash
$ pyenv versions
$ pyenv local <version>
$ python -m venv .venv
```

### 2. Setup the virtual environment

```bash
$ python -m venv .venv
# run it:
# nonwindows use:
$ source .venv/bin/activate
# windows use:
$ source .venv/Scripts/activate
$ deactivate   # to exit
```

### 3. Setup the latest pip

```bash
$ python -m pip install --upgrade pip
```

### 4. Install (and record) the package dependencies

```bash
$ python -m pip install django && pip freeze > requirements.txt
# NOTE: to import an existing requirements.txt
$ pip install -r requirements.txt
```

## Setup Django project

### 1. Generate the project files ()

```bash
$ django-admin startproject core .   # the dot makes it readily deployable
```

- 'core' (or 'config', another standard naming convention) is the django
  backend (similar to a javascript node server)
- manage.py: forwards commands to the relevant part of django
- settings.py: interacts with your system and manages the project
- urls.py: tells django which files to build in response to browser requests
- wsgi.py (web server gateway interface): helps django serve the files it creates

### 2. Create the SQLite database

```bash
# create the database
$ python manage.py migrate
# test it in a browser: http://localhost:8000
$ python manage.py runserver [optional_port_number]
# [Ctrl+C to exit]
```

### 3. Create main app (i.e. notes)

- Django projects have multiple apps (e.g. one does most of the work, another might
  be user management, etc.)
- In javascript terms an app module has the component, the routes and the database model

```bash
$ python manage.py startapp <app_name>   # create the main app module
```

### 4. Setup the data model

1. Define the data model
   - See the notes/models.py
   - ref: https://docs.djangoproject.com/en/4.1/ref/models/fields
1. Hook the data model up to the project
   - Add the app to the INSTALLED_APPS list (see core/settings.py)
```python
INSTALLED_APPS = [
    # user apps
    "notes",
    ...
```
1. Apply the changes to the database
```bash
# generate translate the data model to a 'sql script' (0001_initial.py)
$ python manage.py makemigrations <app_name>
# Apply the changes to the database
$ python manage.py migrate
```

### 5. Setup an Admin site and Superuser
