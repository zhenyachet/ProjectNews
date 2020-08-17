from django.urls import path
from . import views

urlpatterns = [
    path('update', views.update_twits, name="update-twits"),
    path('', views.person_actions, name="person-actions"),

]
