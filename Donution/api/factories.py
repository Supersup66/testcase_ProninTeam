import factory
from collects.models import Collection
from collects.constants import Reason
from payments.models import Payment
from faker import Faker
from django.contrib.auth import get_user_model

fake = Faker('ru_RU')
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall(
        'set_password',
        'default_password'
    )
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    author = factory.Iterator(User.objects.all())
    title = factory.Faker('sentence', nb_words=6)
    description = factory.Faker('paragraph')
    reason = factory.Iterator(Reason)
    target_amount = factory.Faker(
        'pyint',
        min_value=1000,
        max_value=10000
    )
    image = factory.django.ImageField(color='blue')
    created_at = factory.Faker('date_time_this_year')
    end_time = factory.Faker('future_datetime')


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    amount = factory.Faker(
        'pyint',
        min_value=10,
        max_value=100
    )
    collect = factory.Iterator(Collection.objects.all())
    payer = factory.Iterator(User.objects.all().order_by('username'))
    payment_date_time = factory.Faker('date_time_this_year')
