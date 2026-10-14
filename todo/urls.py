from django.urls import path

from . import views

urlpatterns = [
    path("", views.TodoListView.as_view(), name="todo-list"),
    path("create/", views.TodoFormView.as_view(), name="create-todo"),
    path("edit/<slug:slug>", views.TodoEditView.as_view(), name="todo-detail"),
    path("mark-done/<slug:slug>/", views.MarkDoneView.as_view(), name="mark-done"),
    path("<pk>/delete/", views.DeleteTodoView.as_view(), name="delete-todo")
]
