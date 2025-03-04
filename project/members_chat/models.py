from django.db import models

class Message(models.Model):
   
    room = models.CharField(max_length=255)
    message = models.JSONField(null=True, blank=True,default=list)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)