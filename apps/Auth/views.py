import re
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
from rest_framework.exceptions import PermissionDenied

from .models import Profile, EmergencyContacts, ComplaintsForm, Comment
from .serializers import RegisterSerializer, \
    MyTokenObtainPairSerializer, ProfileSerializer, \
    ProfileSerializerGet, EmergencyContactsSerializer, ComplaintsFormSerializer, CommentSerializer
from rest_framework import generics, status


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileViewPost(generics.ListCreateAPIView):
    queryset = Profile.objects
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        data._mutable = True
        data['user'] = user.id
        serializer = ProfileSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     try:
    #         serializer.save(user=self.request.user)
    #     except IntegrityError:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_queryset(self):
    #     return self.queryset.filter()


class ProfileViewUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializerGet
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Profile.objects
    lookup_field = 'user_id'


class ProfileViewGet(generics.ListAPIView):
    serializer_class = ProfileSerializerGet
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Profile.objects
    pagination_class = None

    def get_queryset(self):
        owner = self.request.user
        profile_owner = User.objects.get(username=owner)
        return self.queryset.filter(user=profile_owner)


def logout_view(request):
    logout(request)
    return ''


class EmergencyContactsView(generics.ListCreateAPIView):
    queryset = EmergencyContacts.objects
    serializer_class = EmergencyContactsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ComplaintsFormView(generics.ListCreateAPIView):
    queryset = ComplaintsForm.objects
    serializer_class = ComplaintsFormSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UpdateComplaintsForm(generics.UpdateAPIView):
    queryset = ComplaintsForm.objects
    serializer_class = ComplaintsFormSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'id'
    pagination_class = None


class DeleteComplaintsForm(generics.DestroyAPIView):
    queryset = ComplaintsForm.objects
    serializer_class = ComplaintsFormSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    lookup_field = 'id'
    pagination_class = None


class DetailComplaintsForm(generics.RetrieveAPIView):
    """
    Details of products by a user
    """
    queryset = ComplaintsForm.objects.all()
    model = ComplaintsForm
    serializer_class = ComplaintsFormSerializer
    lookup_field = 'id'


class CommentFormView(generics.ListCreateAPIView):
    queryset = Comment.objects
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = None

    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['id'])
        if not profile.is_official:
            raise PermissionDenied("Not Authorized")
        serializer.save(profile=profile)

    def get_queryset(self):
        return self.queryset.filter(profile=self.kwargs['id'])

