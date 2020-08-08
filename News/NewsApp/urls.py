from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('rss/', views.rss, name="rss"),
  #  path('resources/<url>', views.resources_detail, name="resources-detail"),
    path('resources/', views.resources, name="resources"),

]

