from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from simulated_sportsbook.models import Event, Betslip
from simulated_sportsbook.rest_api.serializers.betslip_serializer import BetslipSerializer
from simulated_sportsbook.rest_api.serializers.event_serializer import EventSerializer
from simulated_sportsbook.rest_api.serializers.user_serializer import UserSerializer, AccountSerializer
from users.models import Account


class BaseViewSet(GenericViewSet):
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    lookup_field = 'id'


class AllMethodsViewSet(BaseViewSet,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(AllMethodsViewSet):
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventViewSet(AllMethodsViewSet):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class BetslipViewSet(AllMethodsViewSet):
    queryset = Betslip.objects.all().order_by('-id')
    serializer_class = BetslipSerializer
    permission_classes = [permissions.IsAuthenticated]

