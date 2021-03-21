from django.shortcuts import render
from ..models import Post

# Create your views here.

def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'discussion_board/index.html', context)
