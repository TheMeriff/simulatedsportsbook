from rest_framework import serializers

from simulated_sportsbook.models import Betslip


class BetslipSerializer(serializers.HyperlinkedModelSerializer):
    event = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user_account = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Betslip
        fields = [
            'id',
            'user_account',
            'event',
            'type_of_bet',
            'predicted_outcome',
            'stake',
            'profit',
            'total_return',
            'processed_ticket',
            'winning_ticket'
        ]
