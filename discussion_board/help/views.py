from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    context = {
    }
    return render(request, 'help_resources/index.html', context)
