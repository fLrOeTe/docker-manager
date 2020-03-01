import docker
import os
import time
import sys

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



a=DockerView()
