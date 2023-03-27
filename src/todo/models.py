from django.db import models

from uuid import uuid4

from users.models import User
from household.models import HouseHold
# Create your models here.
class Todo(models.Model):

    TASK_STATUS = (('Not Started','Not Started'),
                   ('In progress', 'In progress'),
                   ('Completed', 'Completed'))
    owner = models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE)
    household = models.ForeignKey(HouseHold,null=False,blank=False,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    description = models.CharField(max_length=250,null=True,blank=True)
    status = models.CharField(choices=TASK_STATUS,default=[0],max_length=20)
    start = models.DateTimeField(blank=True,null=True)
    due = models.DateTimeField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)
    
