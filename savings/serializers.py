from rest_framework import serializers
from .models import Payment, Cashout
from .services import process_cashout_request


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["status", "user"]

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Invalid month.")
        return value


class CashoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cashout
        fields = "__all__"
        read_only_fields = [
            "status",
            "user",
            "fee_percentage",
            "fee_amount",
            "net_amount",
            "total_savings_snapshot"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        requested_amount = validated_data["requested_amount"]

        return process_cashout_request(user, requested_amount)