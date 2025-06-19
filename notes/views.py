from django.shortcuts import render
from .models import Topic  # Ensure your models.py defines a class named 'Topic'


def index(request):
    """Home page"""
    # Render and return the 'index.html' template for the app
    return render(request, "notes/index.html")


def topics(request):
    """Topics page"""
    # query the database for the Topics, sort by date
    # pylint: disable=no-member
    topics = Topic.objects.order_by("date_added")
    # define the context (here a dictionary)
    context = {"topics": topics}
    return render(request, "notes/topics.html", context)


def topic(request, topic_id):
    """Show single topic list the entries"""
    # query the database for the Topics, sort by date
    # pylint: disable=no-member
    topic = Topic.objects.get(id=topic_id)
    # desc order (newest first)
    entries = topic.entry_set.order_by("-date_added")
    # store query results in a dictionary
    context = {"topic": topic, "entries": entries}
    # fill the template with context data
    return render(request, "notes/topic.html", context)
