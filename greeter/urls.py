from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^greeter/$', views.IndexView.as_view(), name='index'),
    url(r'^greeter/signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^greeter/signout/$', views.signout, name='signout'),
    url(r'^greeter/drchrono_redirect', views.drchrono_redirect, name='drchrono_redirect'),
]
