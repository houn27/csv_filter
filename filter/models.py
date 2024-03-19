from django.db import models
import time


# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=200)

    path = models.CharField(max_length=200)

    types = models.CharField(max_length=2000,null=True,blank=True)

    create_date=models.BigIntegerField(default=int(time.time()))