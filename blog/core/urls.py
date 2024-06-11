from django.urls import path, include
# from django.conf.urls import url
from .views import (register_view, login_view, logout_view,index_view, UserGroupView)
 
urlpatterns = [
    path('index/', index_view, name="index"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('groups/<str:group>/users', UserGroupView.as_view({'get': 'list', 'post': 'create'})),
    path('groups/<str:group>/users/<int:pk>', UserGroupView.as_view({'delete': 'remove'})),

]