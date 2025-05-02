from django.core.management.base import BaseCommand
from redis import Redis
from api.models import Mission, Planet
from time import sleep
from datetime import datetime
import pytz

utc=pytz.UTC

class Command(BaseCommand):
    def add_arguments(self, planet_id):
        planet_id.add_argument('--planet_id', type=int)
        ...

    def handle(self, *args, **options):
        while True:
            
            r = Redis(host='104.237.1.145', port=6379, db=0, decode_responses=True)
            for key in r.keys():
                if not key.startswith('mission'):
                    continue
                mission_id = r.get(key)
                print(mission_id)
                mission = Mission.objects.get(id=mission_id)
                now = datetime.now()
                now = utc.localize(now)

                arrival_dt = mission.arrival_datetime
                return_dt = mission.return_datetime
                print(mission.fleet.all())

                if mission.state == 'returning':
                    if now < return_dt:
                        print(f'Returning to planet at {str(return_dt)})')
                        continue
                    else:
                        print('Returned home')
                        mission.success = True
                        mission.save()
                        planet = Planet.objects.get(galaxy=mission.origin_galaxy, solar_system=mission.origin_solar_system, position=mission.origin_position)
                        print(planet)
                        for ship in mission.fleet.all():
                            planet.fleet.add(ship)
                            planet.save()

                        planet.steel += mission.steel
                        planet.gold += mission.gold
                        planet.water += mission.water

                        planet.save()
                        r.delete(key)

                        print(mission.report)
                        continue
                if mission.retreat:
                    mission.state = 'returning'
                    mission.report = 'mission retreatead'
                    mission.save()
                    continue

                if now < arrival_dt:
                    print(f'Reaching destination at {str(arrival_dt)} {str(arrival_dt - now)}')

                else:
                    print('Battle')

                    max_storage = sum([ship.cargo_space for ship in mission.fleet.all()])
                    target_planet = Planet.objects.get(galaxy=mission.target_galaxy, solar_system=mission.target_solar_system, position=mission.target_position)
                    
                    loot_steel = int(max_storage / 3)
                    loot_gold = int(max_storage / 3)
                    loot_water = int(max_storage / 3)

                    target_planet.steel -= loot_steel
                    target_planet.gold -= loot_gold
                    target_planet.water -= loot_water

                    mission.steel += loot_steel
                    mission.gold += loot_gold
                    mission.water += loot_water

                    mission.success = True
                    mission.save()
                    target_planet.save()

                    mission.report = f'Reached target planet at [{target_planet.galaxy}, {target_planet.solar_system}, {target_planet.position}] and looted {loot_steel} steel, {loot_water} water and {loot_gold} gold'

                if mission.success:
                    mission.state = 'returning'
                    mission.save()

