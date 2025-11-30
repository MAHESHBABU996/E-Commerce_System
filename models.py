from django.db import models

# ...existing code...

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name