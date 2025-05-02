from django.core.management.base import BaseCommand

from api.models import Universe, Galaxy, SolarSystem
from time import sleep


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('--name', type=int)
        ...

    def handle(self, *args, **options):
        print('The result of a random atom collision was a big explosion that created a universe...')
        universe = Universe.objects.create()


        for gi in range(9):
            galaxy = Galaxy.objects.create(id=gi+1)
            galaxy.save()

            for ss in range(500):
                solar_system = SolarSystem.objects.create(galaxy_position=ss+1, galaxy=galaxy)
                solar_system.save()
        
            print('Look, a galaxy with 500 solar systems appear to be emerged from the explosion...')
            universe.galaxies.add(galaxy)
            universe.save()
        print(f'A total of {universe.galaxies.count()} galaxies where created from this Big Bang')
