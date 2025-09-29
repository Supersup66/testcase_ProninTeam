from django.core.management.base import BaseCommand
from api.factories import UserFactory, CollectionFactory, PaymentFactory
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Fill the database with fake data using factories.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of objects to create. Must be a positive integer.'
        )

    def handle(self, *args, **options):
        count = options['count']

        if count <= 0:
            self.stderr.write(
                self.style.ERROR('Count must be a positive integer.'))
            return
        start = datetime.now()
        users = UserFactory.create_batch(count)
        collections = CollectionFactory.create_batch(count)
        payments = PaymentFactory.create_batch(count)

        self.stdout.write(self.style.SUCCESS(
            f'{len(collections)} collections created.'))

        self.stdout.write(self.style.SUCCESS(
            f'{len(payments)} payments created.'))

        self.stdout.write(self.style.SUCCESS(
            f'{len(users) + len(payments)} users created.'))

        end = datetime.now() - start
        self.stdout.write(self.style.SUCCESS(
            f'Время выполнения: {int(end.total_seconds())} секунд.'))
