from django.urls import re_path
from .views import BoardView, PostView

app_name = 'post'

urlpatterns = [
    re_path('^(?P<board_name>\w+)/$', BoardView.as_view(), name='board'),
    re_path('^(?P<board_name>\w+)/(?P<endpoint>.+)/', PostView.as_view(), name='post'),
]