from django.core.management.base import BaseCommand
from redis import Redis
from api.models import Mission, Planet, Ship
from api.battle import Battle
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
                mission = Mission.objects.get(id=mission_id)
                now = datetime.now()
                now = utc.localize(now)

                arrival_dt = mission.arrival_datetime
                return_dt = mission.return_datetime

                if mission.state == 'returning':
                    if now < return_dt:
                        print(f'[{mission.state}] Returning to planet at {str(return_dt)})')
                        continue
                    else:
                        print('Returned home')
                        mission.success = True
                        mission.state = 'completed'
                        mission.save()
                        planet = Planet.objects.get(galaxy=mission.origin_galaxy, solar_system=mission.origin_solar_system, position=mission.origin_position)
                        print(planet)
                        for ship in mission.fleet.all():
                            planet.fleet.add(ship)
                            mission.fleet.remove(ship)
                            planet.save()

                        planet.steel += mission.steel
                        planet.gold += mission.gold
                        planet.water += mission.water

                        planet.save()
                        print(mission.report)
                        r.delete(key)
                        continue

                if mission.retreat:
                    mission.state = 'returning'
                    mission.report = 'mission retreatead'
                    print(mission.report)
                    mission.save()
                    continue

                if now < arrival_dt:
                    print(f'[{mission.state}] Reaching destination at {str(arrival_dt)} {str(arrival_dt - now)}')

                else:
                    target_planet = Planet.objects.get(galaxy=mission.target_galaxy, solar_system=mission.target_solar_system, position=mission.target_position)

                    
                    if target_planet.fleet.count() > 0:
                        battle = Battle(mission.fleet.all(), target_planet.fleet.all())
                        result = battle.battle()

                        for ship_id in result['destroyed_ship_ids']:
                            try:
                                ship = Ship.objects.get(id=ship_id)
                                ship.delete()
                            except Exception as error:
                                print('++'*15)
                                print(str(error))
                                print('++'*15)
                        # mission.fleet.set(result['attacker_remaining_fleet'])
                        # target_planet.fleet.set(result['defender_remaining_fleet'])

                        max_storage = sum([ship.cargo_space for ship in mission.fleet.all()])
                        if result['battle_result'] == 'ATTACKER_WINS':
                            loot_steel = int(max_storage / 3)
                            loot_gold = int(max_storage / 3)
                            loot_water = int(max_storage / 3)

                            target_planet.steel -= loot_steel
                            target_planet.gold -= loot_gold
                            target_planet.water -= loot_water

                            mission.steel += loot_steel
                            mission.gold += loot_gold
                            mission.water += loot_water
                            mission.state = 'returning'
                            mission.success = True
                            mission.report = f'Reached target planet at [{target_planet.galaxy}, {target_planet.solar_system}, {target_planet.position}] and looted {loot_steel} steel, {loot_water} water and {loot_gold} gold' + ' '.join(f'\n{k}: {v}' for k, v in result.items())
                            mission.save()
                            target_planet.save()
                            

                        elif result['battle_result'] == 'DEFENDER_WINS':
                            mission.state='returning'
                            mission.success = False
                            mission.report = str(result)
                            mission.save()

                        elif result['battle_result'] == 'NO_SURVIVORS':
                            mission.state='returning'
                            mission.success = False
                            mission.report = ''.join(f'\n{k}: {v}' for k, v in result.items())
                            mission.save()

                        elif result['battle_result'] == 'DRAW':
                            mission.state='returning'
                            mission.success = False
                            mission.report = ''.join(f'\n{k}: {v}' for k, v in result.items())
                            mission.save()
                            continue
                    else:
                        max_storage = sum([ship.cargo_space for ship in mission.fleet.all()])
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
                        mission.state='returning'
                        mission.report = f'Reached target planet at [{target_planet.galaxy}, {target_planet.solar_system}, {target_planet.position}] and looted {loot_steel} steel, {loot_water} water and {loot_gold} gold'
                        mission.save()
                        target_planet.save()

                if mission.success:
                    mission.state = 'returning'
                    mission.save()

            r.close()