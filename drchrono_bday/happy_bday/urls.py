from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^patients/$', views.index, name='index'),
    url(r'^patients/new/$', views.new, name='new'),
    url(r'^patients/(?P<patient_id>[0-9]+)/$', views.show, name='show'),
]
