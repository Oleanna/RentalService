import os
import random
from datetime import timedelta

import django
import faker
from factory import fuzzy

from apps.bookings.permissions import CanRejectBooking
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
        #django_get_or_create = ('username',)

    # first_name = factory.LazyAttribute(lambda _: faker_.unique.username())
    # email = factory.LazyAttribute(lambda obj: f"{obj.username}@email.com")

    email = factory.Faker('email')

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    role = factory.LazyAttribute(lambda: random.choice(Roles.choices()))
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@email.com")

    birthday = factory.LazyAttribute('date_of_birth', minimum_age=18, maximum_age=99)
    age = factory.LazyAttribute(lambda obj: timezone.now().year - obj.birthday.year)

    phone_number = factory.LazyAttribute(lambda _: f"+{faker_.msisdn()}")
    is_staff = False
    is_active = True

    date_joined = factory.LazyAttribute(timezone.now)

    password = factory.LazyAttribute(lambda: make_password("qwertz12345"))

class ListingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listing

    country = factory.Faker('country')
    city = factory.Faker('city')
    street = factory.Faker('street_name')

    # postcode = factory.Faker('postcode')
    # building = factory.Faker('building_number')
    # apartment = factory.Faker('apartment_number', min=1, max=9999)

    location = factory.LazyAttribute(
        lambda obj: f"{obj.street}, {obj.city}, {obj.country}"
    )
    landlord = factory.SubFactory(UserFactory)

    title = factory.Faker('title')
    description = factory.Faker('paragraph')
    price = fuzzy.FuzzyDecimal(300, 5000, precision=2)
    rooms = fuzzy.FuzzyInteger(1, 5)

    property_type = factory.LazyAttribute(lambda: random.choice(PropertyType.choices()))

    created_at = factory.LazyAttribute(lambda: timezone.now())
    updated_at = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=random.randint(1, 365)))
    is_active = True

    is_active = factory.LazyAttribute(lambda: random.choice([True, False]))


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    listing = factory.SubFactory(ListingFactory)
    user = factory.SubFactory(UserFactory)
    rating = fuzzy.FuzzyFloat(1.0, 5.0)
    comment = factory.Faker('text', max_nb_chars=600)
    created_at = factory.LazyAttribute(lambda: timezone.now())

class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
        listing = factory.SubFactory(ListingFactory)
        user = factory.SubFactory(UserFactory)
        check_in = factory.LazyAttribute(lambda: timezone.now())
        check_out = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=random.randint(1, 365)))

        status = factory.LazyAttribute(lambda: random.choice(BookingStatus.choices()))
        created_at = factory.LazyAttribute(lambda: timezone.now())


if __name__ == "__main__":
    print("!!")
    UserFactory.create_batch(100)
    ListingFactory.create_batch(100)
    ReviewFactory.create_batch(300)
    BookingFactory.create_batch(70)
    print("DONE")

