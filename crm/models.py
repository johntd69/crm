from django.db import models
# Create your models here.
class Employees(models.Model):
    name=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    salary=models.PositiveIntegerField()
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField()
    contact=models.CharField(null=True,max_length=200)
    profile_pic=models.ImageField(upload_to="image",null=True)
    def _str_(self) :
        return self.name
class Book(models.Model):
    name=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    author_name=models.CharField(max_length=200)
    publisher=models.CharField(max_length=200)
    pages=models.PositiveIntegerField()

