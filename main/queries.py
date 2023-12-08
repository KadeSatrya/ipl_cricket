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
    allow_no_result = \
        "player_label" not in bindings.keys() and \
        "winner_label" not in bindings.keys()
    if allow_no_result:
        optional_start = "OPTIONAL {"
        optional_end = "}"
    else:
        optional_start = ""
        optional_end = ""
    query_string = \
        """
        select distinct ?iri (substr(str(?iri), 22) as ?label) ?team1_label ?team2_label ?date_literal ?winner_label where {
        ?iri :city ?city.
        ?city rdfs:label ?city_label.
        ?iri :date ?date_literal.
        filter(?date_literal >= ?date_starts && ?date_literal <= ?date_ends)
        ?iri :dl_applied ?dl_literal.
        %s
        ?iri :player_of_match ?player.
        ?player rdfs:label ?player_label.
        %s
        ?iri :result ?result_literal.
        ?iri :season ?season_literal.
        ?iri :team ?team1.
        ?team1 rdfs:label ?team1_label.
        ?iri :team ?team2.
        ?team2 rdfs:label ?team2_label.
        filter(?team1_label < ?team2_label)
        ?iri :toss_decision ?toss_decision_literal.
        ?iri :toss_winner ?toss_winner.
        ?toss_winner rdfs:label ?toss_winner_label.
        ?iri :umpire ?umpire1.
        ?umpire1 rdfs:label ?umpire1_label.
        ?iri :umpire ?umpire2.
        ?umpire2 rdfs:label ?umpire2_label.
        ?iri :venue ?venue.
        ?venue rdfs:label ?venue_label.
        ?iri :win_by_amount ?win_by_amount_literal.
        ?iri :win_by_type ?win_by_type_literal.
        %s
        ?iri :winner ?winner.
        ?winner rdfs:label ?winner_label.
        %s
        } order by ?date_literal
        """ % (optional_start, optional_end, optional_start, optional_end)
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