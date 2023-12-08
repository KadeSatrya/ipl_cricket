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
    result = request.GET.get("result")
    season = request.GET.get("season")
    team1 = request.GET.get("team1")
    team2 = request.GET.get("team2")
    toss_decision = request.GET.get("toss_decision")
    toss_winner = request.GET.get("toss_winner")
    umpire1 = request.GET.get("umpire1")
    umpire2 = request.GET.get("umpire2")
    venue = request.GET.get("venue")
    win_by_amount = request.GET.get("win_by_amount")
    win_by_type = request.GET.get("win_by_type")
    winner = request.GET.get("winner")

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
        if result != "" and result != None:
            bindings["result_literal"] = Literal(result)
        if season != "" and season != None:
            bindings["season_literal"] = Literal(season, datatype=XSD.gYear)
        if team1 != "" and team1 != None:
            bindings["team1_label"] = Literal(team1)
        if team2 != "" and team2 != None:
            bindings["team2_label"] = Literal(team2)
        if toss_decision != None:
            bindings["toss_decision_literal"] = Literal(toss_decision)
        if toss_winner != "" and toss_winner != None:
            bindings["toss_winner_label"] = Literal(toss_winner)
        if umpire1 != "" and umpire1 != None:
            bindings["umpire1_label"] = Literal(umpire1)
        if umpire2 != "" and umpire2 != None:
            bindings["umpire2_label"] = Literal(umpire2)
        if venue != "" and venue != None:
            bindings["venue_label"] = Literal(venue)
        if win_by_amount != "" and win_by_amount != None:
            bindings["win_by_amount_literal"] = Literal(win_by_amount, datatype=XSD.int)
        if win_by_type != None:
            bindings["win_by_type_literal"] = Literal(win_by_type)
        if winner != "" and winner != None:
            bindings["winner_label"] = Literal(winner)

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