from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Urgency(models.Model):
    URGENCY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    choice = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES,
        default="medium",
    )

    def __str__(self):
        return self.get_choice_display()

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    marked_done = models.BooleanField()
    date = models.DateField()
    slug = models.SlugField(unique=True, db_index=True)
    urgency = models.ForeignKey(Urgency, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 2

        while Todo.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return not self.marked_done and self.date < timezone.localdate()
    
    def __str__(self):
        return self.title
    

