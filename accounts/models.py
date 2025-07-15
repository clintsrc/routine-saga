import binascii
import os
from django.db import models
from django.contrib.auth.models import User


# Model stores a unique token for each user to handle API authentication
# NOTE: revisit later to use JWT instead ofa a simple token
class Token(models.Model):
    """
    Generates an authentication token linked to a single user.
    The token is used for API request authententication
    """

    # The token string
    key = models.CharField(max_length=40, primary_key=True)
    # One token per user. When a user is deleted this will also
    # (cascade) delete their token
    user = models.OneToOneField(
        User, related_name="auth_token", on_delete=models.CASCADE
    )
    # When a user is created, automatically add a timestamp
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override save() to automatically generate a token key if it doesn't exist
        """
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    # Return a binary encoded token
    def generate_key(self):
        """
        Generate a binary token, encode it as a hex string
        """
        return binascii.hexlify(os.urandom(20)).decode()
