from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ["slug", "is_overdue", "user"]
        labels = {
            "title": "Title",
            "description": "Description",
            "date": "Due Date",
            "urgency": "Urgency",
            "marked_done": "Mark as done"
        }
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date"
            }),
        }
        error_messages = {
            "title": {
                "required": "The todo title cannot be empty",
                "max_length": "Please enter a shorter title",
            },
            "description": {
                "max_length": "Please enter a shorter description",
            },
            "date": {
                "required": "You must enter a due date."
            },
            "urgency": {
                "required": "You must select an urgency option."
            }
        }