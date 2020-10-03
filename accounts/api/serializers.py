from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User  # , Profile
from datetime import datetime, timedelta

from profiles.api.serializers import ProfileSerializer
from profiles.models import UserProfile


class LoginSerializer(serializers.Serializer):
    userid = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    # profile = ProfileSerializer(read_only=True)

    def validate(self, data):
        # request = self.context.get('request')
        # print("DEBUG request Context", request)
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)
        # print("DEBUG", user)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # profile = ProfileSerializer(required=True)
    profile_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password',
                  'token',
                  'profile_id',
                  'profile_image',
                  ]

        read_only_fields = ['token', 'profile_id', 'profile_image']

    def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def get_profile_id(self, obj):
        return obj.profile.pk

    def get_profile_image(self, obj):
        request = self.context.get('request')
        # return request.build_absolute_uri('/') + obj.profile.profile_image.url
        return request.get_host() + obj.profile.profile_image.url

