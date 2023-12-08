from .models import graph

def search_all_in_class(class_keyword):
    if class_keyword == "matches":
        result = graph.query(
            """
            select distinct ?iri (substr(str(?iri), 22) as ?label) where {
            ?iri :team ?team.
            } 
            order by ?label
            """
        )
    else:
        properties = {
            "cities": "city",
            "players": "player_of_match",
            "teams": "team",
            "umpire": "umpires",
            "venues": "venue",
        }
        result = graph.query(
            """
            select distinct ?iri ?label where {
            ?match :%s ?iri.
            ?iri rdfs:label ?label.
            } 
            order by ?label
            """
        ) % (properties[class_keyword])
    return result

def search_identifier(identifier):
    identifier = identifier.lower()
    result = graph.query(
        """
        select * where {
        {
        select distinct ?iri ?label where {
        ?iri rdfs:label ?label.
        filter(contains(lcase(?label), "%s"))
        }
        } union {
        select distinct ?iri (substr(str(?iri), 22) as ?label) where {
        ?iri :team ?team.
        filter(contains(lcase(substr(str(?iri), 22)), "%s"))
        }
        }
        }
        order by ?label
        """ % (identifier, identifier)
    )
    return result

def get_iri_details(iri):
    # find more efficient query
    iri_properties = graph.query(
        """
        select distinct ?property ?iri ?label where {
        ?object ?property ?iri.
        filter(str(?object)='%s')
        ?iri rdfs:label ?label.
        }
        order by ?property
        """ % (iri)
    )
    # find more efficient query
    literal_properties = graph.query(
        """
        select distinct ?property ?literal where {
        ?object ?property ?literal.
        filter(str(?object)='%s')
        filter(isliteral(?literal))
        }
        order by ?property
        """ % (iri)
    )
    return iri_properties, literal_properties