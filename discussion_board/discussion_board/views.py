from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Post, User
from .forms import CreatePostForm

# Create your views here.

def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'discussion_board/index.html', context)

def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            details = form.cleaned_data['details']
            p = Post(title=title, details=details, user=User.objects.get(pk=1))
            p.save()
            return HttpResponseRedirect('/board')

    else:
        form = CreatePostForm()

    context = {
        'form': form
    }

    return render(request, 'discussion_board/create-post.html', context)

