from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from profiles.models import Profile, Gender
from profiles.models.profile_photo.serializers import ProfilePhotoSerializer


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name']


class ProfileDataSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField('repr_gender')
    photo = serializers.SerializerMethodField('repr_photo')
    name = serializers.SerializerMethodField('repr_name')
    casual_name = serializers.SerializerMethodField('repr_casual_name')
    full_name = serializers.SerializerMethodField('repr_full_name')
    username = serializers.SerializerMethodField('repr_username')

    def repr_name(self, obj):
        return obj.get_name()

    def repr_casual_name(self, obj):
        return obj.get_casual_name()

    def repr_full_name(self, obj):
        return obj.get_full_name()

    def repr_username(self, obj):
        return obj.get_username()

    def repr_photo(self, obj):
        photo = obj.get_photo()
        try:
            return ProfilePhotoSerializer(photo).data
        except AttributeError:
            return {
                "id": None,
                "photo": None,
                "caption": None,
            }

    def repr_gender(self, obj):
        if obj.gender:
            return Gender.objects.get(id=obj.gender_id).name
        return None

    class Meta:
        model = Profile
        fields = [
            'id',
            'uuid',
            'account',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'photo',
            'name',
            'casual_name',
            'full_name',
            'username'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('repr_url')
    gender = serializers.SerializerMethodField('repr_gender')
    photo = serializers.SerializerMethodField('repr_photo')
    name = serializers.SerializerMethodField('repr_name')
    casual_name = serializers.SerializerMethodField('repr_casual_name')
    full_name = serializers.SerializerMethodField('repr_full_name')
    username = serializers.SerializerMethodField('repr_username')

    def repr_name(self, obj):
        return obj.get_name()

    def repr_casual_name(self, obj):
        return obj.get_casual_name()

    def repr_full_name(self, obj):
        return obj.get_full_name()

    def repr_username(self, obj):
        return obj.get_username()

    def repr_photo(self, obj):
        photo = obj.get_photo()
        try:
            return ProfilePhotoSerializer(photo).data
        except AttributeError:
            return {
                "id": None,
                "photo": None,
                "caption": None,
            }

    def repr_gender(self, obj):
        if obj.gender:
            return Gender.objects.get(id=obj.gender_id).name
        return None

    def repr_url(self, obj):
        url = reverse_lazy(
            'dashboard_user_profile_detail_view',
            kwargs={
                'profile': obj.uuid
            }
        )
        return url

    class Meta:
        model = Profile
        fields = [
            'id',
            'uuid',
            'account',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'url',
            'photo',
            'name',
            'casual_name',
            'full_name',
            'username'
        ]
