from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^patient/index/$', views.index, name='index'),
    url(r'^patient/new/$', views.new, name='new'),
    url(r'^patient/(?P<patient_id>[0-9]+)/$', views.show, name='show'),
]
