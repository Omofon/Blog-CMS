from django.urls import path, re_path

from .views import (
    PostView,
    SinglePostView,
    post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
)
urlpatterns = [
    path('posts', PostView.as_view()),
    path('posts/<int:pk>', SinglePostView.as_view()),
    re_path(r'^$', post_list, name='list'),
    re_path(r'^create/$', post_create),
    re_path(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
