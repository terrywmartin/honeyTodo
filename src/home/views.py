from django.shortcuts import render, redirect

from django.views import View


# Create your views here.
class HomeIndex(View):
    def get(self, request):
        context = {}
        return render(request, 'home/index.html', context)
    
