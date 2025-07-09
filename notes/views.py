# pylint: disable=no-member
# Import redirect to forward from new_topic to the topic page on submit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm  # Import the new submission form


##
# Read using GET endpoints
#
def index(request: HttpRequest) -> HttpResponse:
    """Home page"""
    # Render and return the 'index.html' template for the app
    return render(request, "notes/index.html")


# Decorator restricts access to authenticated users, by running
@login_required
def topics(request: HttpRequest) -> HttpResponse:
    """Topics page"""
    # Query the database for the Topics, sort by date
    # Retrieve only the objects from the database where the owner attribute
    #   matches the current user.
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    # define the context (here a dictionary)
    context = {"topics": topics}
    return render(request, "notes/topics.html", context)


@login_required
def topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Show single topic list the entries"""
    # query the database for the Topics, sort by date
    topic = Topic.objects.get(id=topic_id)
    # Check whether the currnt user has access
    if topic.owner != request.user:
        raise Http404
    # desc order (newest first)
    entries = topic.entry_set.order_by("-date_added")
    # store query results in a dictionary
    context = {"topic": topic, "entries": entries}
    # fill the template with context data
    return render(request, "notes/topic.html", context)


##
# Create using POST endpoints
#
@login_required
def new_topic(request: HttpRequest) -> HttpResponse:
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
            # XXX before saving it:
            # Create new topic but don't save it yet
            new_topic = form.save(commit=False)
            # Change the form first: set the owner
            new_topic.owner = request.user
            new_topic.save()  # write to the database

            return redirect("notes:topics")  # forward to view the Topics page

    # Show the initial input form, or handle invalid input indicators
    context = {"form": form}
    # Store the form in the context dictionary to pass it along to the template
    return render(request, "notes/new_topic.html", context)


@login_required
def new_entry(request: HttpRequest, topic_id: int) -> HttpResponse:
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
# Update endpoints
#
@login_required
def edit_topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Edit an existing Topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Ensure the current user owns the topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # Load form pre-filled with topic data
        form = TopicForm(instance=topic)
    else:
        # Update topic with user-submitted data
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes:topics")  # Redirect to topics list

    context = {"form": form, "topic": topic}
    return render(request, "notes/edit_topic.html", context)


@login_required
def edit_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Edit an existing Entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Check whether the current user has access
    if topic.owner != request.user:
        raise Http404

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


##
# Delete endpoint
#
# Delete a topic (via form: POST for deletion)
@login_required
def delete_topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Delete an existing Topic and its entries."""
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method == "POST":
        topic.delete()
        return redirect("notes:topics")

    return render(request, "notes/delete_topic.html", {"topic": topic})


# Delete an entry (via form: POST for deletion)
@login_required
def delete_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Delete an existing entry."""
    # Return the entry or show the 404 page
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # Check whether the current user has access
    if topic.owner != request.user:
        raise Http404

    # Using a form to delete the entry, so use the POST command
    if request.method == "POST":
        entry.delete()
        return redirect("notes:topic", topic_id=topic.id)

    # If GET request, confirm deletion
    return render(request, "notes/delete_entry.html", {"entry": entry, "topic": topic})
