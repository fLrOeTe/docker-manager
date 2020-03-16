from django.shortcuts import render
from .dockerfunc import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
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
from .schema_view import DocParam
from django.shortcuts import HttpResponse
from rest_framework import permissions
from rest_framework import generics
import json
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

    def get(self,request):
        conSet=self.dclass.getAllContainers()
        return Response(conSet)

class ImageConfigViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = ImageTModel.objects.all()
    serializer_class = ImageTSerializer
    dk=DockerView()
    """
    all:
        return all images
    search:
        search images local
    delete:
        delete images local
    detail:
        retuen the image's detail
    find:
        search images in network
    pull:
        download image from network
    """
    def refrush(self):
        image = self.dk.getAllImage()
        for i in image:
            if self.get_queryset().filter(name=i["name"]).count() == 0:
                ser = self.get_serializer(data=i)
                if ser.is_valid():
                    ser.save()
            elif self.get_queryset().filter(tag=i["tag"]).count() == 0:
                ser = self.get_serializer(data=i)
                if ser.is_valid():
                    ser.save()
            else:
                pass
    @action(methods=['get'],detail=False)
    def all(self,request):
        self.refrush()
        return  Response(self.get_queryset().all().values())

    @action(methods=['post'],detail=False)
    def search(self,request):
        self.refrush()
        name=request.data["name"]
        ret=self.get_queryset().filter(name=name)
        image=self.dk.inspectImage(request.data["name"])
        return Response(ret.values())
    @action(methods=['post'],detail=False)
    def delete(self,request):
        self.refrush()
        print(request.data)
        name=request.data["name"]
        tag=request.data["tag"]
        id=request.data["id"]
        print(str(id))
        image=""
        if id!="":
            ret=model_to_dict(self.get_queryset().filter(id=id).first())
            if ret!={}:
                img=ret["name"]+":"+ret["tag"]
                dic=self.dk.removeImage(image=img,force=True)
                if dic["success"]==True:
                    self.get_queryset().filter(id=id).delete()
                    return  Response(dic)
                else:
                    return Response(dic)
            else:
                return Response({
                    "msg":"no mach"
                })
        elif name!="":
            if tag!="":
                img=name+":"+tag
                dic=self.dk.removeImage(image=img,force=True)
                self.get_queryset().filter(name=name,tag=tag).delete()
                return Response(dic)
            else:
                img=name
                dic=self.dk.removeImage(image=img,force=True)
                if dic["success"]==True:
                    self.get_queryset().filter(name=name).delete()
                    return Response(dic)
                else:
                    return Response(dic)
    @action(methods=['post'],detail=False)
    def detail(self,request):
        name=request.data["name"]
        id=request.data["id"]
        tag=request.data["tag"]
        if id!="":
            ret=model_to_dict(self.get_queryset().filter(id=id).first())
            if ret!={}:
                name=ret["name"]+":"+ret["tag"]
                dic=self.dk.inspectImage(image=name)
                return Response({
                    "success":True,
                    "msg":dic
                })
            else:
                return Response({
                    "success":False,
                    "msg":"No"
                })
        elif name!="":
            dic={}
            if tag!="":
                name=name+":"+tag
                dic=self.dk.inspectImage(image=name)
            else:
                dic=self.dk.inspectImage(image=name)
            return Response({
                "success":True,
                "msg":"No"
            })
        else:
            return Response({
                "success":False,
                "msg":"No"
            })
    @action(methods=['post'],detail=False)
    def find(self,request):
        name=request.data['name']
        dic=self.dk.searchImage(tern=name)
        return Response(dic)
    @action(methods=['post'],detail=False)
    def pull(self,request):
        name=request.data['name']
        try:
            self.dk.pullImages(name=name)
            ret={
                "success":True,
                "msg":"pull image success!"
            }
            self.refrush()
            return Response(ret)
        except Exception as e:
            ret={
                "success":False,
                "msg":e
            }
class NetworkViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = IpamPoolModel.objects.all()
    serializer_class = IpamPoolSerializer
    dk=DockerView()

    @action(methods=['post'],detail=False)
    def create_ip_pool(self,request):
        subnet=request.data['subnet']
        iprange=request.data['iprange']
        gateway=request.data['gateway']
        aux_addresses=request.data['aux_addresses']
        data={
            "success":True,
            "data":{
                "subnet":subnet,
                "iprange":iprange,
                "gateway":gateway,
                "aux_addresses":aux_addresses
            }
        }
        if self.get_queryset().filter(subnet=subnet,iprange=iprange,gateway=gateway,aux_addresses=aux_addresses).count() == 0:
            ser=self.get_serializer(data=data["data"])
            if ser.is_valid():
                ser.save()
                return Response(data)
        return Response({
            "success":False,
            "msg":"exist!"
        })
    @action(methods=['get'],detail=False)
    def all_ip_pool(self,request):
        return Response(self.get_queryset().all().values())
class VolumesViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = VolumesMode.objects.all()
    serializer_class = VolumesSerializer
    dk=DockerView()
    @action(methods=['get'],detail=False)
    def all(self,request):
        dict=self.dk.listVolumes()
        return Response(dict)
    @action(methods=['post'],detail=False)
    def create_volumes(self,request):
        name=request.data["name"]
        driver=request.data["driver"]
        driver_opts=json.loads(request.data["driver_opts"])
        labels=request.data["labels"]
        data={
            "name":name,
            "driver":driver,
            "driver_opts":driver_opts,
            "labels":labels
        }
        if self.get_queryset().filter(name=name).count()==0:
            dict=self.dk.createVolumes(name=name,driver=driver,driver_opts=driver_opts,labels=labels)
            ser=self.get_serializer(data=data)
            if ser.is_valid():
                ser.save
                return Response(dict)
        else:
            return {
                "success":False,
                "msg":"this value is exist!"
            }


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

class AssetInfo(generics.ListCreateAPIView):
    """
    资产
    """
    queryset = Asset.objects.get_queryset().order_by('id')
    serializer_class = AssetSerializer
    permission_classes = (permissions.IsAdminUser,)