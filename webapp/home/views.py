from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .tasks import add_board

from crawl.tasks import crawl_board
from post.models import Board

from utils.paginate import paginate
from utils.response import http_response_data
from utils.request_params import param2str

# Create your views here.
class HomeView(View):
    def render_home(self, request):
        qs = Board.objects.select_related('crawler').all()
        paged_objs, count, page, limit = paginate(qs, request, limit_defval=5)

        data = http_response_data(
            request,
            **{
                'board_list': paged_objs,
                'page': page,
                'limit': limit,
                'count': count,
            }
        )

        return render(request, 'home.html', data)

    def get(self, request):
        return self.render_home(request)

    def post(self, request):
        args = request.POST or None
        board_name = args.get('board', "")

        add_board.delay(board_name)
        return self.render_home(request)


def action_browse(request, board_name="", **kwargs):
    return redirect(reverse('post:board', args=(board_name, )))

def action_default(request, board_name="", **kwargs):
    return redirect(reverse('home:home'))

def action_crawl(request, board_name="", **kwargs):
    crawl_board.delay(board_name)
    return redirect(reverse('home:home'))

action_list = {
    'default': action_default,
    'browse': action_browse,
    'crawl': action_crawl,
}

class HomeActionView(View):
    def get(self, request):
        return redirect(reverse('home:home'))

    def post(self, request):
        name = param2str(request, 'POST', 'board_name', "")
        action = param2str(request, 'POST', 'action', "default")

        handler = action_list.get(action, action_default)
        return handler(request, board_name=name)

