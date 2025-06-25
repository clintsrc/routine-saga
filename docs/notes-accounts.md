# Setup User Account Login and Registraton

## Reminder: to start the virtual environment

```bash
# nonwindows use:
$ source .venv/bin/activate
# windows use:
$ source .venv/Scripts/activate
$ deactivate # to exit

# Start the server:
$ python manage.py runserver [optional_port_number]
# test it in a browser: http://localhost:8000
# [Ctrl+C to exit]
```

## Setup User Accounts

### Create an accounts app

```bash
$ cd <project_root>
$ python manage.py startapp accounts
```

### Add account to INSTALLED_APPS

(in core/settings.py)

```python
INSTALLED_APPS = [
    # user apps
    "<app_name>",
    "accounts",
    # core apps
```

### Add urls to be defined for the accounts app

(Update: core/urls.py)

```python
# define all urls for the website
urlpatterns = [
    # all urls specifically available for the admin site
    path("admin/", admin.site.urls),
    # all urls specifically available for the accounts app site
    path("accounts", include("accounts.urls")),
    # all urls specifically available for the main app site
    path("", include("<app_name>.urls")),
]
```

## Setup a Login page

Create: accounts/urls.py

```python
"""
URL configuration for the accounts app (login page).
"""

from django.urls import path, include

# Unique name helps Django to identify this specific urls.py
app_name = "accounts"

# define all urls for the admin website
urlpatterns = [
    # Login page
    # Add "" to the route to match the default (root url) path "/"
    # django urls provide 'accounts/login' and 'accounts/logout' urls
    path("", include('django.contrib.auth.urls')),
    # Any additional pages available for this app...
]
```

### Create a login Template page

Create: accounts/templates/registration/login.html

```html
<!-- Make the UI will have the same look and feel -->
{% extends '<app_name
  >/base.html' %}

  <!-- Show an error if the form.errors attribute is set -->
  {% block content %} {% if form.errors %}
  <p>Your username and password do not match</p>
  {% endif %}

  <!-- Process the form with the login view -->
  <form action="{% url 'accounts:login' %}" method="post">
    {% csrf_token %}
    <!-- View sends a form object to the to the template to be displayed -->
    {{form.as_div}}
    <button name="submit">Login</button>
  </form>

  {% endblock content %}</app_name
>
```

### Redirect a successful login

(Update core/settings.py -- add to the end of the file:)

```python
# user settings
LOGIN_REDIRECT_URL = '<app_name>:index'
```

### Update the base template to show the login on every page: <app_name>/templates/<app_name>/base.html

```html
<!-- use a template tag: {'% %'} //-->

<!-- Create a link using the index alias in the urls.py file -->
<p>
  <a href="{% url 'notes:index' %}">Routine Notes</a>
   - <a href="{% url 'notes:topics' %}">Topics</a>
  {% if user.is_authenticated %}
  <p>{{user.username}}</p>
  {% else %}
   - <a href="{% url 'accounts:login' %}">Login</a>
  {% endif %}
</p>

<!-- The child template will define what is rendered here as needed -->
{% block content %} {% endblock content %}

```

### Test it out

1.  First log out of your admin account: http://localhost:8000/admin
1.  Login as a user: http://localhost:8000/accounts/login

## Setup a Log out page (the form uses POST)

### Update the base template to show the login on every page: <app_name>/templates/<app_name>/base.html

```html
... {% block content %} {% endblock content %} {% if user.is_authenticated %}
<hr />
<form action="{% url 'accounts:logout' %}" method="post">
  {% csrf_token %} {% csrf_token %}
  <!-- Log out post doesn't need (shouldn't have) a form -->
  <button name="submit">Log out</button>
</form>
{% endif %}
```

### Add a redirect for the logout

(Update core/settings.py -- add to the end of the file:)

```python
# user settings
LOGIN_REDIRECT_URL = '<app_name>:index'
LOGOUT_REDIRECT_URL = '<app_name>:index'
```

### Test it out

1.  Click the Log out button
2.  You should be redirected to the Home page

## Setup New User Registration

### Add the registration endpoint

Update: accounts/urls.py

```python
...
urlpatterns = [
    ...
    # User Registration
    path("register/", views.register, name='register'),
]
```

### Add a view function

Update: accounts/views.py

```python

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Bring in the locally defined views
from . import views

def register(request):
    """New User registration"""
    if request.method != "POST":
        # Present the blank form to the user
        form = UserCreationForm()
    else:
        # Recieved contents of form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            # Save the user and encrypted password to the database
            new_user = form.save()
            # Login the new user using the credentials provided
            #   directly in the request
            login(request, new_user)
            # Forward to the home page
            return redirect("notes:index")

    # Show initial blank form or if the input is invalid
    context = {"form": form}
    return render(request, "registration/register.html", context)
```

### Create a registration Template page

Create: accounts/templates/registration/register.html

```html
<!-- Make the UI will have the same look and feel -->
{% extends 'notes/base.html' %}

<!-- Show an error if the form.errors attribute is set -->
{% block content %}<!-- Process the form with the login view -->
<form action="{% url 'accounts:register' %}" method="post">
  {% csrf_token %}
  <!-- View sends a form object to the to the template to be displayed -->
  {{form.as_div}}
  <button name="submit">Register</button>
</form>

{% endblock content %}
```

### Update the base template to show the registration link on every page (when not logged in)

(Update <app_name>/templates/<app_name>/base.html)

```html
... {% if user.is_authenticated %}
<p>{{user.username}}</p>
{% else %} - <a href="{% url 'accounts:login' %}">Login</a> -
<a href="{% url 'accounts:register' %}">Register</a>
{% endif %} ...
```

## Restrict Access

Add the @login_required decorator to the page. When an unauthenticated user tries
to access it, Django will redirect them to a URL (usually the login page) specified by
settings.py's LOGIN_URL.

Add @login_required to each view where you want to restrict access

1. Update: <app_name>/views.py

```python
...
from django.contrib.auth.decorators import login_required
...
# Decorator restricts access to authenticated users, by running
#   login_required() before topics()
@login_required
...
```

1. Update core/settings.py to redirect to the login page:

```python
# user settings
...
LOGIN_URL = 'accounts:login'
```
## Private Data
Restrict each user's data to that user
1. Update the database model: the app data needs a foreign key to relate to the user
1. Migrate the database
1. Update views to only show the data associated with the logged-in user

### Update the model
Update <app_name>/models.py:
```python
...
from django.contrib.auth.models import User
...
class Topic(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    # The owner sets a foreign key relationship to the User model
    # on_delete ensures that if a user is deleted, all the
    #   user's associated data is also removed
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
...
```
### Migrate the database
The migrate command needs to know which existing user gets the existing app data.
This associates the data to the user but it will not restrict it. That will be
addressed after the migration.
#### Viewing existing users in the database
You can view existing users from the shell. You import the auth models (same as the
import linen models.py), then calling: User.objects.all().
```bash
$ python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: app_admin>, <User: app_user>]>
>>> quit()
```
#### Migrate
Here's the shell command to perform the migration
```bash
$ python manage.py makemigrations <app_name>
[The promt indicates you must specify the data owner...]
1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
...
Select an option: 1
Please enter the default value now, as valid Python.
The datetime [...]
>>> 1
>>> quit()
```
Apply the migration:
```bash
$ python manage.py migrate
```
NOTE:
To delete the database and start fresh, you can use:
```bash
$ python manage.py flush
```
#### Restricting User Access
1. Update: <app_name>/views.py
Add the .filter(owner=request.user) member:
```python
...
    # Retrieve only the objects from the database where the owner attribute
    #   matches the current user.
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
...
```
1. Test it by logging in as the user with access to view the data, and as another
user that doesn't own it
