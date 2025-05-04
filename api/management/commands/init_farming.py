from django.core.management.base import BaseCommand

from api.models import Planet
from time import sleep

STEEL_RATIO, GOLD_RATIO, WATER_RATIO = .8, .3, .6


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('Mining farm started')
        while True:
            planets = Planet.objects.all()
            for planet in planets:
                planet.water += WATER_RATIO * planet.water_farm_lv
                planet.steel += STEEL_RATIO * planet.steel_mine_lv
                planet.gold += GOLD_RATIO * planet.gold_mine_lv
                planet.save()
                print(f'Updated planet {planet.name} [{planet.galaxy}, {planet.solar_system}, {planet.position}] | S:{planet.steel} G:{planet.gold} W: {planet.water}')
            sleep(1.5)
