from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobApplication


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password1'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('first_name', 'last_name')


class ConfirmApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('confirmed',)
