"""DockerManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from django.urls import include,path
from django.conf.urls import url
from dockermanage.views import *
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
router=routers.SimpleRouter()
router.register(r'images',ImageConfigViewSet,base_name="image-detail")
schema_view=get_swagger_view(title='api doc')
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/image$',ImageView.as_view(),name='image'),
    url(r'^api/image/download$',ImagedownloadView.as_view(),name="downloadimage"),
    url(r'^api/image/import$',ImageImportView.as_view(),name="importimage"),
    url(r'^api/image/detail$',ImageDetailView.as_view(),name="detailimage"),
    url(r'^api/image/remove$',ImageRemoveView.as_view(),name="removeimage"),
    url(r'^api/container$',ContainerView.as_view(),name='container'),
    url(r'^', include(router.urls))
]
urlpatterns+=[
    path(r'docs/',schema_view),
]
