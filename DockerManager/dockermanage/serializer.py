from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageModel
        fields=('name','id','time','size')
