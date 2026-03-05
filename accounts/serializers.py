from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_approved = False
        user.save()
        return user


class CustomLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username_or_phone = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username_or_phone).first() or \
               User.objects.filter(telephone=username_or_phone).first()

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_approved:
            raise serializers.ValidationError("Account not approved by admin.")

        return super().validate({
            "username": user.username,
            "password": password
        })
        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "telephone",
            "full_name",
            "address",
            "bank_name",
            "bank_account_number",
            "profile_picture",
        ]