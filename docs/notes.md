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
```

Start the server:

```bash
$ python manage.py runserver [optional_port_number]
# test it in a browser: http://localhost:8000
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

1. Apply the changes to the database (run these commands whenever you make changes to
   the model)

```bash
# generate translate the data model to a 'sql script' (0001_initial.py)
$ python manage.py makemigrations <app_name>
# Apply the changes to the database
$ python manage.py migrate
```

### 5. Setup an Admin site and Superuser

1. Create a superuser:

```bash
   python manage.py createsuperuser

```

1. Register a model with the admin site. Update <app_name>/admin.py:

```python
...
from .models import Topic

admin.site.register(<model_name>)
```

1. Navigate to http://localhost:8000/admin
1. Try creating a new topic

## Django Shell (especially for testing and debugging)

- ref: https://docs.djangoproject.com/en/4.1/topics/db/queries

1. Start the Django CLI:

```bash
   python manage.py shell
```

2. Open a model

```bash
>> from <app_name>.models import <Model_name>
>> <Model_name>.objects.all()
```

3. Run queries:

```bash
# Loop over a queryset, eg:
>> topics = Topic.objects.all()
>> for topic in topics:
      print(topic.id, topic)
```

```bash
# Access data by id, eg:
>> t = Topic.objects.get(id=1)
>> t.text
>> t.date_added
# Get data via foreign key with _set
>> t.entry_set.all()
>> quit()
```

## Django Webpage Anatomy

1. Define the URL in urls.py (similar to a React route)
1. Write the View in views.py (similar to a React component)
1. Write the template (base html layout)

### URL (urls.py):

```python
from django.contrib import admin
from django.urls import path, include

# define all urls for the website
urlpatterns = [
    # all urls specifically available for the admin site
    path("admin/", admin.site.urls),
    # all urls specifically available for the main app site
    path("", include("<app_name>.urls")),
]
```

### Create <app_name>/urls.py

```python
Define URLs for the app itself
"""
URL configuration for the main app (home page).
"""

from django.urls import path, include
from . import views  # import ./views.py

# Unique name helps Django to identify this specific urls.py
app_name = "<app_name>"

# define all urls for the website
urlpatterns = [
    # Home page
    # Add "" to the route to match the default (root) path "/"
    # views.index: the function Django will call in views.py when this route is matched
    # name="index": a name/alias for this route (useful for reverse lookups)
    path("", views.index, name="index"),
    # Any additional pages available for this app...
]
```

### Add a view to <app_name>/views.py

```python
from django.shortcuts import render


def index(request):
    """Routine Saga Home page"""
    # Render and return the 'index.html' template for the Routine Saga app
    return render(request, "<app_name>/index.html")
```

### Create a template: <app_name>/templates/<app_name>/index.html
```html
<p>Home Page</p>

<p>Welcome to the site!</p>
```

Start the server and test it out:
```bash
$ python manage.py runserver
Then open: http://localhost:8000
```
### Inherited Templates
#### Create a base template: <app_name>/templates/<app_name>/base.html
```html
<!-- use a template tag: {'% %'} //-->

<!-- Create a link using the index alias in the urls.py file -->
<p>
  <a href="{% url 'notes:index' %}">App Name</a> -
  <a href="{% url 'notes:topics' %}">Topics</a>
</p>

<!-- The child template will define what is rendered here as needed -->
{% block content %} {% endblock content %}
```
#### Update the index.html to use the base template
(Update: <app_name>/templates/<app_name>/index.html)
```html
<!-- 'extends' the parent template it inherits from //-->
{% extends '<app_name>/base.html' %}

<!-- Specify the content block //-->
{% block content %}
<p>App description</p>
{% endblock content %}
```
#### An example 'topics' page
(Update: <app_name>/templates/<app_name>/topics.html)
```html
<!-- 'extends' the parent template it inherits from //-->
{% extends 'notes/base.html' %}

<!-- Specify the content block //-->
{% block content %}
<p>Topics</p>
<!-- Use a for loop to populate an unordered list from the context dictionary
    which contains the topics queried from the database //-->
<ul>
  {% for topic in topics %}
  <!-- Double brace for variable interplation //-->
  <li>{{topic.text}}</li>
  <!-- Handle and empty query result //-->
  {% empty %}
  <li>No topics have been added yet.</li>
  {% endfor %}
</ul>
{% endblock content %}
```
#### Add the url pattern to match the topics page:
(Update: <app_name>/urls.py)
```python
...
urlpatterns = [
    ...
    path("", views.index, name="index"),
    # Any additional pages available for this app...
    path("topics/", views.topics, name="topics"),
]
```
#### Add the topic page view:
(Update: <app_name>/views.py)
```python
...
from .models import Topic

def topics(request):
    """Routine Saga Topics page"""
    # query the database for the Topics, sort by date
    topics = Topic.objects.order_by("date_added")
    # define the context (here a dictionary)
    context = {"topics": topics}
    return render(request, "<app_name>/topics.html", context)
```