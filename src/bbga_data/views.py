# from django.shortcuts import render

# Create your views here.
from datetime import date

from django_filters.rest_framework import filters
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from datapunt_api import rest
from . import models
from . import serializers


@api_view(['GET'])
def meta_groepen(_request):
    """
    Lijst van groepen
    """

    queryset = models.Meta.objects.values('groep').distinct().extra(
        order_by=['groep'])

    data = {
        'groepen': sorted([r['groep'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_themas(_request):
    """
    Lijst met gebruikte thema's
    """
    queryset = models.Meta.objects.values('thema').distinct().extra(
        order_by=['thema'])
    data = {
        'themas': sorted([r['thema'] for r in queryset])
    }
    return Response(data)


@api_view(['GET'])
def meta_variabelen(_request):
    """
    Lijst met gebruikte variabelen
    """
    queryset = models.Meta.objects.values('variabele').distinct().extra(
        order_by=['variabele'])

    data = {
        'variabelen': [r['variabele'] for r in queryset]
    }
    return Response(data)


@api_view(['GET'])
def meta_gebiedcodes(_request):
    """
    Lijst met gebruikte gebiedscodes
    """
    queryset = models.Cijfers.objects.values('gebiedcode15').distinct().extra(
        order_by=['gebiedcode15'])

    data = {
        'variabelen': [r['gebiedcode15'] for r in queryset]
    }
    return Response(data)


class MetaViewSet(rest.AtlasViewSet):
    """
    Metadata

    Lijst met alle Meta-data gebruikt in BBGA
    """

    queryset = models.Meta.objects.all().order_by('id')
    serializer_class = serializers.Meta
    serializer_detail_class = serializers.MetaDetail

    filter_fields = ('id', 'thema', 'variabele', 'groep', 'bron')


class CijfersFilter(FilterSet):
    """
    Filter nummeraanduidingkjes
    """

    jaar = filters.CharFilter(method='filter_jaar')

    class Meta:
        model = models.Cijfers
        fields = [
            'gebiedcode15',
            'variabele',
            # must be last!!
            'jaar',
        ]

    def filter_jaar(self, queryset, _name, value):
        """ TODO: Why not select the MAX year rather than loop starting at the
                  current year?
        """
        if value == 'latest':
            # find value for this year
            year = date.today().year
            qs = queryset.filter(jaar=year)
            # check if we have data or go
            # up to 3 years back!!
            for _ in range(1, 4):
                valid = qs.count()
                if valid:
                    break
                else:
                    year -= 1
                    qs = queryset.filter(jaar=year)
            return qs

        return queryset.filter(jaar=value)


class CijfersViewSet(rest.AtlasViewSet):
    """
    Basisbestand Gebieden Amsterdam

    https://www.ois.amsterdam.nl/online-producten/basisbestand-gebieden-amsterdam

    bronhouder: OIS (Onderzoek, Informatie en Statistiek)

    bekijk de filter opties
    er kan op jaar, gebiedcode15 en variabele gefiltert worden

    voorbeeld:

    https://acc.api.data.amsterdam.nl/bbga/cijfers/?variabele=BEV12_17&gebiedcode15=STAD&jaar=2015

    """

    queryset = models.Cijfers.objects.all().order_by('id')
    serializer_class = serializers.Cijfers
    serializer_detail_class = serializers.CijferDetail
    filter_class = CijfersFilter

    ordering_fields = ('jaar', 'buurt', 'variabele')
    ordering = ('-jaar', 'buurt', 'variabele')