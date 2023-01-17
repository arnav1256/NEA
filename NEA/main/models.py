from django.db import models

# Create your models here.
class List(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Item(models.Model):
    li = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    complete = models.BooleanField()
    def __str__(self):
        return self.text