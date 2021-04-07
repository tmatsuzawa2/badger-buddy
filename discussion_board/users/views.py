from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/index.html', context)
