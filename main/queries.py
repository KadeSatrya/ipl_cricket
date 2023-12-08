from .models import graph

def search_all_in_class(bindings):
    result = graph.query(
        """
        select distinct ?iri ?label where {
        ?match ?property ?iri.
        ?iri rdfs:label ?label.
        } 
        order by ?label
        """
    , initBindings=bindings)
    return result

def search_identifier(bindings):
    result = graph.query(
        """
        select * where {
        {
        select distinct ?iri ?label where {
        ?iri rdfs:label ?label.
        filter(contains(lcase(?label), ?identifier))
        }
        } union {
        select distinct ?iri (substr(str(?iri), 22) as ?label) where {
        ?iri :team ?team.
        filter(contains(lcase(substr(str(?iri), 22)), ?identifier))
        }
        }
        }
        order by ?label
        """
    , initBindings=bindings)
    return result

def search_detailed_matches(bindings):
    keys = bindings.keys()
    team_query = "|| ?team2_label < ?team1_label"
    optional_start = "OPTIONAL {"
    optional_end = "}"
    additional_query = ""

    if "player_label" in keys or "winner_label" in keys:
        optional_start = ""
        optional_end = ""
    if "team1_label" not in keys and "team2_label" not in keys:
        team_query = ""
    if "city_label" in keys:
        additional_query += \
            """
            ?iri :city ?city.
            ?city rdfs:label ?city_label.
            """
    if "dl_literal" in keys:
        additional_query += \
            """
            ?iri :dl_applied ?dl_literal.
            """
    if "player_label" in keys:
        additional_query += \
            """
            ?iri :player_of_match ?player.
            ?player rdfs:label ?player_label.
            """
    if "result_literal" in keys:
        additional_query += \
            """
            ?iri :result ?result_literal.
            """
    if "season_literal" in keys:
        additional_query += \
            """
            ?iri :season ?season_literal.
            """
    if "toss_decision_literal" in keys:
        additional_query += \
            """
            ?iri :toss_decision ?toss_decision_literal.
            """
    if "toss_winner_label" in keys:
        additional_query += \
            """
            ?iri :toss_winner ?toss_winner.
            ?toss_winner rdfs:label ?toss_winner_label.
            """
    if "umpire1_label" in keys:
        additional_query += \
            """
            ?iri :umpire ?umpire1.
            ?umpire1 rdfs:label ?umpire1_label.
            """
    if "umpire2_label" in keys:
        additional_query += \
            """
            ?iri :umpire ?umpire2.
            ?umpire2 rdfs:label ?umpire2_label.
            """
    if "venue_label" in keys:
        additional_query += \
            """
            ?iri :venue ?venue.
            ?venue rdfs:label ?venue_label.
            """
    if "win_by_amount_literal" in keys:
        additional_query += \
            """
            ?iri :win_by_amount ?win_by_amount_literal.
            """
    if "win_by_type_literal" in keys:
        additional_query += \
            """
            ?iri :win_by_type ?win_by_type_literal.
            """

    query_string = \
        """
        select distinct ?iri (substr(str(?iri), 22) as ?label) ?team1_label ?team2_label ?date_literal ?winner_label where {
        ?iri :date ?date_literal.
        filter(?date_literal >= ?date_starts && ?date_literal <= ?date_ends)
        ?iri :team ?team1.
        ?team1 rdfs:label ?team1_label.
        ?iri :team ?team2.
        ?team2 rdfs:label ?team2_label.
        filter(?team1_label < ?team2_label %s)
        %s
        ?iri :winner ?winner.
        ?winner rdfs:label ?winner_label.
        %s
        %s
        } order by ?date_literal
        """ % (team_query, optional_start, optional_end, additional_query)
    
    result = graph.query(query_string, initBindings=bindings)
    return result

def get_iri_details(bindings):
    iri_properties = graph.query(
        """
        select distinct ?property ?iri ?label where {
        ?object ?property ?iri.
        ?iri rdfs:label ?label.
        }
        order by ?property
        """
    , initBindings=bindings)
    literal_properties = graph.query(
        """
        select distinct ?property ?literal where {
        ?object ?property ?literal.
        filter(isliteral(?literal))
        }
        order by ?property
        """
    , initBindings=bindings)
    return iri_properties, literal_properties