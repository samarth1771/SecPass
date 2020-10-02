from rest_framework import serializers

from profiles.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    user_id = serializers.CharField(source='user.pk')
    profile_id = serializers.CharField(source='user.profile.pk')
    profile_image = serializers.ImageField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'user_id',
            'profile_id',
            'profile_image',
            'created_at',
            'updated_at',
        ]

        # read_only_fields = ('userid', 'profileid')
