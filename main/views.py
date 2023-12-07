from django.shortcuts import redirect, render
from .queries import *

classes = ["cities", "matches", "players", "seasons", "teams", "umpires", "venues"]

def show_search(request):
    return render(request, 'search.html')

def show_result(request):
    input = request.GET.get("query")
    if input == None or input == "":
        return redirect("main:show_search")
    
    input_split = input.split()
    is_valid = True
    if len(input_split) == 1:
        if input_split[0] in classes:
            result = search_all_in_class(input_split[0])
        else:
            result = search_identifier(input_split[0])
    else:
        result = []
        is_valid = False

    context = {
        "input": input,
        "result": result,
        "is_valid": is_valid,
    }
    return render(request, 'result.html', context)