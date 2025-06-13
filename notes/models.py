from django.db import models


# Create your models here.
class Topic(models.Model):
    """Details (notes) for a topic"""

    text = models.CharField(max_length=200)
    # When a topic is created, automatically add a timestamp
    date_added = models.DateTimeField(auto_now_add=True)

# Default method (__str__) is called for string output
def __str__(self):
    """Represent the model as a string"""
    return self.text
