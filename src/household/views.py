from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from uuid import uuid4

from .models import HouseHold


# Create your views here.
#class HouseholdViewHousehold(LoginRequiredMixin, View):
class HouseholdViewHousehold( View):
    def get(self, request,pk):
        context = {}
        return render(request, 'household/household.html', context)
    
class HouseholdCreateHousehold(View):
    def get(self,request):
        context = { 'next': 'home:index'}

        return render(request, 'household/register_household.html', context)
    
    def post(self, request):
        name = ""
        # Validate form
        if request.POST.get('name'):
            name = request.POST.get('name')
        # Save Household
        household = HouseHold.objects.create(name=name)
        #household.save()
        # Redirect to create a user
        
        context = {}
        return redirect(reverse('users:user_create') + '?household=' + str(household.id))
        #return redirect(reverse('users:user_create'))