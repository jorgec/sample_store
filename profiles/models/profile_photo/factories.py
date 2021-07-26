import factory
from faker import Faker

from .models import ProfilePhoto as Master

fake = Faker()


class ProfilePhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Master
    
    # Fields:
