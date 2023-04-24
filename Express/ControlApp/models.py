from django.db import models

class Course(models.Model):
    name=models.CharField(max_length=256)
    language=models.CharField(max_length=3)
    price=models.CharField(max_length=10)

    def __str__(self):
        return self.name