from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageModel
        fields=('name','id','time','size')
class AssetSerializer(serializers.ModelSerializer):
    hostname = serializers.CharField(help_text='主机')

    class Meta:
        model = Asset
        fields = '__all__'