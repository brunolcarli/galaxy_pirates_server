"""
- [2025]
- Main API schema containing the ojects and queries.
- @beelzebruno
- *.beelzeware.dev
"""
from collections import Counter
from datetime import datetime, timedelta
from random import randint, choice
from redis import Redis
import numpy as np
import graphene
from django.conf import settings
from api.models import Universe, Galaxy, Planet, Ship, Mission, UserModel, Inbox, SolarSystem
from api.util import BuildingResourceRatio
from api.ships import ships
import graphql_jwt
from api.user_auth import access_required



class ResourceCostType(graphene.ObjectType):
    steel = graphene.Int()
    water = graphene.Int()
    gold = graphene.Int()


class RequirementsType(graphene.ObjectType):
    military_power = graphene.Int()
    shield_power = graphene.Int()
    engine_power = graphene.Int()


class ShipType(graphene.ObjectType):
    id = graphene.Int()
    index = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    offense_power = graphene.Int()
    shield_power = graphene.Int()
    cargo_space = graphene.Int()
    speed = graphene.Int()
    cost = graphene.Field(ResourceCostType)
    build_time = graphene.Int()
    requirements = graphene.Field(RequirementsType)
    integrity = graphene.Int()

    def resolve_index(self, info, **kwargs):
        return self.id


class MissionType(graphene.ObjectType):
    kind = graphene.String()
    origin_coords = graphene.List(graphene.Int)
    target_coords = graphene.List(graphene.Int)
    origin_galaxy = graphene.Int()
    origin_solar_system = graphene.Int()
    origin_position = graphene.Int()
    target_galaxy = graphene.Int()
    target_solar_system = graphene.Int()
    target_position = graphene.Int()
    speed = graphene.Int()
    fleet = graphene.List(ShipType)
    steel = graphene.Int()
    water = graphene.Int()
    gold = graphene.Int()
    retreat = graphene.Boolean()
    report = graphene.String()
    launch_datetime = graphene.DateTime()
    arrival_datetime = graphene.DateTime()
    return_datetime = graphene.DateTime()
    distance = graphene.Int()
    success = graphene.Boolean()
    travel_time = graphene.Int()
    state = graphene.String()

    def resolve_fleet(self, info, **kwargs):
        return self.fleet.all()

    def resolve_origin_coords(self, info, **kwargs):
        return [self.origin_galaxy, self.origin_solar_system, self.origin_position]

    def resolve_target_coords(self, info, **kwargs):
        return [self.target_galaxy, self.target_solar_system, self.target_position]


class PlanetType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    size = graphene.Int()
    galaxy = graphene.Int()
    solar_system = graphene.Int()
    position = graphene.Int()
    water = graphene.Int()
    steel = graphene.Int()
    gold = graphene.Int()
    temperature = graphene.Float()
    water_farm_lv = graphene.Int()
    gold_mine_lv = graphene.Int()
    steel_mine_lv = graphene.Int()
    fields_used = graphene.Int()
    military_power = graphene.Int()
    engine_power = graphene.Int()
    shield_power = graphene.Int()
    fleet = graphene.List(ShipType)

    def resolve_fleet(self, info, **kwargs):
        return self.fleet.all()


class SolarSystemType(graphene.ObjectType):
    galaxy_position = graphene.Int()
    position_1 = graphene.Field(PlanetType)
    position_2 = graphene.Field(PlanetType)
    position_3 = graphene.Field(PlanetType)
    position_4 = graphene.Field(PlanetType)
    position_5 = graphene.Field(PlanetType)
    position_6 = graphene.Field(PlanetType)
    position_7 = graphene.Field(PlanetType)
    position_8 = graphene.Field(PlanetType)
    position_9 = graphene.Field(PlanetType)
    position_10 = graphene.Field(PlanetType)
    position_11 = graphene.Field(PlanetType)
    position_12 = graphene.Field(PlanetType)
    position_13 = graphene.Field(PlanetType)
    position_14 = graphene.Field(PlanetType)
    position_15 = graphene.Field(PlanetType)



class GalaxyType(graphene.ObjectType):
    id = graphene.ID()
    solar_systems = graphene.List(SolarSystemType)

    def resolve_solar_systems(self, info, **kwargs):
        return self.solarsystem_set.all()


class UniverseType(graphene.ObjectType):
    galaxies = graphene.List(GalaxyType)

    def resolve_galaxies(self, info, **kwargs):
        return self.galaxies.all()


class BuildingRequiredResources(graphene.ObjectType):
    name = graphene.String()
    lv = graphene.Int()
    steel = graphene.Int()
    gold = graphene.Int()
    water = graphene.Int()


class InboxType(graphene.ObjectType):
    datetime = graphene.DateTime()
    title = graphene.String()
    message = graphene.String()


class UserType(graphene.ObjectType):
    id = graphene.ID()
    rank = graphene.Int()
    username = graphene.String()
    fleet_count = graphene.Int()
    buildings = graphene.Int()
    planets = graphene.List(PlanetType)
    fleet = graphene.List(ShipType)
    missions = graphene.List(MissionType)
    inbox = graphene.List(InboxType)

    def resolve_planets(self, info, **kwargs):
        return self.planet_set.all()
    
    def resolve_fleet(self, info, **kwargs):
        return self.ship_set.all()

    def resolve_missions(self, info, **kwargs):
        return self.mission_set.all()
    
    def resolve_inbox(self, info, **kwargs):
        return self.inbox_set.all()

    def resolve_fleet_count(self, info, **kwargs):
        return self.ship_set.count()

    def resolve_rank(self, info, **kwargs):
        return self.buildings + self.fleet_count


################################################
# QUERIES
################################################

class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    
    user = graphene.Field(
        UserType,
        id=graphene.ID(required=True),
        username=graphene.String(required=True)
    )

    @access_required
    def resolve_user(self, info, **kwargs):
        kwargs.pop('user')
        return UserModel.objects.get(**kwargs)

    ranking = graphene.List(
        UserType,
        limit=graphene.Int()
    )

    @access_required
    def resolve_ranking(self, info, **kwargs):
        return UserModel.objects.all().order_by('-fleet_count', '-buildings')[:kwargs.get('limit', 100)]

    universe = graphene.Field(UniverseType)
    
    @access_required
    def resolve_universe(self, info, **kwargs):
        return Universe.objects.first()

    solar_system = graphene.Field(
        SolarSystemType,
        galaxy__id=graphene.ID(required=True),
        galaxy_position=graphene.Int(required=True)
    )

    @access_required
    def resolve_solar_system(self, info, **kwargs):
        return SolarSystem.objects.get(galaxy_position=kwargs['galaxy_position'], galaxy_id=kwargs['galaxy__id'])

    hangar = graphene.List(ShipType)

    @access_required
    def resolve_hangar(self, info, **kwargs):
        return [ShipType(**ship) for ship in ships]

    building_next_level = graphene.Field(
        BuildingRequiredResources,
        current_level=graphene.Int(required=True),
        building_type=graphene.String(required=True)
    )

    @access_required
    def resolve_building_next_level(self, info, **kwargs):
        building_lv = kwargs['current_level']
        if building_lv < 0 or building_lv >= 50:
            raise Exception('Invalid building level')

        if kwargs['building_type'] == 'steel_mine':
            steel, gold, water = BuildingResourceRatio.get_steel_mine_resource_ratio(building_lv)
            return BuildingRequiredResources(name='Steel Mine', lv=building_lv, steel=steel, gold=gold, water=water)

        if kwargs['building_type'] == 'gold_mine':
            steel, gold, water = BuildingResourceRatio.get_gold_mine_resource_ratio(building_lv)
            return BuildingRequiredResources(name='Gold Mine', lv=building_lv, steel=steel, gold=gold, water=water)

        if kwargs['building_type'] == 'water_farm':
            steel, gold, water = BuildingResourceRatio.get_water_farm_resource_ratio(building_lv)
            return BuildingRequiredResources(name='Water Farm', lv=building_lv, steel=steel, gold=gold, water=water)

        if kwargs['building_type'] == 'military_power':
            steel, gold, water = BuildingResourceRatio.get_military_upgrade_ratio(building_lv)
            return BuildingRequiredResources(name='Military Power', lv=building_lv, steel=steel, gold=gold, water=water)

        if kwargs['building_type'] == 'shield_power':
            steel, gold, water = BuildingResourceRatio.get_shield_upgrade_ratio(building_lv)
            return BuildingRequiredResources(name='Shield Power', lv=building_lv, steel=steel, gold=gold, water=water)

        if kwargs['building_type'] == 'engine_power':
            steel, gold, water = BuildingResourceRatio.get_engine_upgrade_ratio(building_lv)
            return BuildingRequiredResources(name='Engine Power', lv=building_lv, steel=steel, gold=gold, water=water)

    mission_reports = graphene.List(
        MissionType,
        user__id=graphene.ID(required=True),
        datetime__gte=graphene.DateTime(),
        datetime__lte=graphene.DateTime()
    )

    @access_required
    def resolve_mission_reports(self, info, **kwargs):
        kwargs.pop('user')
        return Mission.objects.filter(**kwargs)


    spy = graphene.Field(
        PlanetType,
        origin_coords=graphene.List(graphene.Int, required=True),
        target_coords=graphene.List(graphene.Int, required=True),
        user_id=graphene.Int(required=True)
    )

    @access_required
    def resolve_spy(self, info, **kwargs):
        if len(kwargs['origin_coords']) < 3 or len(kwargs['target_coords']) < 3:
            raise Exception('Invalid coordinates shape')
        try:
            user = UserModel.objects.get(id=kwargs['user_id'])
        except UserModel.DoesNotExist:
            raise Exception('Invalid User ID')
        
        if user.id != kwargs['user'].id:
            raise Exception('unauthorized operation')
        
        o_g, o_ss, o_p = kwargs['origin_coords']
        t_g, t_ss, t_p = kwargs['target_coords']

        try:
            origin_planet = Planet.objects.get(galaxy=o_g, solar_system=o_ss, position=o_p)
            target_planet = Planet.objects.get(galaxy=t_g, solar_system=t_ss, position=t_p)
        except:
            raise Exception('Invalid planet location')

        if origin_planet.user.id != user.id:
            raise Exception('unauthorized operation')

        if target_planet.user.id == user.id:
            raise Exception('Cannot perform this mission on owned planetary systems...')
        
        now = datetime.now()
        
        target_fleet = ''.join(f'{k} x {v}\n' for k,v in Counter([ship.name for ship in target_planet.fleet.all()]).items())

        spy_report = f'''
        Spy report from {str(now)} on {target_planet.name} [{t_g}, {t_ss}, {t_p}] - {target_planet.user.username}
        Our probe reached the target planetary system and collected valuable intel.

        PLANET RESOURCES
         Steel: {target_planet.steel} | Water: {target_planet.water} | Gold: {target_planet.gold}

        PLANET DEVELOPMENT


         Steel Mine     | {target_planet.steel_mine_lv}
        ----------------|-----------------
         Water Farm     | {target_planet.water_farm_lv} 
        ----------------|-----------------
         Gold Mine      | {target_planet.gold_mine_lv}
        ----------------|----------------
         Military Power | {target_planet.military_power}
        ----------------|----------------
         Shield Power   | {target_planet.shield_power}
        ----------------|----------------
         Engine Power   | {target_planet.engine_power}

        MILITARY FORCES

         {target_fleet}
        '''


        target_inbox = Inbox.objects.create(
            title=f'[{str(now)}] Spy activity from {user.username} on {target_planet.name}',
            datetime=now,
            message=f'A spy probe comming from {origin_planet.name} [{o_g}, {o_ss}, {o_p}] was detected on {target_planet.name} collecting crucial information about the planet development!',
            user=target_planet.user
        )
        target_inbox.save()

        origin_inbox = Inbox.objects.create(
            title=f'[{str(now)}] Spy report from {target_planet.name}',
            datetime=now,
            message=spy_report,
            user=user
        )
        origin_inbox.save()

        return target_planet

    inbox_messages = graphene.List(
        InboxType,
        user__id=graphene.ID(required=True)
    )

    @access_required
    def resolve_inbox_messages(self, info, **kwargs):
        kwargs.pop('user')
        return Inbox.objects.filter(**kwargs)

################################################
# MUTATIONS
################################################


class CreatePlanet(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        name = graphene.String(requried=True)
        galaxy = graphene.Int(required=True)
        solar_system = graphene.Int(required=True)
        position = graphene.Int(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        galaxy = Galaxy.objects.get(id=kwargs['galaxy'])
        ss = galaxy.solarsystem_set.all()[kwargs['solar_system']]
        if ss.__getattribute__(f'position_{kwargs["position"]}') is not None:
            raise Exception('Position already colonized...')
        
        temperature = randint(-50, 88)
        size = randint(66, 266)
        planet = Planet.objects.create(
            name=kwargs['name'],
            size=size,
            temperature=temperature,
            galaxy=kwargs['galaxy'],
            solar_system=kwargs['solar_system'],
            position=kwargs['position'],
        )
        planet.save()

        ss.__setattr__(f'position_{kwargs["position"]}', planet)
        ss.save()

        return CreatePlanet(planet)


class ImproveWaterFarm(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.water_farm_lv == 50:
            raise Exception('Water Farm already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_water_farm_resource_ratio(planet.water_farm_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.water_farm_lv += 1
        planet.save()

        return ImproveWaterFarm(planet)


class ImproveSteelMine(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.steel_mine_lv == 50:
            raise Exception('Steel mine already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_steel_mine_resource_ratio(planet.steel_mine_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.steel_mine_lv += 1
        planet.save()

        return ImproveSteelMine(planet)


class ImproveGoldMine(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.gold_mine_lv == 50:
            raise Exception('Gold mine already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_gold_mine_resource_ratio(planet.gold_mine_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.gold_mine_lv += 1
        planet.save()

        return ImproveGoldMine(planet)


class ImproveEnginePower(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.engine_power == 50:
            raise Exception('Engine power already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_engine_upgrade_ratio(planet.gold_mine_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.engine_power += 1
        planet.save()

        return ImproveEnginePower(planet)


class ImproveMilitaryPower(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.military_power == 50:
            raise Exception('Military power already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_military_upgrade_ratio(planet.gold_mine_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.military_power += 1
        planet.save()

        return ImproveMilitaryPower(planet)


class ImproveShieldPower(graphene.relay.ClientIDMutation):
    planet = graphene.Field(PlanetType)

    class Input:
        planet_id = graphene.ID(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.shield_power == 50:
            raise Exception('Shield power already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_military_upgrade_ratio(planet.gold_mine_lv)

        if (planet.steel < steel) or (planet.gold < gold) or (planet.water < water):
            raise Exception('Do not have necessary amount of resources, cannot improve the building')

        planet.steel -= steel
        planet.gold -= gold
        planet.water -= water
        planet.fields_used += 1
        planet.shield_power += 1
        planet.save()

        return ImproveShieldPower(planet)


class BuildShip(graphene.relay.ClientIDMutation):
    ship = graphene.Field(ShipType)

    class Input:
        planet_id = graphene.ID(required=True)
        ship_id = graphene.Int(required=True)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        ship = ships[kwargs['ship_id']]

        # Validate infrastructure requirements
        military = ship['requirements']['military_power']
        shield = ship['requirements']['shield_power']
        engine = ship['requirements']['engine_power']

        infrastructure = (planet.military_power >= military) and (planet.shield_power >= shield) and (planet.engine_power >= engine)

        # Validate resource requirements
        steel = ship['cost']['steel']
        water = ship['cost']['water']
        gold = ship['cost']['water']

        resources = (planet.steel >= steel) and (planet.water >= water) and (planet.gold >= gold)

        able_to_do = infrastructure and resources

        if not able_to_do:
            raise Exception('Not enough requirements or resources.')

        planet.steel -= steel
        planet.water -= water
        planet.gold -= gold

        new_ship = Ship.objects.create(
            name=ship['name'],
            description=ship['description'],
            offense_power=ship['offense_power'],
            shield_power=ship['shield_power'],
            cargo_space=ship['cargo_space'],
            speed=ship['speed'],
            integrity=ship['integrity']
        )
        new_ship.save()
        planet.fleet.add(new_ship)
        planet.save()

        return BuildShip(ship)


class SendAttackMission(graphene.relay.ClientIDMutation):
    mission = graphene.Field(MissionType)

    class Input:
        origin_planet = graphene.ID(required=True)
        target_planet = graphene.ID(required=True)
        fleet = graphene.List(graphene.ID, required=True)
        speed = graphene.Float(default=1.0)

    @access_required
    def mutate_and_get_payload(self, info, **kwargs):
        origin_planet = Planet.objects.get(id=kwargs['origin_planet'])
        target_planet = Planet.objects.get(id=kwargs['target_planet'])

        fleet = Ship.objects.filter(id__in=kwargs['fleet'])
        fleet = [ship for ship in fleet if ship in origin_planet.fleet.all()]
        for ship in fleet:
            origin_planet.fleet.remove(ship)

        if len(fleet) == 0:
            raise Exception('Invalid ship assigment')

        src_coord = np.array([origin_planet.galaxy, origin_planet.solar_system, origin_planet.position])
        tgt_coord = np.array([target_planet.galaxy, target_planet.solar_system, target_planet.position])
        distance = np.linalg.norm(tgt_coord - src_coord)
        travel_time = int( ((distance * 60) / origin_planet.engine_power) * kwargs['speed'])

        now = datetime.now()
        attack_arrive = now + timedelta(seconds=travel_time)
        return_to_planet = attack_arrive + timedelta(seconds=travel_time)

        mission = Mission.objects.create(
            kind='Attack',
            origin_galaxy=origin_planet.galaxy,
            origin_solar_system=origin_planet.solar_system,
            origin_position=origin_planet.position,
            target_galaxy=target_planet.galaxy,
            target_solar_system=target_planet.solar_system,
            target_position=target_planet.position,
            speed=kwargs['speed'],
            launch_datetime=now,
            arrival_datetime=attack_arrive,
            return_datetime=return_to_planet,
            state='going',
            distance=distance,
            success=False,
            travel_time=travel_time,
        )
        mission.fleet.set(fleet)
        mission.save()
        origin_planet.save()

        r = Redis(host='104.237.1.145', port=6379, db=0)
        r.set(f'mission_{mission.id}', mission.id)

        fleet_report = ''.join(f'{k} x {v}\n' for k,v in Counter([ship.name for ship in mission.fleet.all()]).items())

        attack_alert = f'''
        [{str(now)}] An incoming hostile fleet from {origin_planet.name} {list(src_coord)} - {origin_planet.user.username}
        towards the planet {target_planet.name} {list(tgt_coord)} with estimated arrival datetime {str(attack_arrive)}

        The following ships were identified:

        {fleet_report}
        '''
 
        target_inbox = Inbox.objects.create(
            title=f'[{str(now)}] Incomming attack from {origin_planet.user.username} on {target_planet.name}',
            datetime=now,
            message=attack_alert,
            user=target_planet.user
        )
        target_inbox.save()

        return SendAttackMission(mission)


class SignUp(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        planet_name = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        # Check if username or email already exists
        try:
            UserModel.objects.get(username=kwargs['username'])
        except UserModel.DoesNotExist:
            pass
        else:
            raise Exception('Username already in use')

        # Create user object
        user = UserModel.objects.create(username=kwargs['username'])
        user.set_password(kwargs['password'])
        user.save()

        empty_positions = {
            'position_1': 1,
            'position_2': 2,
            'position_3': 3,
            'position_4': 4,
            'position_5': 5,
            'position_6': 6,
            'position_7': 7,
            'position_8': 8,
            'position_9': 9,
            'position_10': 10,
            'position_11': 11,
            'position_12': 12,
            'position_13': 13,
            'position_14': 14,
            'position_15': 15
        }
        position_filter = choice(list(empty_positions))
        planet_position = empty_positions[position_filter]

        ss = choice(SolarSystem.objects.filter(**{position_filter: None}))
  
        planet = Planet.objects.create(
            name=kwargs['planet_name'],
            temperature=randint(-50, 88),
            size=randint(66, 266),
            galaxy=ss.galaxy.id,
            solar_system=ss.galaxy_position,
            position=planet_position,
            user=user
        )
        planet.save() 

        ss.__setattr__(position_filter, planet)
        ss.save()

        building_points = planet.steel_mine_lv + planet.water_farm_lv + planet.gold_mine_lv
        infra_points = planet.engine_power + planet.military_power + planet.shield_power
        user.buildings = building_points + infra_points
        user.save()

        return SignUp(user)


class SignIn(graphene.relay.ClientIDMutation):
    token = graphene.String()
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            user = UserModel.objects.get(
                username=kwargs['username']
            )
        except UserModel.DoesNotExist:
            raise Exception('User not found')

        if not user.check_password(kwargs['password']):
            raise Exception('Invalid password')

        user.last_login = datetime.now()
        user.save()

        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=user.username,
            password=kwargs['password']
        )

        return SignIn(token=session.token, user=user)


class Mutation:
    sign_up = SignUp.Field()
    sign_in = SignIn.Field()

    create_planet = CreatePlanet.Field()
    improve_water_farm = ImproveWaterFarm.Field()
    improve_steel_mine = ImproveSteelMine.Field()
    improve_gold_mine = ImproveGoldMine.Field()
    improve_engine_power = ImproveEnginePower.Field()
    improve_military_power = ImproveMilitaryPower.Field()
    improve_shield_power = ImproveShieldPower.Field()
    
    build_ship = BuildShip.Field()
    
    send_attack_mission = SendAttackMission.Field()