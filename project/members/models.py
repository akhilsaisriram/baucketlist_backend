from django.db import models
import uuid

class User(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(null=True,max_length=15,blank=True)
    spass = models.CharField(null=True,max_length=255,blank=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(null=True,max_length=255,blank=True)
    bucket = models.JSONField(null=True, blank=True,default=list)
    gid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    curlocation=models.JSONField(null=True, blank=True,default=list)

    def save(self, *args, **kwargs):
        if not self.gid:
            self.gid = str(self.uid)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
