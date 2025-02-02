"""
URL configuration for MyNewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
#from rest_framework import routers
#from rest_framework.routers import DefaultRouter
from news_app.views import PostsList, NewsListView, ArticlesListView


#router = DefaultRouter()
#router = routers.DefaultRouter()
#router.register(r'posts', views.PostViewset, basename='post')


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news_app.urls')),
    path('protect/', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('news/', NewsListView.as_view(), name='news_list'),  #'news_app.urls'
    path('articles/', ArticlesListView.as_view(), name='articles_list'),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
