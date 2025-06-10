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
$ source .venv/bin/activate   # run it
$ deactivate   # to exit
```

### 3. Setup the latest pip

```bash
$ python -m pip install --upgrade pip
```

### 4. Install (and record) the package dependencies

```bash
$ python -m pip install django && pip freeze > requirements.txt
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
$ python manage.py migrate   # create the database
$ python manage.py runserver   # test it in a browser: http://localhost:
[Ctrl+C to exit]
```

### 3. Create main app

- Django projects have multiple apps (e.g. one does most of the work, another might
  be user management, etc.)

```bash
$ python manage.py runserver   # if it's not already running
# Open another terminal in the same path (project root)
# Start the venv environment for that terminal
$ python manage.py startapp notes   # create the main app
```

- 'notes' is for the app logic (routes, controllers, db models)
