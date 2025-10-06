import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from collects.constants import Reason
from collects.models import Collection
from payments.models import Payment

User = get_user_model()
faker = Faker()


class Command(BaseCommand):
    help = 'Fill the database with fake data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=1000,
            help='Number of users to create. Must be a positive integer.'
        )
        parser.add_argument(
            '--collects',
            type=int,
            default=1000,
            help='Number of collects to create. Must be a positive integer.'
        )
        parser.add_argument(
            '--payments',
            type=int,
            default=2000,
            help='Number of collects to create. Must be a positive integer.'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_collects = options['collects']
        num_payments = options['payments']
        if any(x < 0 for x in (
            num_users, num_collects, num_payments)
        ):
            self.stderr.write(
                self.style.ERROR('Number must be a positive integer.'))
            return
        start = datetime.now()

        users = []
        for _ in range(num_users):
            users.append(
                User(
                    username=faker.unique.user_name(),
                    email=faker.unique.email(),
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                )
            )
        try:
            users = User.objects.bulk_create(users)
            self.stdout.write(
                self.style.SUCCESS(f'{len(users)} users created'))
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'User creation failed: {e}')
            )
            return

        collects = []
        for _ in range(num_collects):
            stop_date = datetime.now() + timedelta(days=random.randint(-1, 30))
            author = random.choice(users)
            collects.append(
                Collection(
                    author=author,
                    title=faker.unique.sentence(nb_words=3),
                    description=faker.text(max_nb_chars=200),
                    reason=random.choice(Reason.values),
                    end_time=random.choice((None, stop_date)),
                    created_at=faker.date_time_this_year(),
                    target_amount=random.choice(
                        (
                            None,
                            random.randint(0, 10000)
                        )
                    )
                )
            )
        try:
            collects = Collection.objects.bulk_create(collects)
            self.stdout.write(
                self.style.SUCCESS(f"{len(collects)} collects created")
            )
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Collect creation failed: {e}')
            )
            return

        payments = []
        for _ in range(num_payments):
            payments.append(
                Payment(
                    payer=random.choice(users),
                    collect=random.choice(collects),
                    amount=random.uniform(1, 100),
                    is_hidden=random.choice([True, False]),
                )
            )
        payments = Payment.objects.bulk_create(payments)
        self.stdout.write(
            self.style.SUCCESS(f"{len(payments)} payments created")
        )
        end = datetime.now() - start
        self.stdout.write(self.style.SUCCESS(
            f'Время выполнения: {int(end.total_seconds())} секунд.'))
