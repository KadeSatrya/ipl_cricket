import rdflib
from rdflib.namespace import XSD
from .models import graph

def search_all_in_matches():
    result = graph.query(
        """
        select distinct ?iri (substr(str(?iri), 22) as ?label) where {
        ?iri :team ?team.
        } 
        order by ?label
        """
    )
    return result

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
    result = graph.query(
        """
        select ?iri (substr(str(?iri), 22) as ?label) where {
        ?iri :city ?city.
        ?city rdfs:label ?city_label.
        ?iri :date ?date_literal.
        ?iri :dl_applied ?dl_literal.
        ?iri :player_of_match ?player.
        ?player rdfs:label ?player_label.
        } order by ?label
        """
    , initBindings=bindings)
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