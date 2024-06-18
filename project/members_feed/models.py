from django.db import models
import uuid

class User(models.Model):
    userid = models.TextField()
    name = models.CharField(max_length=255)
    phone = models.CharField(null=True,max_length=15,blank=True)
    email = models.CharField(max_length=255, blank=True,null=True)
    content=models.TextField(blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image=models.TextField(blank=True,null=True)
    place=models.JSONField(blank=True,null=True)

    class Meta:
      ordering = ('date_added',)



