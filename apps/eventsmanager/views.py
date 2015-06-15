from .models import Event
from .serializers import EventSerializer
from rest_framework import generics
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from SPARQLWrapper import SPARQLWrapper, JSON
import json

class Base(APIView):

     def get(self, request, format=None):
        result = {
            "Events": reverse('author-list', request=request),
        }
        return Response(result)

class EventView(generics.ListCreateAPIView):
    model = Event
    serializer_class = EventSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        def validate_date(d):
            try:
                datetime.strptime(d, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        queryset = Event.objects.all()
        title = self.request.QUERY_PARAMS.get('title', None)
        start = self.request.QUERY_PARAMS.get('start', None)
        end = self.request.QUERY_PARAMS.get('end', None)
        if start and end is not None:
            if validate_date(start) and validate_date(end) is not None:
                queryset2 = queryset
                queryset = queryset.filter(Q(startEventDate__range=[start, end]) | Q(endEventDate__range=[start, end]))
                queryset = queryset | queryset2.filter(startEventDate__lte=start).filter(endEventDate__gte=end)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class EventInstanceView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer

@api_view(['GET'])
def harvest_events(request):
    start = request.QUERY_PARAMS.get('start', None)
    if start is None:
        start = "0001-01-01"
    end = request.QUERY_PARAMS.get('end', None)
    if end is None:
        end = "2099-12-31"
    keyword = request.QUERY_PARAMS.get('keyword', None)
    if keyword is None:
        keyword = ""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

        SELECT ?event ?date ?comment ?label ?startDate ?endDate {
            ?event a dbpedia-owl:Event ;
            rdfs:comment ?comment ;
            rdfs:label ?label ;
            dbpedia-owl:date ?date .
            FILTER (?date > \"""" + start + """\"^^xsd:date &&
            ?date < \"""" + end + """\"^^xsd:date &&
            langMatches(lang(?label),"en") &&
            langMatches(lang(?comment),"en") &&
            (regex(?label, \"""" + keyword + """\", "i") || regex(?comment, \"""" + keyword + """\", "i"))) .
        }
        limit 10
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    output = []
    for key in results["results"]["bindings"]:
        output.append({"title": key["label"]["value"], "description": key["comment"]["value"], "date": key["date"]["value"], "url": key["event"]["value"]})
    #Example Request: http://localhost:8000/api/v1/eventsmanager/harvestevents?start=1968-10-30&end=1980-12-31&keyword=war
    return Response(output)