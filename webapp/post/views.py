from django.http.response import Http404
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Post, Board

from utils.response import http_response_data
from utils.paginate import paginate

# Create your views here.
class BoardView(View):
    def get(self, request, board_name=""):
        qs = Post.objects.select_related('board').filter(board__name__iexact=board_name).order_by('-create_time')
        paged_objs, count, page, limit = paginate(qs, request)

        data = http_response_data(
            request, 
            **{
                'board_name': board_name,
                'post_list': paged_objs,
                'page': page,
                'limit': limit,
                'count': count
            }
        )

        return render(request, 'board.html', data)


class PostView(View):
    def get(self, request, board_name="", endpoint=""):
        try:
            post = Post.objects.get(Q(board__name__exact=board_name), Q(endpoint=endpoint))
        except Post.DoesNotExist:
            raise Http404()

        data = http_response_data(
            request,
            **{
                'post': post,
            }
        )

        return render(request, 'post.html', data)