from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Account


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    adjustments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'starting_balance', 'current_balance', 'account_resets', 'adjustments']
