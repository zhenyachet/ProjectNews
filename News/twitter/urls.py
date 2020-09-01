from django.urls import path, re_path
from . import views

urlpatterns = [
    #re_path(r'^update/(?P<id>[0-9]{4})/$', views.year_archive)
    path('auth', views.auth, name="auth"),
    # re_path(r'^get_list/(?P<page>\d+)/$', views.get_list, name="get-list"),
    path('get_list', views.get_list, name="get-list"),
    path('success', views.success, name="success"),
    path('update', views.update_twits, name="update-twits"),
    path('', views.person_actions, name="person-actions"),

]
