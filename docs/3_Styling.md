<!-- markdownlint-disable MD014 -->

# Styling with Bootstrap

## Install and Configure Bootstrap

```bash
$ pip install django-bootstrap5
```

Add it to the list of installed apps
Update core/settings.py:

```python
...
INSTALLED_APPS = [
    # user apps
    "notes",
    "accounts",
    # 3rd party apps
    "django_bootstrap5",
    # core apps
...
```

## Bootstrap Templates

Ref: See Examples at: <https://getbootstrap.com/>

### Style the common base.html template

The idea is to:

1. Setup the semantic html (structured by using nav, main, footer, etc)
1. Add the bootstrap tags in the header: this makes the styling available for all templates that inherit from base.html with the {% load django_bootstrap5 %} tag
1. The content block is moved out to the `main` section
1. Add the styling (class="<bootstrap selector/s>")

Update <app_name>/templates/notes/base.html:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>App Name</title>
  {% load django_bootstrap5 %}
  {% bootstrap_css %}
  {% bootstrap_javascript %}
</head>
<body>
<nav>
  <!-- Existing code is here//-->
</nav>
<main class="container">
  <div >
    {% block page_header %}{% endblock page_header %}
  </div>

  <div>
    {% block content %}{% endblock content %}
  </div>
</main>
</body>
</html>
```

1. Add 'jumbotron', a large box that stands out on the main page. Add styling to
the index.html

Update <app_name>/templates/notes/index.html:

```html
<!-- 'extends' the parent template it inherits from //-->
{% extends 'notes/base.html' %}

<!-- Specify the content block //-->
{% block page_header %}
<div class="p-3 mb-4 bg-light border rounded-3">
  <div class="container-fluid py-4">
    <h1 class="display-3">Capture notes in your daily routine.</h1>
    <p class="lead">
      Routine Saga is a note-taking app for any topic you want to pursue,
      especially for major undertakings for your betterment.
    </p>
    <a class="btn btn-primary btn-lg mt-1" href="{% url 'accounts:register' %}"
      >Register &raquo;</a
    >
  </div>
</div>

<!-- Specify the content block //-->
{% endblock page_header %}
```

1. Style the remaining pages:

accounts/templates/registration/login.html (see the code)
<project_root>/templates/<app_name>/topics.html (see the code)
<project_root>/templates/<app_name>/topic.html (see the code)