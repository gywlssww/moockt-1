from django.db import models

# Create your models here.
class ChatbotUser(models.Model):
    user_id = models.CharField(max_length=50)
    exp_date = models.DateTimeField(auto_now=True)
    