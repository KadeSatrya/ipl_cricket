from django.shortcuts import redirect, render
from .queries import *

classes = ["cities", "matches", "players", "teams", "umpires", "venues"]

def show_search(request):
    context = {
        "cities": search_all_in_class("cities")
    }
    return render(request, 'search.html', context)

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

def show_infobox(request):
    iri = request.GET.get("iri")
    label = request.GET.get("label")
    iri_properties, literal_properties = get_iri_details(iri)
    context = {
        "iri": iri,
        "label": label,
        "iri_properties": iri_properties,
        "literal_properties": literal_properties,
    }
    return render(request, 'infobox.html', context)