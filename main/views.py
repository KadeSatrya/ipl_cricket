from django.shortcuts import redirect, render
from rdflib import Literal, URIRef
from rdflib.namespace import XSD
from .queries import *

properties = {
    "cities": "https://appname.here/data#city",
    "players": "https://appname.here/data#player_of_match",
    "teams": "https://appname.here/data#team",
    "umpire": "https://appname.here/data#umpire",
    "venues": "https://appname.here/data#venue",
}

def show_search(request):
    context = {}
    for property in properties.keys():
        context[property] = search_all_in_class({"property": URIRef(properties[property])})
    return render(request, 'search.html', context)

def show_general_result(request):
    input = request.GET.get("query")
    if input == None or input == "":
        return redirect("main:show_search")
    if len(input.split()) == 1 and input == "matches":
        result = search_all_in_matches()
    elif len(input.split()) == 1 and input in properties.keys():
        bindings = {"property": URIRef(properties[input])}
        result = search_all_in_class(bindings) 
    else:
        bindings = {"identifier": Literal(input.lower())}
        result = search_identifier(bindings)
    context = {
        "input": input,
        "result": result,
        "is_valid": True,
    }
    return render(request, 'result.html', context)

def show_infobox(request):
    iri = request.GET.get("iri")
    label = request.GET.get("label")
    bindings = {"object": URIRef(iri)}
    iri_properties, literal_properties = get_iri_details(bindings)
    is_valid = True
    if len(iri_properties) == 0 and len(literal_properties) == 0:
        is_valid = False
    context = {
        "iri": iri,
        "label": label,
        "iri_properties": iri_properties,
        "literal_properties": literal_properties,
        "is_valid": is_valid,
    }
    return render(request, 'infobox.html', context)

def show_detailed_result(request):
    city = request.GET.get("city")
    date = request.GET.get("date")
    dl_applied = request.GET.get("dl_applied")
    player = request.GET.get("player")
    try:
        bindings = {}
        if city != "" and city != None:
            bindings["city_label"] = Literal(city)
        if date != "" and date != None:
            bindings["date_literal"] = Literal(date, datatype=XSD.date)
        if dl_applied != None:
            bindings["dl_literal"] = Literal(dl_applied, datatype=XSD.boolean)
        if player != "" and player != None:
            bindings["player_label"] = Literal(player)
        result = search_detailed_matches(bindings)
        is_valid = True
    except:
        result = []
        is_valid = False
    context = {
        "input": "",
        "result": result,
        "is_valid": is_valid,
    }
    return render(request, 'result.html', context)