import docker
import os
import time
import sys
import json
from io import BytesIO

# root是指当前目录路径(文件夹的绝对路径)
# dirs是指路径下所有的子目录(文件夹里的文件夹)
# files是指路径下所有的文件(文件夹里所有的文件)
def openFile(file_dir):
    bayes_list=[]
    svm_list=[]
    xgboost_list=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[0] == 'bayes':
                bayes_list.append(os.path.join(root,file))
                print((bayes_list))
            elif os.path.splitext(file)[0] == 'svm':
                svm_list.append(os.path.join(root,file))
                print(svm_list)
            elif os.path.splitext(file)[0] == 'xgboost':
                xgboost_list.append(os.path.join(root,file))
                print(xgboost_list)
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件

class DockerView():
    def __init__(self,*args,**kwargs):
        if "path" in kwargs and kwargs["path"]!="":
            self.path=kwargs["path"]
            try:
                self.dockerm=docker.client(base_url=self.path)
            except Exception as e:
                self.dockerm=docker.from_env()
                raise e
                pass
        else:
            self.dockerm=docker.from_env()

    def pullImages(self,*args,**kwargs):
        imageName=kwargs["name"]
        tag=kwargs["tag"]
        try:
            res=self.dockerm.pull(imageName,tag=tag)
            print(res)
        except Exception as e:
            print(e)

    def getAllImage(self,*args,**kwargs):
        try:
            imageDict=self.dockerm.images()
        except Exception as e:
            return {}
        dict={}
        if imageDict == {}:
            return {}
        for i in imageDict:
            id=i["Id"][7:]
            name=i["RepoTags"][0]
            size=i["Size"]
            time=i["Created"]
            dict.update({
                name:{
                    "name":name,
                    "id":id,
                    "size":size,
                    "time":time
                }
            })
        return dict
    def getAllContainers(self):
        try:
            conDict=self.dockerm.containers()
            return conDict
        except Exception as e:
            return {}

    def imageBuild(self,*args,**kwargs):
        try:
            path=kwargs["path"]
            f=open(path,"r")
            str=f.read()
            tags=kwargs["tag"]
            print(str)
            f=BytesIO(str.encode('utf-8'))
            response=[line for line in self.dockerm.build(
                fileobj=f,rm=True,tag=tags
            )]
            f.close()
            print(response)
        except Exception as e:
            raise e

a=DockerView()
#a.pullImages(name="centos",tag="latest")
a.imageBuild(path="/home/lot/Desktop/rm/Dockerfile",tag="web1:latest")