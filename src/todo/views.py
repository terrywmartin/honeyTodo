from django.shortcuts import render

from django.views import View

# Create your views here.
class TodoViewTodos(View):
    def get(self, request):
        context = {}

        return render(request, 'todo/todos.html', context=context)