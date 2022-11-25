import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    template_name = 'stations/index.html'
    bus_stations_list = list()

    with open('data-398-2018-08-30.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['Name'], "\n", row['StationName'])
            b_stations = {
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District']
            }
            bus_stations_list.append(b_stations)
    # print(bus_stations_list)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(bus_stations_list, per_page=10)
    page = paginator.get_page(page_number)
    content = page.object_list

    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    # bus_station_url = settings.BUS_STATION_CSV
    # print(bus_station_url)
    context = {
        'bus_stations': content,
        'page': page
    }
    return render(request, template_name, context)
