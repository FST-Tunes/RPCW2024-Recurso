import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD, OWL
import re



# Definir o namespace da namespacelogia
BOOKS = Namespace("http://rpcw.di.uminho.pt/2024/untitled-ontology-19/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Criar um novo grafo RDF
g = Graph()
g.bind("", BOOKS)
g.bind("rdfs", RDFS)
g.bind("owl", OWL)

g.parse("books_base.ttl", format="turtle")

with open('clean_dataset.json') as f:
    data = json.load(f)

for entry in data:
    book_id = re.sub(r'\W+', '_', entry['bookId']).lower()
    book_uri = BOOKS[book_id]

    g.add((book_uri, RDF.type, BOOKS.Book))
    g.add((book_uri, BOOKS.bookId, Literal(entry['bookId'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.title, Literal(entry['title'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.author, Literal(entry['author'], datatype=XSD.string)))

    for genre in eval(entry['genres']):
        g.add((book_uri, BOOKS.genres, Literal(genre)))

    for character in eval(entry['characters']):
        g.add((book_uri, BOOKS.characters, Literal(character)))



g.serialize(destination='books.ttl', format='turtle')
