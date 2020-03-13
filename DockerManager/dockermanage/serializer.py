from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageModel
        fields=('name','id','time','size')

class ImageTSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageTModel
        fields=('name','tag','id','time','size')
class AssetSerializer(serializers.ModelSerializer):
    hostname = serializers.CharField(help_text='主机')

    class Meta:
        model = Asset
        fields = '__all__'

class IpamPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpamPoolModel
        fields=('subnet','iprange','gateway','aux_addresses')


class VolumesSerializer(serializers.ModelSerializer):
    class Meta:
        model=VolumesMode
        fields=('name','driver','driver_opts','labels')