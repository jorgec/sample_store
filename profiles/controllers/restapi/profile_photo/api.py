from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from profiles.models import ProfilePhoto
from profiles.models.profile_photo.serializers import ProfilePhotoSerializer


class ProfilePhotoAPI(ModelViewSet):
    """
    Pass ?single=true to get single photos
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfilePhotoSerializer

    def get_object(self):
        profile = self.kwargs.get('profile')
        if self.request.GET.get('uuid', None):
            try:
                obj = ProfilePhoto.objects.get(
                    profile__uuid=profile,
                    uuid=self.request.GET.get('uuid'),
                    is_active=True
                )

            except ProfilePhoto.DoesNotExist:
                obj = None
        else:
            try:
                obj = ProfilePhoto.objects.get(
                    profile__uuid=profile,
                    is_active=True,
                    is_primary=True
                )

            except ProfilePhoto.DoesNotExist:
                obj = None

        return obj

    def get_queryset(self):
        objs = ProfilePhoto.objects.filter(profile__uuid=self.kwargs.get('profile', None)).actives()
        return objs

    def list(self, request, *args, **kwargs):
        if 'single' in request.GET:
            queryset = self.get_object()
            serializer = self.get_serializer(queryset)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().profile.account:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().profile.account:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
