from django.db import models


# Create your models here.
class Topic(models.Model):
    """Details about a topic"""

    text = models.CharField(max_length=200)
    # When a topic is created, automatically add a timestamp
    date_added = models.DateTimeField(auto_now_add=True)

    # Default method (__str__) is called for string output
    def __str__(self):
        """Represent the model as a string"""
        return str(self.text)


class Entry(models.Model):
    """Note entries for a topic"""

    # delete all all associeated topic entries
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    # When a topic is created, automatically add a timestamp
    date_added = models.DateTimeField(auto_now_add=True)

    # Django metaclass to help describe plural entry operations
    class Meta:
        verbose_name_plural = "entries"

    # Default method (__str__) is called for string output
    # limit it to the first 50 charadters
    def __str__(self):
        """Represent the entry model as a string"""
        display_string = str(self.text)
        if len(display_string) > 50:
            display_string = display_string[:50] + "..."
        return display_string
