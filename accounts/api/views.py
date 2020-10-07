from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import views
from rest_framework.utils import json

from accounts.models import User
from .serializers import LoginSerializer, UserSerializer, ChangePasswordSerializer


# To create a new user with a password , create method defined in UserSerializer
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    # permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': self.request})
        # print("Request DATA", self.request)
        if serializer.is_valid():
            user = serializer.save()
            # print("Serializer DATA", serializer.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class LoginAPIView(views.APIView):
    permission_classes = [AllowAny]
    # permission_classes = []
    # renderer_classes = JSONRenderer
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        userid = serializer.validated_data.pk
        email = serializer.data['email']
        # username = serializer.data['username']
        token = serializer.data['token']
        host = request.get_host()
        # This is fetched from user model side with using related name (which we created in UserProfile model)
        profile_id = serializer.validated_data.profile.pk
        try:
            profile_image = serializer.validated_data.profile.profile_image.url
        except:
            profile_image = None

        return Response(data={
            "userid": userid,
            "email": email,
            # 'username': username,
            'profile_id': profile_id,
            'profile_image': host + profile_image,
            'token': token

        }, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = []
    permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

    # def retrieve(self, request, *args, **kwargs):
    #     # There is nothing to validate or save here. Instead, we just want the
    #     # serializer to handle turning our `User` object into something that
    #     # can be JSON field and sent to the client.
    #     serializer = self.serializer_class(request.user)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def update(self, request, *args, **kwargs):
    #     # serializer_data = request.data.get('user', {})
    #     # serializer_data = request.data
    #
    #     user_data = request.data.get('user', {})
    #
    #     serializer_data = {
    #         'username': user_data.get('username', request.user.username),
    #         'email': user_data.get('username', request.user.email),
    #         'profile':{
    #             'profile_image': user_data.get('profile_image',request.user.profile.profile_image)
    #         }
    #     }
    #     # Here is that serialize, validate, save pattern we talked about
    #     # before.
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     # return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response({"message": "User Updated Successfully"}, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
