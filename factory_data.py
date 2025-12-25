import os
import random
from datetime import timedelta

import django
import faker
from factory import fuzzy
from common.enums import Roles, PropertyType, BookingStatus

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from apps.users.models import User
from apps.listings.models import Listing
from apps.bookings.models import Booking
from apps.reviews.models import Review

faker_ = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    role = Roles.RENTER.value

    email = factory.LazyAttributeSequence(lambda obj, n: f"{obj.last_name.lower()}_{obj.role}_{n}@email.com")

    birthday = factory.Faker('date_of_birth', minimum_age=18, maximum_age=99)

    phone_number = factory.LazyAttribute(lambda _: f"+{faker_.msisdn()}")
    is_active = True

    password = factory.LazyFunction(lambda: make_password("qwertz12345"))

class LandlordFactory(UserFactory):
    role = Roles.LANDLORD.value


class RenterFactory(UserFactory):
    role = Roles.RENTER.value

class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    landlord = factory.SubFactory(LandlordFactory)
    title = factory.Faker('catch_phrase')
    location = factory.LazyAttribute(
        lambda _: f"{faker_.street_name()}, {faker_.city()}, {faker_.country()}"
    )
    description = factory.Faker('paragraph')
    price = fuzzy.FuzzyDecimal(300, 5000, precision=2)
    rooms = fuzzy.FuzzyInteger(1, 5)

    property_type = factory.LazyAttribute(lambda _: random.choice(PropertyType.choices()))
    is_active = True


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
    listing = factory.SubFactory(ListingFactory)
    renter = factory.SubFactory(RenterFactory)
    check_in = factory.LazyFunction(
            lambda : timezone.now() + timedelta(days=random.randint(1, 30))
        )

    check_out = factory.LazyAttribute(
        lambda obj: obj.check_in + timedelta(days=random.randint(1, 364))
    )
    #status = factory.LazyAttribute(lambda: random.choice(BookingStatus.choices()))
    status = BookingStatus.PENDING.value


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    listing = factory.SubFactory(ListingFactory)
    user = factory.SubFactory(RenterFactory)
    rating = fuzzy.FuzzyFloat(1.0, 5.0)
    comment = factory.Faker('text', max_nb_chars=600)

if __name__ == "__main__":
    LandlordFactory.create_batch(20)
    RenterFactory.create_batch(50)

    ListingFactory.create_batch(100)
    BookingFactory.create_batch(150)
    ReviewFactory.create_batch(80)

    print("DONE")
