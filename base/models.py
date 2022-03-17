from django.db import models

# Create your models here.

class Room(models.Model):
    #host = 
    #topic = 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True ,max_length=500, blank=True)
    #participants = 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str (self):
        return self.name

