from django import forms

from .models import Topic, Entry


# Inherit ModelForm base form from Django
class TopicForm(forms.ModelForm):
    class Meta:  # describes which form and fields to inherit
        model = Topic  # use our Topic model
        fields = ["text"]  # Include the text field
        labels = {"text": ""}  # Do not generate a label for the text field

# Reuse ModelForm for Topic Entries
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text": ""}
        """
        Override the Django default textarea widget to increase the default
        40-char column width for a more lengthy note
        """
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
