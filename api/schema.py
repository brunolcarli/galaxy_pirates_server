from random import randint
import graphene
from django.conf import settings
from api.models import Universe, Galaxy, SolarSystem, Planet


class PlanetType(graphene.ObjectType):
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

class Mutation:
    create_planet = CreatePlanet.Field()
