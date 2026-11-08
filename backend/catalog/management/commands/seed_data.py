from django.core.management.base import BaseCommand

from catalog.models import Biotope, Region, Species


REGIONS = {
    'Amazonía': ['Río Negro', 'Río Amazonas'],
    'Sudeste Asiático': ['Río Mekong', 'Pantano de Tailandia'],
    'Lago Malawi': ['Zona rocosa', 'Zona arenosa'],
}

SPECIES = [
    {
        'common_name': 'Tetra neón',
        'scientific_name': 'Paracheirodon innesi',
        'kind': 'fish',
        'temp_min': 20, 'temp_max': 26,
        'ph_min': 6.0, 'ph_max': 7.0,
        'gh_min': 1, 'gh_max': 8,
        'adult_size_cm': 2.5,
        'min_tank_liters': 60,
        'min_group_size': 6,
        'diet': 'omnivore',
        'temperament': 'peaceful',
        'swim_zone': 'middle',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': False,
        'biotope': ('Río Negro', 'Amazonía'),
    },
    {
        'common_name': 'Corydora panda',
        'scientific_name': 'Corydoras panda',
        'kind': 'fish',
        'temp_min': 22, 'temp_max': 26,
        'ph_min': 6.0, 'ph_max': 7.5,
        'gh_min': 2, 'gh_max': 10,
        'adult_size_cm': 5,
        'min_tank_liters': 60,
        'min_group_size': 5,
        'diet': 'omnivore',
        'temperament': 'peaceful',
        'swim_zone': 'bottom',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': False,
        'biotope': ('Río Amazonas', 'Amazonía'),
    },
    {
        'common_name': 'Ramirezi',
        'scientific_name': 'Mikrogeophagus ramirezi',
        'kind': 'fish',
        'temp_min': 24, 'temp_max': 28,
        'ph_min': 5.5, 'ph_max': 7.0,
        'gh_min': 1, 'gh_max': 8,
        'adult_size_cm': 6,
        'min_tank_liters': 80,
        'min_group_size': 2,
        'diet': 'omnivore',
        'temperament': 'semi_aggressive',
        'swim_zone': 'bottom',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': True,
        'biotope': ('Río Amazonas', 'Amazonía'),
    },
    {
        'common_name': 'Otocinclus',
        'scientific_name': 'Otocinclus vittatus',
        'kind': 'fish',
        'temp_min': 22, 'temp_max': 26,
        'ph_min': 6.0, 'ph_max': 7.5,
        'gh_min': 2, 'gh_max': 10,
        'adult_size_cm': 4,
        'min_tank_liters': 60,
        'min_group_size': 3,
        'diet': 'herbivore',
        'temperament': 'peaceful',
        'swim_zone': 'bottom',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': False,
        'biotope': ('Río Negro', 'Amazonía'),
    },
    {
        'common_name': 'Rasbora arlequín',
        'scientific_name': 'Trigonostigma heteromorpha',
        'kind': 'fish',
        'temp_min': 23, 'temp_max': 28,
        'ph_min': 5.5, 'ph_max': 7.0,
        'gh_min': 1, 'gh_max': 8,
        'adult_size_cm': 4,
        'min_tank_liters': 60,
        'min_group_size': 6,
        'diet': 'omnivore',
        'temperament': 'peaceful',
        'swim_zone': 'middle',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': False,
        'biotope': ('Río Mekong', 'Sudeste Asiático'),
    },
    {
        'common_name': 'Guppy',
        'scientific_name': 'Poecilia reticulata',
        'kind': 'fish',
        'temp_min': 22, 'temp_max': 28,
        'ph_min': 6.8, 'ph_max': 8.0,
        'gh_min': 8, 'gh_max': 20,
        'adult_size_cm': 4,
        'min_tank_liters': 40,
        'min_group_size': 3,
        'diet': 'omnivore',
        'temperament': 'peaceful',
        'swim_zone': 'top',
        'eats_plants': False,
        'fin_nipper': False,
        'territorial': False,
        'biotope': ('Río Amazonas', 'Amazonía'),
    },
]


class Command(BaseCommand):
    help = 'Carga regiones, biotopos y especies de ejemplo (idempotente).'

    def handle(self, *args, **options):
        for region_name, biotope_names in REGIONS.items():
            region, _ = Region.objects.get_or_create(name=region_name)
            for biotope_name in biotope_names:
                Biotope.objects.get_or_create(name=biotope_name, region=region)

        for item in SPECIES:
            data = dict(item)
            biotope_name, region_name = data.pop('biotope')
            biotope = Biotope.objects.get(name=biotope_name, region__name=region_name)
            Species.objects.update_or_create(
                scientific_name=data['scientific_name'],
                defaults={**data, 'biotope': biotope},
            )

        self.stdout.write(self.style.SUCCESS(
            f'Datos cargados: {Region.objects.count()} regiones, '
            f'{Biotope.objects.count()} biotopos, {Species.objects.count()} especies.'
        ))
