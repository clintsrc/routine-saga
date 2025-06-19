from django.contrib import admin
from .models import Topic  # for ./models.py
from .models import Entry

# Register your models here.
admin.site.register(Topic)  # manage Topic throught he admin site
admin.site.register(Entry)
