from django.conf.urls import url

# from happy_bday import settings
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^patients/$', views.IndexView.as_view(), name='index'),
    url(r'^patients/signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^patients/signout/$', views.signout, name='signout'),
    url(r'^patients/drchrono_signin', views.drchrono_signin, name='drchrono_signin'),
]
