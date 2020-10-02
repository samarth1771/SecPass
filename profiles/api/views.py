from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from profiles.models import UserProfile
# from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    # renderer_classes = (JSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = UserProfile.objects.select_related('user').get(
                user__username=username
            )
        except UserProfile.DoesNotExist:
            raise

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = []
    permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = ProfileSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     # serializer_data = request.data.get('user', {})
    #     serializer_data = request.data
    #
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
