from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """ Serializes an user object """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """ Serializes an user object for making registrations """
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data
        ['username'], validated_data['email'], validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):
    """ Serializes login details """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        check_user = User.objects.filter(email=data['email']).first()
        if check_user is None:
            raise serializers.ValidationError("Incorrect Credentials")
        username = check_user.username
        user = authenticate(username=username, password=data['password'])
        # user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")