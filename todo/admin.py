from django.contrib import admin
from .models import Todo, Urgency

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "user", "urgency",)
    list_filter = ("user", "urgency", "marked_done",)

admin.site.register(Todo, TodoAdmin)
admin.site.register(Urgency)
