from django.shortcuts import render


def index(request):
    """Routine Saga Home page"""
    # Render and return the 'index.html' template for the Routine Saga app
    return render(request, "notes/index.html")
