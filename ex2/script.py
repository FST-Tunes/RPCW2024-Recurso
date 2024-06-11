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
    g.add((book_uri, BOOKS.series, Literal(entry['series'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.author, Literal(entry['author'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.rating, Literal(entry['rating'], datatype=XSD.float)))
    g.add((book_uri, BOOKS.description, Literal(entry['description'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.language, Literal(entry['language'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.isbn, Literal(entry['isbn'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.bookFormat, Literal(entry['bookFormat'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.edition, Literal(entry['edition'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.pages, Literal(entry['pages'], datatype=XSD.int)))
    g.add((book_uri, BOOKS.publisher, Literal(entry['publisher'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.publishDate, Literal(entry['publishDate'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.firstPublishDate, Literal(entry['firstPublishDate'], datatype=XSD.string)))
    g.add((book_uri, BOOKS.numRatings, Literal(entry['numRatings'], datatype=XSD.int)))
    g.add((book_uri, BOOKS.likedPercent, Literal(entry['likedPercent'], datatype=XSD.int)))
    g.add((book_uri, BOOKS.coverImg, Literal(entry['coverImg'], datatype=XSD.string)))

    for genre in eval(entry['genres']):
        g.add((book_uri, BOOKS.genres, Literal(genre)))

    for character in eval(entry['characters']):
        g.add((book_uri, BOOKS.characters, Literal(character)))

    for award in eval(entry['awards']):
        g.add((book_uri, BOOKS.awards, Literal(award)))

    for i, rating in enumerate(eval(entry['ratingsByStars']), start=1):
        g.add((book_uri, BOOKS[f'ratingsByStars_{i}'], Literal(rating, datatype=XSD.integer)))

    for setting in eval(entry['setting']):
        g.add((book_uri, BOOKS.setting, Literal(setting)))


g.serialize(destination='books.ttl', format='turtle')
