import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        phone_objects = Phone.objects.all()

        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        # print('csv file:', phones, '\n')
        for phone in phones:
            # print(f'phone: {phone}, \n')
            # print('phone_name:', phone['name'])
            Phone.objects.create(id=phone['id'],
                                 name=phone['name'],
                                 image=phone['image'],
                                 price=phone['price'],
                                 release_date=phone['release_date'],
                                 lte_exists=phone['lte_exists'],
                                 )

# python manage.py import_phones

