from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^patients/$', views.IndexView.as_view(), name='index'),
    url(r'^patients/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^patients/create/$', views.add, name='create')
    url(r'^patients/destroy/$', views.add, name='destroy')
]
