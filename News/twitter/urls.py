from django.urls import path, re_path
from . import views

urlpatterns = [
    #re_path(r'^update/(?P<id>[0-9]{4})/$', views.year_archive),
    path('success', views.success, name="success"),
    path('update', views.update_twits, name="update-twits"),
    path('', views.person_actions, name="person-actions"),

]
