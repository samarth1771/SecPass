from rest_framework import serializers
from profiles.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    # user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.pk', read_only=True)
    # profile_id = serializers.IntegerField(source='user.profile.pk', required=False)
    # profile_id = serializers.IntegerField()
    profile_id = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(max_length=None, use_url=True, read_only=False)

    class Meta:
        model = UserProfile
        fields = [
            'user_id',
            'username',
            'profile_id',
            'profile_image',
            'created_at',
            'updated_at',
        ]

    def get_profile_id(self, obj):
        # print("DEBUG: profile id", obj.profile.pk)
        return obj.pk
