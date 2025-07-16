from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def register_user(username: str, password1: str, password2: str) -> User:
    """
    Register a new user with username and matching passwords

    Args:
        username (str)
        password1 (str): password
        password2 (str): confirm password

    Raises:
        ValidationError: missing input, password mismatch,
                         or username in exists

    Returns:
        User: The newly created usewr instance
    """
    if not username or not password1 or not password2:
        raise ValidationError("All fields are required.")
    if password1 != password2:
        raise ValidationError("Passwords do not match.")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists.")

    return User.objects.create_user(username=username, password=password1)
