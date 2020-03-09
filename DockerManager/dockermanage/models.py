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

class ImageTModel(models.Model):
    name = models.CharField(max_length=100)
    tag=models.CharField(max_length=50)
    id = models.CharField(max_length=200, primary_key=True)
    time = models.CharField(max_length=100)
    size = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'ImageT'
        verbose_name_plural = verbose_name
class Asset(models.Model):
    hostname = models.CharField(max_length=64, verbose_name='主机名', unique=True)
    ip = models.CharField(max_length=30, verbose_name='ip', blank=True, null=True, )
    class Meta:
        db_table = "asset"
        verbose_name = "asset"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname

class IpamPoolModel(models.Model):
    subnet=models.CharField(max_length=64,primary_key=True)
    iprange=models.CharField(max_length=72)
    gateway=models.CharField(max_length=100)
    aux_addresses=models.CharField(max_length=150)

    class Meta:
        verbose_name='IpamPool'
        verbose_name_plural=verbose_name
