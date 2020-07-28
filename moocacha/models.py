from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Test(models.Model):
    #test
    message = models.CharField(max_length=100)
    shifted = models.CharField(max_length=254)
    op = models.CharField(max_length=100)
 