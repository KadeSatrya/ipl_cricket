from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

def get_player_detail_by_label(label):
    regex_pattern = r'\\.?\\s*'.join(label.lower())
    query = f"""
    SELECT ?player_iri ?name ?gender ?citizenship ?country_name ?birthdate ?birthplace ?birthplace_name (GROUP_CONCAT(DISTINCT ?team; SEPARATOR=", ") AS ?teams) (GROUP_CONCAT(DISTINCT ?team_name; SEPARATOR=", ") AS ?team_names)
    WHERE {{
      ?player_iri rdfs:label ?name.
      ?player_iri wdt:P106 wd:Q12299841.
      ?player_iri wdt:P21 ?gender_iri.
      ?gender_iri rdfs:label ?gender.
      ?player_iri wdt:P27 ?citizenship.
      ?citizenship rdfs:label ?country_name.
      ?player_iri wdt:P569 ?birthdate.
      ?player_iri wdt:P19 ?birthplace.
      ?birthplace rdfs:label ?birthplace_name.
      ?player_iri wdt:P54 ?team.
      ?team rdfs:label ?team_name.
    FILTER(REGEX(?name, "{regex_pattern}", "i"))
    FILTER(LANG(?name) = "en")
    FILTER(LANG(?country_name) = "en")
    FILTER(LANG(?birthplace_name) = "en")
    FILTER(LANG(?team_name) = "en")
    FILTER(LANG(?gender) = "en")
    }}
    GROUP BY ?player_iri ?name ?gender ?citizenship ?birthdate ?birthplace ?country_name ?birthplace_name
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("User-Agent", "Mozilla/5.0")
    results = sparql.query().convert()
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]
    else:
        return None
    
def get_team_detail_by_label(label):
    regex_pattern = r'\\.?\\s*'.join(label.lower())
    query = f"""
    SELECT ?team_iri ?name ?inception ?league ?league_name ?captain ?captain_name
    WHERE {{
      ?team_iri wdt:P641 wd:Q5375.
      ?team_iri rdfs:label ?name.
      ?team_iri wdt:P571 ?inception.
      ?team_iri wdt:P118 ?league.
      ?league rdfs:label ?league_name.
      OPTIONAL {{ 
        ?team_iri wdt:P634 ?captain.
        OPTIONAL {{ ?captain rdfs:label ?captain_name. FILTER(LANG(?captain_name) = "en") }}
        }}
      FILTER(REGEX(?name, "{regex_pattern}", "i"))
      FILTER(LANG(?name) = "en")
      FILTER(LANG(?league_name) = "en")
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("User-Agent", "Mozilla/5.0")
    results = sparql.query().convert()    
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]
    else:
        return None
    
def get_venue_detail_by_label(label):
    regex_pattern = r'\\.?\\s*'.join(label.lower())
    query = f"""
    SELECT ?venue_iri ?name ?opening_date ?country ?country_name ?location ?location_name
    WHERE {{
      ?venue_iri wdt:P31 wd:Q682943.
      ?venue_iri rdfs:label ?name.
      OPTIONAL {{?venue_iri wdt:P1619 ?opening_date.}}
      ?venue_iri wdt:P17 ?country.
      ?country rdfs:label ?country_name.
      OPTIONAL {{ 
        ?venue_iri wdt:P276 ?location.
        OPTIONAL {{ ?location rdfs:label ?location_name. FILTER(LANG(?location_name) = "en")}}
        }}
      FILTER(REGEX(?name, "{regex_pattern}", "i"))
      FILTER(LANG(?name) = "en")
      FILTER(LANG(?country_name) = "en")
      
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("User-Agent", "Mozilla/5.0")
    results = sparql.query().convert()
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]
    else:
        return None