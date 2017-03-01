
from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import Play


def graph(request):
    return render(request, 'd3ex/graph.html')


def play_count_by_month(request):
    data = Play.objects.all() \
        .extra(
            select={
                'month': connections[Play.objects.db].ops.date_trunc_sql('month', 'date')
            }
        ) \
        .values('month') \
        .annotate(count_items=Count('id'))

    for instance in data:
        print(instance)

    return JsonResponse(list(data), safe=False)