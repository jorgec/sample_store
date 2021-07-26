from faker import Faker
from django.test import TestCase


from profiles.models.profile_photo.models import ProfilePhoto as Master

fake = Faker()


class ProfilePhotoTest(TestCase):
    def test_create_profile_photo(self):
        # standard creation
        obj = Master.objects.create(

        )

        self.assertTrue(
            isinstance(
                obj,
                Master
            ),
            f"{obj} is not of type {Master}"
        )