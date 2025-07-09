from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
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
