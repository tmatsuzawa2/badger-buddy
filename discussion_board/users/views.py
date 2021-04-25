from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import EditProfileForm
from ..models import Post, Reply
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/index.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, initial={"email": request.user.email})
        if form.is_valid():
            username = form.cleaned_data['username']
            # If taken, then change the is_valid()
            if User.objects.filter(username__iexact=username).exclude(email__iexact=request.user.email).exists():
                form._errors['username'] = ['The username has already been taken.']
            if form.is_valid():
                request.user.username = form.cleaned_data['username']
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.profile.anonymous = form.cleaned_data['anonymous']
                request.user.save()
                return HttpResponseRedirect('/profile/view/')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'users/edit_profile.html', context)


def post_history(request):
    user = request.user
    posts = Post.objects.filter(user=user)
    print(posts)
    replies = Reply.objects.all()
    context = {
        'posts': posts,
        'replies': replies
    }
    return render(request, 'users/post_history.html', context)


def reply_history(request):
    user = request.user
    replies = Reply.objects.filter(user=user)
    context = {
        'replies': replies
    }
    return render(request, 'users/reply_history.html', context)

