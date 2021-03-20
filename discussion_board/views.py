from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'discussion_board/index.html', context)
