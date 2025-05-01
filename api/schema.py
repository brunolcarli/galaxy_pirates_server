from random import randint
import graphene
from django.conf import settings
from api.models import Universe, Galaxy, SolarSystem, Planet, Ship
from api.util import BuildingResourceRatio
from api.ships import ships


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
    name = graphene.String()
    description = graphene.String()
    offense = graphene.Int()
    shield = graphene.Int()
    cargo = graphene.Int()
    speed = graphene.Int()
    cost = graphene.Field(ResourceCostType)
    build_time = graphene.Int()
    requirements = graphene.Field(RequirementsType)


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


class SolarSystemType(graphene.ObjectType):
    id = graphene.ID()
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



################################################
# QUERIES
################################################


class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    universe = graphene.Field(UniverseType)
    def resolve_universe(self, info, **kwargs):
        return Universe.objects.first()

    solar_system = graphene.Field(
        SolarSystemType,
        galaxy__id=graphene.ID(required=True),
        galaxy_position=graphene.Int(required=True)
    )
    def resolve_solar_system(self, info, **kwargs):
        galaxy = Galaxy.objects.get(id=kwargs['galaxy__id'])
        return galaxy.solarsystem_set.all()[kwargs['galaxy_position']]

    hangar = graphene.List(ShipType)

    def resolve_hangar(self, info, **kwargs):
        return [ShipType(**ship) for ship in ships]



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

    def mutate_and_get_payload(self, info, **kwargs):
        planet = Planet.objects.get(id=kwargs['planet_id'])
        
        if planet.gold_mine_lv == 50:
            raise Exception('Gold mine already reached max level')

        if planet.fields_used == planet.size:
            raise Exception('Planet reached max occupation size, do not have space left for building')

        steel, gold, water = BuildingResourceRatio.get_gold_mine_resource_ration(planet.gold_mine_lv)

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


class BuildShip(graphene.relay.ClientIDMutation):
    ship = graphene.Field(ShipType)

    class Input:
        planet_id = graphene.ID(required=True)
        ship_id = graphene.Int(required=True)

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

        new_ship = Ship.objetcts.create(
            name=ship['name'],
            description=ship['description'],
            offense_power=ship['offense'],
            shield_power=ship['shield'],
            cargo_space=ship['cargo'],
            speed=ship['speed']
        )
        new_ship.save()
        planet.fleet.add(new_ship)
        planet.save()

        return BuildShip(ship)

class Mutation:
    create_planet = CreatePlanet.Field()
    improve_water_farm = ImproveWaterFarm.Field()
    improve_steel_mine = ImproveSteelMine.Field()
    improve_gold_mine = ImproveGoldMine.Field()
    improve_engine_power = ImproveEnginePower.Field()
    build_ship = BuildShip.Field()
