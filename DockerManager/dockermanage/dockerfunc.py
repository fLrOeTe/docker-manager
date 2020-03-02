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
                "msg":e
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
                "msg":e
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
                "msg":e
            }

    def inspectImage(self,image):
        try:
            dist=self.dockerm.inspect_image(image=image)
            return dist
        except Exception as e:
            return {
                "fail":e
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
                "msg":e
            }

    def removeImage(self,image,force=False,noprune=False):
        try:
            self.dockerm.remove_image(image=image,force=force,noprune=noprune)
            return {
                "success":True,
                "msg":"remove Image successfully"
            }
        except Exception as e:
            return {
                "success":False,
                "msg":e
            }

    def searchImage(self,tern):
        try:
            ret=self.dockerm.search(tern)
            return ret
        except Exception as e:
            return {
                "fail":e
            }

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
                "msg":e
            }


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
                "msg":e
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
                "msg":e
            }
    def showNetwork(self,name=None,ids=None):
        try:
            net=self.dockerm.networks(names=name,ids=ids)
            return net
        except Exception as e:
            return {
                "failed":e
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
                "msg":e
            }
    


a=DockerView()
#a.pullImages(name="centos",tag="latest")
#print(json.dumps(a.showNetwork(),indent=3))
#a.showNetworkDetail(net_id="b0514c47f75cf59c9826b4adfc5d90240d185e03d989e557aa67cb9884e172ba")
print(a.searchImage(tern="ctfd"))