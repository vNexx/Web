from django.shortcuts import render

from django.http import HttpResponse
from askmeapp import models

def index(request):
    #return HttpResponse("Hello, world. You're at ASKME APP.")
    str = "alah akbar!!!!"
    return render(request, 'index.html', {"question": str}, )
    #return render(request, 'index.html', {'articles': models.Article.objects.all()} )
