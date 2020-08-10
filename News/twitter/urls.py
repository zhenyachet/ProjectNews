from django.urls import path
from . import views

urlpatterns = [
    path('', views.person_actions, name="person-actions"),
]
