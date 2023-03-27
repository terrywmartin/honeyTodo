from django.db import models

from uuid import uuid4

# Create your models here.
class HouseHold(models.Model):
    name = models.CharField(max_length=250,blank=False,null=True)
    id = models.UUIDField(default=uuid4, unique=True,primary_key=True,editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Invitations(models.Model):
    email = models.EmailField(max_length=250,blank=False,null=False)
    household = models.ForeignKey(HouseHold, on_delete=models.CASCADE,null=False,blank=False)
    token = models.UUIDField(default=uuid4,blank=False,null=False)
    id = models.UUIDField(default=uuid4, unique=True,primary_key=True,editable=False)

