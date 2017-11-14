from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.index, name = "index"),
    url(r"^post/$", views.PostUserData.post, name = "post"),
]