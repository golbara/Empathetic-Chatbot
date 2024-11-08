from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
    template = loader.get_template("bot/index.html")
    # return HttpResponse(template)
    return render(request, "bot/index.html")