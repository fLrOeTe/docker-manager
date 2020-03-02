from django.shortcuts import render
from .dockerfunc import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .models import *
from .serializer import *
from rest_framework import mixins,generics,permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics
from .models import *
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet,ViewSet
from rest_framework.decorators import action
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

class ImageConfigViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
    dk=DockerView()
    @action(methods=['get'],detail=False)
    def all(self,request):
        image=self.dk.getAllImage()
        return  Response(image)

    @action(methods=['post'],detail=False)
    def search(self,request):
        image=self.dk.inspectImage(request.data["name"])
        return Response(image)

class ImagedownloadView(APIView):
    def __init__(self):
        self.dclass=DockerView()
    def get(self,request):
        imageSet=self.dclass.getAllImage()
        return Response(imageSet)
    def post(self,request):
        iamge=request.data["image"]
        path=request.data["path"]
        name=request.data["name"]
        ret=self.dclass.downloadImage(image=iamge,path=path,name=name)
        return Response(ret)

class ImageImportView(APIView):
    def __init__(self):
        self.dclass=DockerView()
    def get(self,request):
        imageSet=self.dclass.getAllImage()
        return Response(imageSet)
    def post(self,request):
        filename=request.data["filename"]
        repository=request.data["rep"]
        tag=request.data["tag"]
        changes=request.data["changes"]
        ret=self.dclass.importImageByfile(filename=filename,repository=repository,tag=tag,changes=changes)
        return Response(ret)

class ImageDetailView(APIView):
    def __init__(self):
        self.dclass=DockerView()
    def get(self,request):
        imageSet=self.dclass.getAllImage()
        return Response(imageSet)
    def post(self,request):
        image=request.data["image"]
        ret=self.dclass.inspectImage(image=image)
        return Response(ret)
class ImageRemoveView(APIView):
    def __init__(self):
        self.dclass=DockerView()
    def get(self,request):
        imageSet=self.dclass.getAllImage()
        return Response(imageSet)
    def post(self,request):
        image=request.data["image"]
        force=request.data["force"]
        noprune=request.data["noprune"]
        forces=False
        if force=="True":
            forces=True
        ret=self.dclass.removeImage(image=image,force=forces)
        return Response(ret)