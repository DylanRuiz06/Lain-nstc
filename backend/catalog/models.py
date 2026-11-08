from django.core.exceptions import ValidationError
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Biotope(models.Model):
    name = models.CharField(max_length=120)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='biotopes')

    class Meta:
        ordering = ['region__name', 'name']

    def __str__(self):
        return f'{self.name} ({self.region.name})'


class Species(models.Model):
    KIND_CHOICES = [
        ('fish', 'Pez'),
        ('invertebrate', 'Invertebrado'),
        ('plant', 'Planta'),
        ('amphibian', 'Anfibio'),
    ]
    DIET_CHOICES = [
        ('herbivore', 'Herbívoro'),
        ('carnivore', 'Carnívoro'),
        ('omnivore', 'Omnívoro'),
    ]
    TEMPERAMENT_CHOICES = [
        ('peaceful', 'Pacífico'),
        ('semi_aggressive', 'Semiagresivo'),
        ('aggressive', 'Agresivo'),
    ]
    SWIM_ZONE_CHOICES = [
        ('top', 'Superior'),
        ('middle', 'Media'),
        ('bottom', 'Inferior'),
    ]

    common_name = models.CharField(max_length=150)
    scientific_name = models.CharField(max_length=150, unique=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    ph_min = models.FloatField()
    ph_max = models.FloatField()
    gh_min = models.FloatField()
    gh_max = models.FloatField()
    adult_size_cm = models.FloatField()
    min_tank_liters = models.IntegerField()
    min_group_size = models.IntegerField()
    diet = models.CharField(max_length=20, choices=DIET_CHOICES)
    temperament = models.CharField(max_length=20, choices=TEMPERAMENT_CHOICES)
    swim_zone = models.CharField(max_length=10, choices=SWIM_ZONE_CHOICES)
    eats_plants = models.BooleanField(default=False)
    fin_nipper = models.BooleanField(default=False)
    territorial = models.BooleanField(default=False)
    biotope = models.ForeignKey(Biotope, on_delete=models.PROTECT, related_name='species')

    class Meta:
        ordering = ['common_name']
        verbose_name_plural = 'species'

    def __str__(self):
        return self.common_name

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('scientific_name',):
            return ValidationError({
                'scientific_name': 'Ya existe una especie con ese nombre científico.',
            })
        return super().unique_error_message(model_class, unique_check)

    def clean(self):
        errors = {}

        if self.ph_min is not None and self.ph_max is not None:
            try:
                if not (0 <= self.ph_min <= 14):
                    errors.setdefault('ph_min', []).append('El pH mínimo debe estar entre 0 y 14.')
                if not (0 <= self.ph_max <= 14):
                    errors.setdefault('ph_max', []).append('El pH máximo debe estar entre 0 y 14.')
                if self.ph_min > self.ph_max:
                    errors.setdefault('ph_max', []).append('El pH mínimo no puede ser mayor que el pH máximo.')
            except TypeError:
                pass

        if self.temp_min is not None and self.temp_max is not None:
            try:
                if not (0 <= self.temp_min <= 40):
                    errors.setdefault('temp_min', []).append('La temperatura mínima debe estar entre 0 y 40 °C.')
                if not (0 <= self.temp_max <= 40):
                    errors.setdefault('temp_max', []).append('La temperatura máxima debe estar entre 0 y 40 °C.')
                if self.temp_min >= self.temp_max:
                    errors.setdefault('temp_max', []).append('La temperatura mínima debe ser menor que la máxima.')
            except TypeError:
                pass

        if self.gh_min is not None and self.gh_max is not None:
            try:
                if self.gh_min < 0:
                    errors.setdefault('gh_min', []).append('La dureza GH mínima no puede ser negativa.')
                if self.gh_min > self.gh_max:
                    errors.setdefault('gh_max', []).append('La GH mínima no puede ser mayor que la GH máxima.')
            except TypeError:
                pass

        if self.adult_size_cm is not None:
            try:
                if self.adult_size_cm <= 0:
                    errors.setdefault('adult_size_cm', []).append('El tamaño adulto debe ser mayor que 0.')
            except TypeError:
                pass

        if self.min_tank_liters is not None:
            try:
                if self.min_tank_liters <= 0:
                    errors.setdefault('min_tank_liters', []).append('Los litros mínimos deben ser mayores que 0.')
            except TypeError:
                pass

        if self.min_group_size is not None:
            try:
                if self.min_group_size < 1:
                    errors.setdefault('min_group_size', []).append('El grupo mínimo debe ser al menos 1.')
            except TypeError:
                pass

        if errors:
            raise ValidationError(errors)
