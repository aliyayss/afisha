from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8)

    def validate_username(self, username):

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def create(self, validated_data):

        password = validated_data.get('password')
        user = User(username=validated_data.get('username'))
        user.set_password(password)
        user.save()
        user.generate_verification_code()
        return user


class UserVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('verification_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('User not found')
        if user.verification_code != code:
            raise ValidationError('Invalid verification code')
        user.is_active = True
        user.verification_code = None
        user.save()
        return {'message': 'User successfully activated'}

