from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View, DeleteView
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TodoListView(LoginRequiredMixin, ListView):
    template_name = "todo/all-todos.html"
    model = Todo
    context_object_name = "all_todos"
    ordering = ["date"]

    def get_queryset(self):
        queryset =  super().get_queryset()

        user = self.request.user
        queryset = queryset.filter(user=user)

        urgency = self.request.GET.get('urgency')
        marked_done = self.request.GET.get('marked_done')
        is_overdue = self.request.GET.get('is_overdue')

        if urgency:
            queryset = queryset.filter(urgency__choice=urgency)
        if marked_done == "true":
            queryset = queryset.filter(marked_done=True)
        elif marked_done == "false":
            queryset = queryset.filter(marked_done=False)
        if is_overdue == "true":
            queryset = queryset.filter(marked_done=False, date__lt=timezone.localdate())
        return queryset

class TodoEditView(LoginRequiredMixin, View):
    template_name = "todo/todo-detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.todo = get_object_or_404(Todo, slug=kwargs["slug"], user=request.user)
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, slug):
        context = {
            "todo": self.todo,
            "todo_form": TodoForm(instance=self.todo)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        todo_form = TodoForm(request.POST, instance=self.todo)

        if todo_form.is_valid():
            todo_form.save()

        return HttpResponseRedirect(reverse("todo-list"))

class TodoFormView(LoginRequiredMixin, View):
    template_name = "todo/todo-form.html"

    def get(self, request):
        context = {
            "todo_form": TodoForm()
        }

        return render(request, self.template_name, context)
    
    def post(self, request):
        todo_form = TodoForm(request.POST)

        if todo_form.is_valid():
            todo = todo_form.save(commit=False)
            todo.user = request.user
            todo.save()
            return HttpResponseRedirect(reverse("todo-list"))
        
class MarkDoneView(LoginRequiredMixin, View):
    def post(self, request, slug):
        todo = get_object_or_404(Todo, slug=slug, user=request.user)
        todo.marked_done = True
        todo.save()

        return HttpResponseRedirect(reverse("todo-list"))
    
class DeleteTodoView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        queryset = queryset.filter(user=user)
        return queryset