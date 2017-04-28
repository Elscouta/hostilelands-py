from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', 
        views.index, name='world.index'),
    url(r'^newvillage/$', 
        views.newvillage, name='world.newvillage'),
]
