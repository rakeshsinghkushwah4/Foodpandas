from django.db import models
from django.utils.text import slugify

from accounts.models import MyProfile

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    Category = (('Indoor','Indoor'),('Out Door','Out Door'))
    seller = models.ForeignKey(to=MyProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    Category = models.CharField(max_length=100,choices = Category)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    cr_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True,unique=True)
    product_status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)
