from .models import graph

def search_all_in_class(class_keyword):
    if class_keyword == "cities":
        result = graph.query(
            """
            select distinct ?label where {
            ?match :city ?city.
            ?city rdfs:label ?label.
            } 
            order by ?team_name
            """
        )
    elif class_keyword == "matches":
        result = graph.query(
            """
            select distinct (substr(str(?match), 22) as ?label) where {
            ?match :team ?team.
            } 
            order by ?label
            """
        )
    elif class_keyword == "players":
        result = graph.query(
            """
            select distinct ?label where {
            ?match :player_of_match ?player.
            ?player rdfs:label ?label.
            } 
            order by ?label
            """
        )
    elif class_keyword == "seasons":
        result = graph.query(
            """
            select distinct ?label where {
            ?match :season ?label.
            } 
            order by ?label
            """
        )
    elif class_keyword == "teams":
        result = graph.query(
            """
            select distinct ?label where {
            ?match :team ?team.
            ?team rdfs:label ?label.
            } 
            order by ?label
            """
        )
    elif class_keyword == "umpires":
        result = graph.query(
            """
            select distinct ?label where {
            ?match :umpire ?umpire.
            ?umpire rdfs:label ?label.
            } 
            order by ?label
            """
        )
    else: #  class_keyword == "venues"
        result = graph.query(
            """
            select distinct ?label where {
            ?match :venue ?venue.
            ?venue rdfs:label ?label.
            } 
            order by ?label
            """
        )
    return result

def search_identifier(identifier):
    identifier = identifier.lower()
    result = graph.query(
        """
        select * where {
        {
        select distinct ?label where {
        ?object rdfs:label ?label.
        filter(contains(lcase(?label), "%s"))
        }
        } union {
        select distinct (substr(str(?match), 22) as ?label) where {
        ?match :team ?team.
        filter(contains(lcase(substr(str(?match), 22)), "%s"))
        }
        } union {
        select distinct ?label where {
        ?match :season ?label.
        filter(contains(str(?label), "%s"))
        }
        }
        }
        order by ?label
        """ % (identifier, identifier, identifier)
    )
    return result