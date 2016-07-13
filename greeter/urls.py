from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^greeter/$', views.IndexView.as_view(), name='index'),
    url(r'^greeter/signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^greeter/signout/$', views.signout, name='signout'),
    url(r'^greeter/drchrono_signin', views.drchrono_signin, name='drchrono_signin'),
]
