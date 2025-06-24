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
{% extends '<app_name>/base.html' %}

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

{% endblock content %}
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
  <a href="{% url 'notes:index' %}">Routine Notes</a> -
  <a href="{% url 'notes:topics' %}">Topics</a>
  {% if user.is_authenticated %}
  <p>{{user.username}}</p>
  {% else %}
  <a href="{% url 'accounts:login' %}">Login</a>
  {% endif %}
</p>

<!-- The child template will define what is rendered here as needed -->
{% block content %} {% endblock content %}

```
### Test it out
   1. First log out of your admin account: http://localhost:8000/admin
   1. Login as a user: http://localhost:8000/accounts/login

## Setup a Log out page (the form uses POST)
### Update the base template to show the login on every page: <app_name>/templates/<app_name>/base.html

```html
...
{% block content %} {% endblock content %}
  {% if user.is_authenticated %}
  <hr/>
  <form action="{% url 'accounts:logout' %}" method="post">
  {% csrf_token %}
  <!-- View sends a form object to the to the template to be displayed -->
  {{form.as_div}}
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
   1. Click the Log out button
   2. You should be redirected to the Home page

## Setup New User Registration
