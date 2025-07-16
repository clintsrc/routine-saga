import json

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

from .utils import register_user
from .models import Token


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


@csrf_exempt  # not using session-based auth
def api_register(request: HttpRequest) -> JsonResponse:
    """
    REST API user registration

    Input is a JSON body containing 'username', 'password1', and 'password2'
    Validates input, creates a new user, generates and returns an authentication token
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Parse JSON request body for the new user info
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Register the user, otherwise report validation errors
    try:
        user = register_user(username, password1, password2)
    except ValidationError as ve:
        return JsonResponse({"error": str(ve)}, status=400)

    # Create token
    token, _ = Token.objects.get_or_create(user=user)

    # Return the registered user and their access token
    return JsonResponse(
        {
            "message": "User registered successfully.",
            "token": token.key,
            "username": user.username,
        },
        status=201,
    )
