from django.shortcuts import render
from .models import Topic  # Ensure your models.py defines a class named 'Topic'


def index(request):
    """Routine Saga Home page"""
    # Render and return the 'index.html' template for the Routine Saga app
    return render(request, "notes/index.html")


def topics(request):
    """Routine Saga Topics page"""
    # query the database for the Topics, sort by date
    # pylint: disable=no-member
    topics = Topic.objects.order_by("date_added")
    # define the context (here a dictionary)
    context = {"topics": topics}
    return render(request, "notes/topics.html", context)
