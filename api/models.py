from django.db import models

# Create your models here.


class Ship(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    offense_power = models.IntegerField()
    shield_power = models.IntegerField()
    cargo_space = models.IntegerField()
    speed = models.IntegerField()


class Planet(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    size = models.IntegerField(null=False)
    galaxy = models.IntegerField(null=False)
    solar_system = models.IntegerField(null=False)
    position = models.IntegerField(null=False)
    water = models.IntegerField(default=0)
    steel = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    temperature = models.FloatField(null=False)
    water_farm_lv = models.IntegerField(default=1)
    gold_mine_lv = models.IntegerField(default=1)
    steel_mine_lv = models.IntegerField(default=1)
    fields_used = models.IntegerField(default=0)

    military_power = models.IntegerField(default=0)
    engine_power = models.IntegerField(default=1)
    shield_power = models.IntegerField(default=0)

    fleet = models.ManyToManyField(Ship)


class Galaxy(models.Model):
    id = models.IntegerField(primary_key=True)


class SolarSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    galaxy_position = models.IntegerField()
    position_1 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p1')
    position_2 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p2')
    position_3 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p3')
    position_4 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p4')
    position_5 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p5')
    position_6 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p6')
    position_7 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p7')
    position_8 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p8')
    position_9 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p9')
    position_10 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p10')
    position_11 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p11')
    position_12 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p12')
    position_13 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p13')
    position_14 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p14')
    position_15 = models.OneToOneField(Planet, on_delete=models.CASCADE, null=True, related_name='p15')
    galaxy = models.ForeignKey(Galaxy, on_delete=models.CASCADE, null=True)


class Universe(models.Model):
    galaxies = models.ManyToManyField(Galaxy)