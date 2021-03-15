from django.http.response import HttpResponseNotModified
from django.urls import re_path
from .views import (
    HomeView,
    HomeActionView,
)

app_name = 'home'

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^action/', HomeActionView.as_view(), name='action'),
]