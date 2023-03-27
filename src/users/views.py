from django.conf import settings
from django.http import QueryDict
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.utils.html import escape
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
from datetime import datetime, timedelta

from users.models import Profile, UserSettings, User, PasswordToken
from users.utils import email_user

from household.models import HouseHold



# Create your views here.
#class UsersViewUsers(LoginRequiredMixin,View):
class UsersViewUsers(View):
    def get(self, request):
        household = request.user.household
        users = list(User.objects.values('id', 'email', 'is_staff','first_name').get(household=household))
        
        context = { 
            'users': users,
            'action': {
                'name': 'User',
                'view_url': 'users:user_view',
                'edit_url': 'users:user_edit',
                'delete_url': 'users:user_delete',
                'create_url': 'users:user_create',
                'invite_url': 'users:user_invite',
            }
        }
        return render(request, 'users/users.html', context)

class UsersViewUser(LoginRequiredMixin,View):
    def get(self, request, pk):
        try:
            household_id = request.user.household
            user = User.objects.values('id','username', 'email', 'is_staff','first_name','last_name','is_active').get(id=pk,household=household_id)
        
        except:
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        context = {
            'page': 'view',
            'edit_user': user,
            'next': 'users:users'
        }
        return render(request, 'users/edit-user.html', context)

class UsersEditUser(LoginRequiredMixin,View):

    def get(self,request, pk):        
        try:
            household = request.user.household
            user = User.objects.values('id','username', 'email', 'is_staff','first_name','last_name', 'is_active').get(id=pk,household=household)
               
        except Exception as err:
            print(err)
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        context = {
            'page': 'edit',
            'edit_user': user,
            'next': 'users:users'
        }
        return render(request, 'users/edit-user.html', context)

    def post(self, request, pk):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        is_admin=request.POST.get('is_admin') 
        is_admin = True if is_admin else False
        is_active=request.POST.get('is_active') 
        is_active = True if is_active else False
        is_household_admin=request.POST.get('is_household_admin') 
        is_household_admin = True if is_household_admin else False
        """  is_locked=request.POST.get('is_locked') 
        is_locked = True if is_locked else False """
        if first_name == "":
            messages.error(request, 'Name cannot be blank.')
            return redirect('users:users')
        try:
            household = request.user.household
            user = User.objects.get(id=pk,household=household)
        except:
            messages.error(request, 'User does not exist')
            return redirect('users:users')
            
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.is_active = is_active
        user.profile.household_admin = is_household_admin
        #user.is_locked = is_locked
        user.save()
        return redirect('users:users')

class UsersDeleteUser(LoginRequiredMixin,View) :
    def delete(self,request, pk):     
        try:
            household = request.user.household
            user = User.objects.filter(id=pk,household=household).delete()

        except:
            messages.error(request, 'User not found')
            return redirect('users:users')
        users = list(User.objects.values('id','username', 'email', 'is_staff','first_name').get(household=household))
        
        context = { 
            'users': users,
            'action': {
                'name': 'User',
                'view_url': 'users:user_view',
                'edit_url': 'users:user_edit',
                'delete_url': 'users:user_delete',
                'create_url': 'users:user_create',
                'invite_url': 'users:user_invite',
            }
        }
        return render(request, 'users/partials/list-users.html', context)
    
class UsersCreateUser(View):
    def get(self,request):
        household_id = ""
        if request.GET.get("household"):
            household_id = request.GET.get("household")
        if request.user.is_authenticated:
            next_url = 'users:users'
        else:
            next_url = 'home:index'
        context = {
           'household_id': household_id,
           'next': next_url
        }
        return render(request, 'users/create_user.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email = request.POST.get('email')
        is_staff = request.POST.get('is_admin')
        is_staff = True if is_staff else False
        is_admin = is_staff
        
        household_id = request.POST.get('household_id')
        #tmp_password = generate_password()
        uuid_str = uuid.uuid4()
        try:
            password_token = PasswordToken(first_name=first_name,last_name=last_name, email=email,is_staff=is_staff,token=uuid_str, token_life=1,household_id=household_id,is_superuser=is_staff,is_admin=is_staff)
            print(password_token)
            password_token.save()
        except Exception as err:
            messages.error(request, 'Error creating password token for new user: ' + str(err))
            return redirect('users:users')

        if password_token == None:
            messages.error(request,'Error creating password token for new user.')
            return redirect('users:users')
            
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(first_name)
        html = """\
        Congratulations, """ + first_name + """!   You're account has been created.  Add your favorite whiskeys to you database, create lists to share with friends and track prices at your favorite stores.

        Please click the link below to activate your account and create a password.

        <a href=""" + url + """ >Activate your account.</a>
        """
        response = email_user(email, html)
        print(response)
        if response['result'] == 0:
            messages.error('Error sending email: ' + str(response['message']))

        return redirect('home:index')

class UsersResetPassword(View):
    def get(request, pk):
        user = User.objects.get(id=pk)
        
        if user == None:
            messages.error('User not found')
            redirect('users:users')

        context = {
            'user': user,
           'next': 'users:users'
        }
        return render(request, 'users/reset_password.html', context)

    def post(self, request,pk):
        user = User.objects.get(id=pk)
        
        if user == None:
            messages.error('User not found')
            redirect('users:users')
        name = user.first_name
        email = user.email
        user.password_expired = True
        user.save()
            
        uuid_str = uuid.uuid4()
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(name)
        print(url)
        html = """\
        Hello, """ + name + """.   Your password has expired.

        Please click the <a href=""" + url + """>link</a>  to create a new password.
        """
        response = email_user(email, html)

        if response['result'] == 0:
            messages.error('Error sending email: ' + str(response['message']))

        return redirect('users:users')
    
class UsersCreatePassword(View):
    def get(self,request, uuid):
        password_token = PasswordToken.objects.get(token=uuid)

        if password_token == None:
            msg = 'Cannot find token.'
            #ctx = { 'uuid': uuid, 'is_admin': request.POST.get'first_name':  request.POST.get('first_name'),'last_name': request.POST.get('last_name'), 'email':  request.POST.get('email'), 'household_id': request.POST.get('household_id'), 'password': '', 'password_confirm': '','next': 'home:index', 'error': True, 'msg': msg}
            return redirect('home:index') #render(request, 'users/create_password.html', ctx)

        #See if the token has expired
        timezone = password_token.created_at.tzinfo

        token_expired_time = password_token.created_at + timedelta(hours=password_token.token_life)
        is_token_expired = True if datetime.now(timezone) > token_expired_time else False

        if is_token_expired:
            messages.error(request, "Token has expired.")
        
        first_name = request.GET.get('name')
        email = request.GET.get('email')
        

        ctx = { 'uuid': uuid, 'first_name': first_name,'last_name':password_token.last_name, 'email': email,'is_admin': password_token.is_staff, 'household_id': password_token.household_id, 'password': '', 'password_confirm': '','next': 'home:index', 'error': False, 'msg': ''}
        return render(request, 'users/create_password.html', ctx)

    def post(self, request, uuid):
        password_token = PasswordToken.objects.get(token=uuid)

        if password_token == None:
            msg = 'Cannot find token.'
            ctx = { 'uuid': uuid,'is_admin': request.POST.get('is_admin'), 'name':  request.POST.get('name'),'last_name': request.POST.get('last_name'), 'email':  request.POST.get('email'), 'household_id': request.POST.get('household_id') ,'password': '', 'password_confirm': '','next': 'home:index', 'error': True, 'msg': msg}
            return render(request, 'users/create_password.html', ctx)

        first_name = password_token.first_name
        last_name = password_token.last_name
        email = password_token.email
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        is_staff = password_token.is_admin
        is_admin = is_staff
        household_id = password_token.household_id
        password_changed = datetime.now()
            
        if password != password_confirm:
            msg = 'Passwords do not match'
            context = { 'uuid': uuid,'is_admin': is_admin, 'first_name': first_name,'last_name': last_name, 'email': email, 'password': password, 'password_confirm': password_confirm,'next': 'home:index','error': True, 'msg': msg, 'household_id': household_id }
            return render(request, 'users/create_password.html', context)

        try:
            password = make_password(password)
            household = HouseHold.objects.get(id=household_id)
            user = User(first_name=first_name,last_name=last_name, email=email,password=password,is_staff=is_staff,household=household,is_superuser=is_admin)
            #full_name = first_name + ' ' + last_name
            user.save()
            #profile = UserProfile.objects.create(user=user,name=full_name,email=email)
            #profile.save()
            #user_settings = UserSettings(ttl=1,profile=profile)
            #user_settings.save()
        except Exception as err:
            print(err)
            msg = err
            context = { 'uuid': uuid,'is_admin':is_admin, 'first_name': first_name,'last_name':last_name, 'email': email, 'password': '', 'password_confirm': '','next': 'home:index', 'error': True, 'msg': msg, 'household_id': household_id }
            return render(request, 'users/create_password.html', context)
        password_token.delete()
        return redirect('home:index')

class UsersInviteUser(LoginRequiredMixin,View):
    def get(self,request):
        context = {
           'next': 'users:users'
        }
        return render(request, 'users/invite_user.html', context)

    def post(self,request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        household_id = request.user.household.id
            
        user = list(User.objects.filter(email=email,household_id=household_id).values())

        if len(user) > 1:
            messages.error(request, 'User already exists.')
            return redirect('users:users')
        uuid_str = uuid.uuid4()
        try:
            password_token = PasswordToken(first_name=first_name,last_name=last_name, email=email,is_staff=False,token=uuid_str, token_life=1,household_id=household_id)
            print(password_token)
            password_token.save()

        except Exception as err:
            messages.error(request, 'Error creating password token for new user: ' + str(err))
            return redirect('users:users')
        if password_token == None:
            messages.error(request,'Error creating password token for new user.')
            return redirect('users:users')
            
        url = 'http://127.0.0.1:8000/users/create-password/' + str(uuid_str) + '?email=' + escape(email) + '&name=' + escape(name)+ '&last_name=' + escape(last_name)
        html = """\
        Congratulations, """ + name + """!   You've been invited to join the Whiskey List!  Add your favorite whiskeys to you database, create lists to share with friends and track prices at your favorite stores.

        Please click the link below to activate your account and create a password.

        <a href=""" + url + """ >Activate your account.</a>
        """
        response = email_user(email, html)

        if response['result'] == 0:
            messages.error('Error sending email: ' + str(response['message']))
            
        return redirect('users:users')

""" class ProfileViewProfile(LoginRequiredMixin,View):
    def get(self,request, pk):
        
        user = User.objects.get(id=pk)
        profile = user.userprofile
        user_settings = profile.usersettings
        
        context = { 'user_settings': user_settings   }

        return render(request, 'users/profile.html', context)

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        profile = user.userprofile
        user_settings = profile.usersettings
        
        data = QueryDict(request.body).dict()
        user_settings.ttl = data['ttl']
        user_settings.save()
        context = { 'user_settings': user_settings,
                        'msg': 'Saved.'
        }
        return render(request, 'users/partials/save-success.html', context)

         """