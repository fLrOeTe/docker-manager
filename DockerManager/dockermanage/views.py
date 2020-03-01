from django.shortcuts import render
from .dockerfunc import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework import generics
# Create your views here.

class ImageView(APIView):
    def __init__(self):
        self.dclass=DockerView()
    def get(self,request):
        imageSet=self.dclass.getAllImage()
        return Response(imageSet)
    def post(self,request):
        imageName=request.data["name"]
        tag=request.data["tag"]
        try:
            self.dclass.pullImages(name=imageName,tag=tag)
            msg={
                "success":True,
                "msg":"pull image successfully!"
            }
            return Response(msg)
        except Exception as e:
            msg={
                "success":False,
                "msg":"Failed!!"
            }
            return Response(msg)
class ContainerView(APIView):
    def __init__(self):
        self.dclass=DockerView()
        self.imageSet=self.dclass.getAllImage()
        for i in self.imageSet:
            if ImageModel.objects.filter(id=self.imageSet[i]["id"]).count()==0:
                serializer=ImageSerializer(data=self.imageSet[i])
                if serializer.is_valid():
                    serializer.save()

    def get(self,request):
        conSet=self.dclass.getAllContainers()
        return Response(conSet)


