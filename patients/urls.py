from django.conf.urls import url

# from happy_bday import settings
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^patients/$', views.IndexView.as_view(), name='index'),
    url(r'^patients/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^patients/signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^patients/create/$', views.create, name='create'),
    url(r'^patients/destroy/$', views.destroy, name='destroy'),
]
