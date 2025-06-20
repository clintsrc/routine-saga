# pylint: disable=no-member
# Import redirect to forward from new_topic to the topic page on submit
from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm  # Import the new submission form


##
# Read using GET routes
#
def index(request):
    """Home page"""
    # Render and return the 'index.html' template for the app
    return render(request, "notes/index.html")


def topics(request):
    """Topics page"""
    # query the database for the Topics, sort by date
    topics = Topic.objects.order_by("date_added")
    # define the context (here a dictionary)
    context = {"topics": topics}
    return render(request, "notes/topics.html", context)


def topic(request, topic_id):
    """Show single topic list the entries"""
    # query the database for the Topics, sort by date
    topic = Topic.objects.get(id=topic_id)
    # desc order (newest first)
    entries = topic.entry_set.order_by("-date_added")
    # store query results in a dictionary
    context = {"topic": topic, "entries": entries}
    # fill the template with context data
    return render(request, "notes/topic.html", context)


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
            form.save()  # write to the database
            return redirect("notes:topics")  # forward to view the Topics page

    # Show the initial input form, or handle invalid input indicators
    context = {"form": form}
    # Store the form in the context dictionary to pass it along to the template
    return render(request, "notes/new_topic.html", context)


def new_entry(request, topic_id):
    """Create a new Entry for a Topic"""
    # pass the topic's id number
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # Load a blank form (no arguments)
        form = EntryForm()
    else:
        # POST request on form submit
        # Pass the request.POST user input
        form = EntryForm(data=request.POST)
        # Process the input
        if form.is_valid():
            # Associate the Entry with the Topic before saving it:
            # Create new entry but don't save it yet
            new_entry = form.save(commit=False)
            # Set current topic
            new_entry.topic = topic
            # Now write to the database using the associated topic
            new_entry.save()
            # Specify the view for the redirect target and topic_id
            #   argument
            return redirect(
                "notes:topic", topic_id=topic_id
            )  # forward to view the Entry page

    # Show the initial input form, or handle invalid input indicators
    context = {"topic": topic, "form": form}
    # Store the form in the context dictionary to pass it along to the template
    return render(request, "notes/new_entry.html", context)


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
                "notes:topic", topic_id=topic_id
            )  # forward to view the Entry page
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "notes/edit_entry.html", context)
