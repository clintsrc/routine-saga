# Python Project Environment Setup (with pyenv and venv)

## NOTE
* Issue: runtime errors
* Soln: When you add/rename functions, classes, or files (especially views.py or
forms.py) be sure to restart the server and test it again before going deeper

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
$ django-admin startproject config .   # the dot makes it readily deployable
```

- 'config' is the django 'core' backend (similar to a javascript node server)
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
   - Add the app to the INSTALLED_APPS list (see config/settings.py)

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
# if the server is running shut it down
$ cd <project_root>
$ python manage.py makemigrations <app_name>
# Apply the changes to the database
$ python manage.py migrate
```

### 5. Setup an Admin site and Superuser

1. Create a superuser:

```bash
# if the server is running shut it down
$ cd <project_root>
$ python manage.py createsuperuser
# input a username and pssword (the email can be empty)

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
  <a href="{% url '<app_name>:index' %}">App Name</a> -
  <a href="{% url '<app_name>:topics' %}">Topics</a>
</p>

<!-- The child template will define what is rendered here as needed -->
{% block content %} {% endblock content %}
```

#### Update the index.html to use the base template

(Update: <app_name>/templates/<app_name>/index.html)

```html
<!-- 'extends' the parent template it inherits from //-->
{% extends '<app_name
  >/base.html' %}

  <!-- Specify the content block //-->
  {% block content %}
  <p>App description</p>
  {% endblock content %}</app_name
>
```

#### An example 'topics' page

(Update: <app_name>/templates/<app_name>/topics.html)

```html
<!-- 'extends' the parent template it inherits from //-->
{% extends '<app_name>/base.html' %}

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

## Create an entry form
### Create a form for a model: <app_name>/forms.py
```python
from django import forms

from .models import Topic

# Inherit ModelForm base form from Django
class TopicForm(forms.ModelForm):
    class Meta:  # describes which form and fields to inherit
        model = Topic   # use our Topic model
        fields = ['text']   # Include the text field
        labels = {'text': ''}   # Do not generate a label for the text field
```
### Add and endpoint for the new Topics page
(Update: <app_name>/urls.py)
```python
urlpatterns = [
    ...
    # Create a new topic
    path("new_topic/", views.new_topic, name="new_topic"),
]
```
### Add add a new Topics view
(Update: <app_name>/views.py)
```python
# Import redirect to forward from new_topic to the topic page on submit
from django.shortcuts import render, redirect
from .forms import TopicForm  # Import the new submission form
...
##
# Create using POST routes
#
def new_topic(request):
    # Request is initially a GET for the form page itself
    """Create a new Topic"""
    if request.method != "POST":
        # Load a blank form (no TopicForm arguments)
        form = TopicForm()
    else:
        # POST request on form submit
        # Pass the TopicForm request.POST user input
        form = TopicForm(data=request.POST)
        # Process the input. is_valid() checks for:
        #   required fields (default is all)
        #   models.py constraints (e.g. type, character limit)
        if form.is_valid():
            form.save() # write to the database
            return redirect("<app_name>:topics") # forward to view the Topics page

    # Show the initial input form, or handle invalid input indicators
    context = {"form": form}
    # Store the form in the context dictionary to pass it along to the template
    return render(request, "<app_name>/new_topic.html", context)
```
### Add add a New Topics template
Create a template: <app_name>/templates/<app_name>/new_topic.html
```html
<!-- 'extends' the parent template it inherits from //-->
{% extends "<app_name>/base.html" %} {% block content %}
<p>Add a new topic:</p>
<!--
  Create the form:
  action: send the form data to the new_topic() view function
  method: submit the data as a POST
//-->
<form action="{% url '<app_name>:new_topic' %}" method="post">
  <!-- csrf_token: prevent cross-site forgery attacks //-->
  {% csrf_token %}
  <!-- Django can automatically handle displaying the fields as div entries //-->
  {{form.as_div}}
  <!-- the form submit button //-->
  <button name="submit">Add</button>
</form>
{% endblock content%}
```
### Add a link for the New Topics form
(Update: <app_name>/templates/<app_name>/topics.html)
```html
...
</ul>
<a href="{% url '<app_name>:new_topic' %}">Add a new topic</a>
{% endblock content %}
```
## Add support for entry Updates
### Add and endpoint for the edit Entry page
(Update: <app_name>/urls.py)
```python
# define all urls for the website
urlpatterns = [
    ...
    # Update an entry
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
]
```

### Add add an edit Entry view
(Update: <app_name>/views.py)
```python
##
# Update routes
#
def edit_entry(request, entry_id):
    """Edit an existing Entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != "POST":
        # Load a blank form (no arguments)
        # Populate the form with data for the existing entry
        form = EntryForm(instance=entry)
    else:
        # POST request on form submit
        # Pass the preexisting info modified by the new input data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # Entry is already associated with the correct topic
            form.save()  # write to the database
            # Specify the view for the redirect target and topic_id
            #   argument
            topic_id = topic.id
            return redirect(
                "<app_name>:topic", topic_id=topic_id
            )  # forward to view the Entry page
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "<app_name>/edit_entry.html", context)
```

### Add add an edit Entry template
Create a template: <app_name>/templates/<app_name>/edit_entry.html
```html
<!-- 'extends' the parent template it inherits from //-->
{% extends "<app_name>/base.html" %} {% block content %}
<!-- Show the topic and link back to main page //-->
<p><a href="{% url '<app_name>:topic' topic.id %}">{{topic}}</a></p>
<p>Add a new entry:</p>
<!--
  Create the form:
  action: send the form data to the new_entry() view function and the
    associated topic id
  method: submit the data as a POST
//-->
<form action="{% url '<app_name>:new_entry' topic.id %}" method="post">
  <!-- csrf_token: prevent cross-site forgery attacks //-->
  {% csrf_token %}
  <!-- Django can automatically handle displaying the fields as div entries //-->
  {{form.as_div}}
  <!-- the form submit button //-->
  <button name="submit">Add</button>
</form>
{% endblock content%}
```


### Add the edit entry link in the Topic page:
(Update): <app_name>/templates/<app_name>/topic.html
```html
...
  <!-- Django uses the | operator to format the data field output //-->
  <li>
    <p>{{entry.date_added|date:'M d, Y H:i'}}</p>
    <!-- linebreaks will handle the necessary html <br> breaks //-->
    <p>{{entry.text|linebreaks}}</p>
    <p><a href="{% url 'notes:edit_entry' entry.id %}">Edit entry</a></p>
  </li>
...
```