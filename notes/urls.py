"""
URL configuration for the main app (home page).
"""

from django.urls import path
from . import views  # import ./views.py

# Unique name helps Django to identify this specific urls.py
app_name = "notes"

# define all urls for the website
urlpatterns = [
    # Home page
    # Add "" to the route to match the default (root) path "/"
    # views.index: the function (route) Django will call in views.py when it
    #   matches this route
    # name="index": a name/alias for this route (useful for reverse lookups)
    path("", views.index, name="index"),
    # Any additional pages available for this app...
    # Show Topics list
    path("topics/", views.topics, name="topics"),
    # Show Topic details by its id (e.g. http://<app_name>/topics/1/)
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    ##
    # Create routes
    #
    # Create a new topic
    path("new_topic/", views.new_topic, name="new_topic"),
    # Create a new topic entry
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    ##
    # Update routes
    #
    # Update a topic
    path("edit_topic/<int:topic_id>/", views.edit_topic, name="edit_topic"),
    # Update an entry
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
    ##
    # Delete routes
    #
    # Delete a topic (GET shows confirm page, POST performs delete)
    path("delete_topic/<int:topic_id>/", views.delete_topic, name="delete_topic"),
    # Delete an entry (GET shows confirm page, POST performs delete)
    path("delete_entry/<int:entry_id>/", views.delete_entry, name="delete_entry"),
]
