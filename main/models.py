from django.db import models
from rdflib import Graph

graph = Graph()
graph.parse("cricket.ttl")

def test_query():
    queries = graph.query(
        """
        SELECT ?result
        WHERE {
        ?match :result ?result
        }
        LIMIT 3
        """
    )

    for row in queries:
        print(row.result)
    return queries