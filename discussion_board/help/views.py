from django.http import HttpResponseRedirect
import random
from ..models import Quotes
from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    quote = get_object_or_404(Quotes, id=random.randrange(2, Quotes.objects.all().count()))
    context = {
        'quote': quote
    }
    return render(request, 'help_resources/index.html', context)
