from django.shortcuts import render
from .models import test_query

def show_main(request):
    test_query()
    context={}
    return render(request, "main.html", context)

