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
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    # permission_classes = [permissions.AllowAny]
    # We need to work on the request on serializers.py so we send request context to serializers with this method

    def get_serializer_context(self):
        return {'request': self.request}


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
        # print("DEBUG: ", serializer.validated_data.pk)
        # print("DEBUG: data", serializer.data['email'])
        userid = serializer.validated_data.pk
        email = serializer.data['email']
        username = serializer.data['username']
        token = serializer.data['token']
        # print(type(token))

        # This is fetched from user side with using related name (which we created in UserProfile model)
        profile_id = serializer.validated_data.profile.pk
        try:
            profile_image = serializer.validated_data.profile.profile_image.url
            # profile_image = serializer.validated_data.profile.get_image_uri()
        except:
            profile_image = None

        return Response(data={
            "userid": userid,
            "email": email,
            'username': username,
            'profile_id': profile_id,
            'profile_image': profile_image,
            'token': token

        }, status=status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    # permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserSerializer

    # queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSON field and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    # permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # serializer_data = request.data.get('user', {})
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "User Updated Successfully"}, status=status.HTTP_200_OK)
