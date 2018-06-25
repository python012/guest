from django.contrib.auth.models import Group, User
from django.shortcuts import render
from rest_framework import viewsets

from sign.models import Event, Guest
from sign.serializers import (EventSerializer, GroupSerializer, GuestSerializer,
                             UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class GuestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows guests to viewed or edited.
    """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
