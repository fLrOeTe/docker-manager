import docker
import os
import time
import sys
import json
from io import BytesIO

class DockerView():
    def __init__(self,*args,**kwargs):
        if "path" in kwargs and kwargs["path"]!="":
            self.path=kwargs["path"]
            try:
                self.dockerm=docker.client(base_url=self.path,timeout=100)
            except Exception as e:
                self.dockerm=docker.from_env()
                raise e
        else:
            self.dockerm=docker.from_env()
    """
        About Image
    """
    def pullImages(self,*args,**kwargs):
        imageName=kwargs["name"]
        try:
            res=self.dockerm.pull(imageName)
            print(res)
        except Exception as e:
            print(e)

    def getAllImage(self,*args,**kwargs):
        try:
            imageDict=self.dockerm.images()
        except Exception as e:
            return {}
        dict=[]
        if imageDict == {}:
            return {}
        for i in imageDict:
            id=i["Id"][7:]
            name=i["RepoTags"][0]
            name1=name[0:name.rfind(':',1)]
            tag=name[name.rfind(':',1)+1:]
            size=i["Size"]
            time=i["Created"]
            dict.append({
                    "name":name1,
                    "tag":tag,
                    "id":id,
                    "size":size,
                    "time":time
            })
        return dict
    def downloadImage(self,image,path,name):
        try:
            image=self.dockerm.get_image(image)
            f=open(path+"/"+name+".tar","wb")
            for chunk in image:
                f.write(chunk)
            f.close()
            return {
                "success":True,
                "msg":"download successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    def importImage(self,src=None, repository=None, tag=None, image=None, changes=None, stream_src=False):
        try:
            self.dockerm.import_image(src=src,repository=repository,tag=tag,image=image,changes=changes,stream_src=False)
            return {
                "success":True,
                "msg":"import image success"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }

    def importImageByfile(self,filename,repository=None,tag=None,changes=None):
        try:
            self.dockerm.import_image_from_file(filename=filename,repository=repository,tag=tag,changes=changes)
            return {
                "success": True,
                "msg": "import image success"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }

    def inspectImage(self,image):
        try:
            dist=self.dockerm.inspect_image(image=image)
            return dist
        except Exception as e:
            return {
                "fail":str(e)
            }
    def pushImage(self,repository, tag=None, stream=False, auth_config=None, decode=False):
        try:
            resp=[]
            for line in self.dockerm.push(repository=repository,tag=tag,stream=stream,auth_config=auth_config,decode=decode):
                print(line)
                resp.append(line)
            return {
                "success":True,
                "msg":resp
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }

    def removeImage(self,image,force=False,noprune=False):
        try:
            self.dockerm.remove_image(image,force=force,noprune=noprune)
            return {
                "success":True,
                "msg":"remove Image successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }

    def searchImage(self,tern):
        try:
            ret=self.dockerm.search(tern)
            return ret
        except Exception as e:
            return {
                "fail":str(e)
            }


    def imageBuild(self,path,tags):
        try:
            f=open(path,"r")
            str=f.read()
            print(str)
            f=BytesIO(str.encode('utf-8'))
            response=[line for line in self.dockerm.build(
                fileobj=f,rm=True,tag=tags
            )]
            f.close()
            print(response)
            return {
                "success":True,
                "msg":"build image success"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e,
                "response":response
            }
    def imageBuilds(self,*args,**kwargs):
        try:
            response = [line for line in self.dockerm.build(**kwargs)]
            print(response)
            return {
                "success":True,
                "msg":"build image success",
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e,
                "response":response
            }
    def deleteCacheAfterBuild(self):
        try:
            dict=self.dockerm.prune_builds()
            return {
                "success":True,
                "msg":dict
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    def tagImage(self,image,repository,tag=None,force=False):
        try:
            bool=self.dockerm.tag(image,repository,tag=tag,force=force)
            if bool==True:
                return {
                    "success":bool,
                    "msg":"tag image success"
                }
            else:
                return {
                    "success":bool,
                    "msg":"fail!!!"
                }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }

    """
        About Network
    """
    def creatEndpoint(self,aliases=None,links=None,ipv4_address=None,ipv6_address=None,link_local_ips=None,*args,**kwargs):
        try:
            end_config=self.dockerm.create_endpoint_config(aliases=aliases,links=links,ipv4_address=ipv4_address,ipv6_address=ipv6_address,\
                                                           link_local_ips=link_local_ips)
            return end_config
        except Exception as e:
            raise e

    def createIpamPool(self,subnet=None, iprange=None, gateway=None, aux_addresses=None):
        try:
            ipam_pool=docker.types.IPAMPool(
                subnet=subnet,
                iprange=iprange,
                gateway=gateway,
                aux_addresses=aux_addresses
            )
            return ipam_pool
        except Exception as e:
            raise e

    def createIpamConfig(self,driver='default',pool_configs=None,options=None):
        try:
            ipam_config=docker.types.IPAMConfig(
                driver=driver,
                pool_configs=pool_configs,
                options=options
            )
            return ipam_config
        except Exception as e:
            raise e

    def createNetwork(self,name, driver=None, options=None, ipam=None, check_duplicate=None, internal=False, labels=None, \
                      enable_ipv6=False, attachable=None, scope=None, ingress=None):
        try:
            network=self.dockerm.create_network(name=name,driver=driver,options=options,ipam=ipam,check_duplicate=check_duplicate,\
                                                internal=internal,labels=labels,enable_ipv6=enable_ipv6)
            return network
        except Exception as e:
            raise e
        
    def createNetworkConfig(self,name,aliases=None,links=None,ipv4_address=None,ipv6_address=None,link_local_ips=None):
        try:
            networkEndpoint=self.creatEndpoint(aliases=aliases,links=links,ipv4_address=ipv4_address,ipv6_address=ipv6_address,link_local_ips=link_local_ips)
            networkConfig=self.dockerm.create_networking_config({
                name:networkEndpoint
            })
            return networkConfig
        except Exception as e:
            raise e
        
    def connectToNetwork(self,container,net_id, ipv4_address=None, ipv6_address=None, aliases=None, links=None, link_local_ips=None):
        try:
            self.dockerm.connect_container_to_network(container=container,net_id=net_id,ipv4_address=ipv4_address,ipv6_address=ipv6_address,aliases=aliases,\
                                                      links=links,link_local_ips=link_local_ips)
            msg={
                "success":True,
                "msg":"connect successfully"
            }
            return msg
        except Exception as e:
            msg={
                "success":False,
                "msg":str(e)
            }
            return msg

    def disconnectFromNetwork(self,container, net_id, force=False):
        try:
            self.dockerm.disconnect_container_from_network(container=container,net_id=net_id,force=force)
            return {
                "success":True,
                "msg":"disconnect successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    def showNetwork(self,name=None,ids=None):
        try:
            net=self.dockerm.networks(names=name,ids=ids)
            return net
        except Exception as e:
            return {
                "failed":str(e)
            }

    def showNetworkDetail(self,net_id,verbose=None,scope=None):
        try:
            detail=self.dockerm.inspect_network(net_id=net_id)
            print(detail)
        except Exception as e:
            print(e)
    
    def removeNetwork(self,net_id):
        try:
            self.dockerm.remove_network(net_id=net_id)
            return {
                "success":True,
                "msg":"remove network successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    """
        About Volumes
    """
    def createVolumes(self,name=None,driver=None,driver_opts=None,labels=None):
        try:
            dic=self.dockerm.create_volume(name=name,driver=driver,driver_opts=driver_opts,labels=labels)
            return {
                "success":True,
                "msg":dic
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    def detailVolumes(self,name):
        try:
            dic=self.dockerm.inspect_volume(name=name)
            return {
                "success":True,
                "msg":dic
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    def removeVolumes(self,name,force=False):
        try:
            self.dockerm.remove_volume(name=name,force=force)
            return {
                "success":True,
                "msg":"delete this volume successsfully"
            }
        except Exception as e:
            return {
                "success":True,
                "msg":"failed to remove this volume"
            }
    def listVolumes(self,filters=None):
        try:
            dic=self.dockerm.volumes(filters=filters)
            return {
                "success":True,
                "msg":dic
            }
        except Exception as e:
            return {
                "success":False,
                "msg":str(e)
            }
    """
        About exec
    """
    def execContainer(self,container,cmd,stdout=True,stderr=True,stdin=False,tty=False,privileged=False,user='',environment=None,workdir=None,detach_keys=None):
        try:
            cont=self.dockerm.exec_create(container=container,cmd=cmd,stdout=stdout,stderr=stderr,stdin=stdin,tty=tty,privileged=privileged,user=user,environment=environment,workdir=workdir,detach_keys=detach_keys)
            return {
                "success":True,
                "msg":cont
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    def execDetail(self,exec_id):
        try:
            det=self.dockerm.exec_inspect(exec_id=exec_id)
            return {
                "success":True,
                "msg":det
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    def execResize(self,exec_id,height=None,width=None):
        try:
            self.dockerm.exec_resize(exec_id=exec_id,height=height,width=width)
            return {
                "success":True,
                "msg":"resize exec successful"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    def execStart(self,exec_id,detach=False,tty=False,stream=False,socket=False,demux=False):
        try:
            ret=self.dockerm.exec_start(exec_id=exec_id,detach=detach,tty=tty,stream=stream,socket=socket,demux=demux)
            return {
                "success":True,
                "msg":str(ret)
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    """
        About Configs
    """
    def getAllConfigs(self,filters=None):
        try:
            dict=self.dockerm.configs(filters=filters)
            return {
                "success":True,
                "msg":dict
            }
        except Exception as e:
            return {
                "success":True,
                "msg":e
            }
    def createConfig(self,name,data,labels=None):
        try:
            dict=self.dockerm.create_config(name=name,data=data,labels=labels)
            return {
                "success":True,
                "msg":dict
            }
        except Exception as e:
            return {
                "success":True,
                "msg":e
            }
    def detailConfig(self,id):
        try:
            dict=self.dockerm.inspect_config(id=id)
            return {
                "success":True,
                "msg":dict
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }
    def removeConfig(self,id):
        try:
            boole=self.dockerm.remove_config(id)
            if boole==True:
                return {
                    "success":True,
                    "msg":"delete Config successfully"
                }
            else:
                return {
                    "success":False,
                    "msg":"delete config failed"
                }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }

    """
        About Container
    """
    def attachContainerBySocket(self,container,params=None,ws=False):
        try:
            socket=self.dockerm.attach_socket(container=container,params=params,ws=ws)
            return socket
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }


    def getAllContainers(self):
        try:
            conDict=self.dockerm.containers()
            return {
                "success":True,
                "msg":conDict
            }
        except Exception as e:
            return {
                "success":False,
                "msg":False
            }

