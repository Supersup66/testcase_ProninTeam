from django.core.management.base import BaseCommand
from payments.models import Payment
from collects.models import Collection
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'Clean tables payments, collections, users in db.'

    def handle(self, *args, **options):
        payments_deleted, _ = Payment.objects.all().delete()
        collections_deleted, _ = Collection.objects.all().delete()
        users_deleted, _ = User.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'{payments_deleted} payments deleted.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'{collections_deleted} collections deleted.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'{users_deleted} users deleted.'
            )
        )
