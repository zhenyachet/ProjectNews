from django.urls import path, re_path
from . import views

urlpatterns = [
    # re_path(r'^rest_list/(?P<filter_words>[\w]{1,15})$', views.list_view, name='rest-list'),
    path('auth', views.auth, name="auth"),
    # re_path(r'^get_list/(?P<page>\d+)/$', views.get_list, name="get-list"),
    path('get_list/', views.get_list, name="get-list"),
    path('success', views.success, name="success"),
    path('update', views.update_twits, name="update-twits"),
    # path('rest_list/<str:filter_words>/<str:sort/>', views.list_view, name="rest-list"),
    path('', views.person_actions, name="person-actions"),

]
