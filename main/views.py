from django.shortcuts import render
from rdflib import Literal, URIRef
from rdflib.namespace import XSD
from .queries import *
from .remote_queries import *
from datetime import datetime

properties = {
    "cities": "https://appname.here/data#city",
    "players": "https://appname.here/data#player_of_match",
    "teams": "https://appname.here/data#team",
    "umpires": "https://appname.here/data#umpire",
    "venues": "https://appname.here/data#venue",
}

default_date_starts = Literal("2000-01-01", datatype=XSD.date)
default_date_ends = Literal("2099-12-31", datatype=XSD.date)

def show_search(request):
    context = {}
    for property in properties.keys():
        context[property] = search_all_in_class({"property": URIRef(properties[property])})
    return render(request, 'search.html', context)

def show_infobox(request):
    iri = request.GET.get("iri")
    label = request.GET.get("label")
    bindings = {"object": URIRef(iri)}
    iri_properties, literal_properties = get_iri_details(bindings)
    is_valid = True
    if len(iri_properties) == 0 and len(literal_properties) == 0:
        is_valid = False

    properties = {}
    for row in iri_properties:
        property_name = str(row.property).replace(" ", "_").title()
        property_value = str(row.label)
        if property_name in properties.keys():
            first_value = properties.pop(property_name)
            properties[f"{property_name} 1"] = first_value
            properties[f"{property_name} 2"] = property_value
        else:
            properties[property_name] = property_value
    for row in literal_properties:
        property_name = str(row.property).replace(" ", "_").title()
        property_value = str(row.label)
        properties[property_name] = property_value
    properties = {key.replace(' ', '_'): value for key, value in properties.items()}

    context = {
        "iri": iri,
        "label": label,
        "properties": properties,
        "is_valid": is_valid,
    }
    print(properties)
    return render(request, 'infobox.html', context)

def show_detailed_result(request):
    city = request.GET.get("city")
    date_starts = request.GET.get("date_starts")
    date_ends = request.GET.get("date_ends")
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
        if date_starts != "" and date_starts != None:
            bindings["date_starts"] = Literal(date_starts, datatype=XSD.date)
        else:
            bindings["date_starts"] = default_date_starts
        if date_ends != "" and date_ends != None:
            bindings["date_ends"] = Literal(date_ends, datatype=XSD.date)
        else:
            bindings["date_ends"] = default_date_ends
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

def show_player_detail(request, label):
    context = {'is_valid': False, 'label': label} 
    query_result = get_player_detail_by_label(label)
    if query_result != None:
        player_iri = query_result['player_iri']['value']
        name = query_result['name']['value']
        gender = query_result['gender']['value']
        citizenship = query_result['citizenship']['value']
        birthdate = query_result['birthdate']['value']
        birthplace = query_result['birthplace']['value']
        country_name = query_result['country_name']['value']
        birthplace_name = query_result['birthplace_name']['value']
        teams = [iri.strip() for iri in query_result['teams']['value'].split(',')]
        team_names = [name.strip() for name in query_result['team_names']['value'].split(',')]
        
        team_list = zip(teams, team_names)
        
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        datetime_object = datetime.strptime(birthdate, date_format)
        birthdate = datetime_object.strftime('%d-%m-%Y')
        
        context = {
            'player_iri': player_iri,
            'name': name,
            'gender': gender,
            'nationality': citizenship,
            'birthdate': birthdate,
            'birthplace': birthplace,
            'country_name': country_name,
            'birthplace_name': birthplace_name,
            'team_list': team_list,
            'is_valid': True,
            'label': label
        }
        
    return render(request, "player_detail.html", context)

def show_team_detail(request, label):
    context = {'is_valid': False, 'label': label} 
    query_result = get_team_detail_by_label(label)
    if query_result != None:
        team_iri = query_result['team_iri']['value']
        captain_iri = query_result['captain']['value']
        league_iri = query_result['league']['value']
        inception = query_result['inception']['value']
        team_name = query_result['name']['value']
        league_name = query_result['league_name']['value']
        captain_name = query_result['captain_name']['value']

        date_format = '%Y-%m-%dT%H:%M:%SZ'
        datetime_object = datetime.strptime(inception, date_format)
        inception = datetime_object.strftime('%Y')
        context = {
            'team_iri': team_iri,
            'captain_iri': captain_iri,
            'league_iri': league_iri,
            'inception': inception,
            'team_name': team_name,
            'league_name': league_name,
            'captain_name': captain_name,
            'is_valid': True,
            'label': label
        }
    return render(request, "team_detail.html", context)

def show_venue_detail(request, label):
    context = {'is_valid': False, 'label': label} 
    query_result = get_venue_detail_by_label(label)
    if query_result != None:
        venue_iri = query_result['venue_iri']['value']
        opening_date = query_result['opening_date']['value']
        location_iri = query_result['location']['value']
        country_iri = query_result['country']['value']
        venue_name = query_result['name']['value']
        country_name = query_result['country_name']['value']
        location_name = query_result['location_name']['value']

        date_format = '%Y-%m-%dT%H:%M:%SZ'
        datetime_object = datetime.strptime(opening_date, date_format)
        opening_date = datetime_object.strftime('%Y')
        
        context = {
            'venue_iri': venue_iri,
            'opening_date': opening_date,
            'location_iri': location_iri,
            'country_iri': country_iri,
            'venue_name': venue_name,
            'country_name': country_name,
            'location_name': location_name,
            'is_valid': True,
            'label': label
        }    
    return render(request, "venue_detail.html", context)