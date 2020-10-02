from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User  # , Profile
from datetime import datetime, timedelta

# from profiles.api.serializers import ProfileSerializer
from profiles.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'token',
            'created_at',
            'expires',
        ]

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)

    def get_expires(self, obj):
        return datetime.now() + timedelta(days=7)

    def get_created_at(self, obj):
        return datetime.now()


class LoginSerializer(serializers.Serializer):
    userid = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    # profile = ProfileSerializer(read_only=True)

    # class Meta:
    #     model = User
    #     fields = [
    #         'userid'
    #         'username'
    #         'email',
    #         'token',
    #         'profile.profile_image',
    #         'profile.pk'
    #     ]

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
    profile_id = serializers.SerializerMethodField(read_only=True, required=False)
    profile_image = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password',
                  'token',
                  'profile_id',
                  'profile_image',
                  ]

        read_only_fields = ('token',)

    def get_profile_id(self, obj):
        print("DEBUG: profile id", obj.profile.pk)
        return obj.profile.pk

    def get_profile_image(self, obj):
        print("DEBUG: profile id", obj.profile.profile_image.url)
        return obj.profile.profile_image.url

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        for (key, value) in profile_data.items():
            # We're doing the same thing as above, but this time we're making
            # changes to the Profile model.
            setattr(instance.profile, key, value)

        # Save the profile just like we saved the user.
        instance.profile.save()

        return instance
