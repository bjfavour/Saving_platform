from rest_framework import serializers
from .models import Payment, Cashout
from .services import process_cashout_request
import os

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["status", "user"]

    def validate_slip(self, file):

        # 5MB limit
        max_size = 5 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError("File must not exceed 5MB.")

        # Allowed file types
        valid_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in valid_extensions:
            raise serializers.ValidationError(
                "Only PDF, JPG, JPEG, PNG files are allowed."
            )

        return file


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