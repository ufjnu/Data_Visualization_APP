from django.db import models

# Create your models here.
from django.db import models

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.TextField()