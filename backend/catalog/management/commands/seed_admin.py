import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea (o actualiza) el usuario admin del panel. Idempotente.'

    def handle(self, *args, **options):
        username = 'admin'
        env_password = os.environ.get('ADMIN_PASSWORD')
        password = env_password or 'admin12345'

        user, created = User.objects.get_or_create(username=username)
        user.is_staff = True
        user.is_superuser = True
        if created or env_password:
            user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Admin creado: {username} (contraseña desde ADMIN_PASSWORD o valor de desarrollo).'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'El admin "{username}" ya existía; se aseguró is_staff=True.'
            ))
