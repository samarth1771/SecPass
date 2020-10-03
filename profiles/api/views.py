from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView
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
    queryset = UserProfile.objects.all()
    lookup_field = 'user_id'


# class ProfileRetrieveAPIView(RetrieveAPIView):
#     permission_classes = [AllowAny]
#     # renderer_classes = (JSONRenderer,)
#     serializer_class = ProfileSerializer
#
#     def retrieve(self, request, username, *args, **kwargs):
#         try:
#             profile = UserProfile.objects.select_related('user').get(
#                 user__username=username
#             )
#         except UserProfile.DoesNotExist:
#             raise
#
#         serializer = self.serializer_class(profile)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = []
    permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user_id'




