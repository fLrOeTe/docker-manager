from django.db import models

# Create your models here.
class ImageModel(models.Model):
    name=models.CharField(max_length=100)
    id=models.CharField(max_length=200,primary_key=True)
    time=models.CharField(max_length=100)
    size=models.CharField(max_length=100)
    class Meta:
        verbose_name='Image'
        verbose_name_plural=verbose_name