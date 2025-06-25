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
