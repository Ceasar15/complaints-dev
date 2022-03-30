from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.Auth.models import Profile, EmergencyContacts, ComplaintsForm


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    city = serializers.CharField(write_only=True, required=True)
    country = serializers.CharField(write_only=True, required=True)
    state = serializers.CharField(write_only=True, required=True)
    zip_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name',
                  'city', 'country', 'state', 'zip_code')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        profile = Profile.objects.create(
            user=user,
            city=validated_data['city'],
            country=validated_data['country'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "user", "city", "country", "state", "zip_code"
        ]

        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)


class ProfileSerializerGet(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            "user", "city", "country", "state",
            "first_name", "last_name", "username", "zip_code", "is_official"
        ]

        extra_kwargs = {
            'user': {'required': False}
        }

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user = validated_data['user']
        if 'city' in validated_data:
            instance.city = validated_data['city']
        if 'country' in validated_data:
            instance.country = validated_data['country']
        if 'state' in validated_data:
            instance.state = validated_data['state']
        if 'zip_code' in validated_data:
            instance.zip_code = validated_data['zip_code']
        if 'is_official' in validated_data:
            instance.is_official = validated_data['is_official']
        instance.save()
        return instance


class EmergencyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContacts
        fields = [
            "user", "state", "phone_number"
        ]

        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        return EmergencyContacts.objects.create(**validated_data)


class ComplaintsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintsForm
        fields = [
            "id", "police_department", "police_department_zip_code",
            "occured_time", "descriptions", "primary_reason", "race_of_officer",
            "phone_number", "upload_file", "were_you_arressted",
        ]

        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        return ComplaintsForm.objects.create(**validated_data)
