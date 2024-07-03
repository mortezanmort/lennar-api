from random import sample

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from stuffs.factories import ComponentFactory, GroupFactory, SpecificationFactory


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        specifications = SpecificationFactory.create_batch(10)
        current_specification = specifications[-1]

        groups = GroupFactory.create_batch(10, specification=current_specification)
        ComponentFactory.create_batch(10, group=sample(groups, 1)[0], specification=current_specification)

        User = get_user_model()
        User.objects.create_superuser(username="admin", password="admin")

        self.stdout.write("Data seeded successfully.")
