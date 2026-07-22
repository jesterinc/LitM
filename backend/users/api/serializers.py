#backend/users/api/serializers.py
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from users.models import StorytellerProfile, PlayerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class StorytellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StorytellerProfile
        fields = ['id', 'user', 'token_uuid', 'bio']


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PlayerProfile
        fields = ['id', 'user', 'token_uuid']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('player', 'Player'), ('storyteller', 'Storyteller')])
    email = serializers.EmailField(required=False) # <--- RENDILO OPZIONALE

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):

        role = validated_data.pop('role')
        email = validated_data.get('email', '') # <--- USA .get() PER EVITARE KEYERROR
        user = User.objects.create_user(
            username=validated_data['username'],
            email=email,
            password=validated_data['password']
        )

        if role == 'storyteller':

            StorytellerProfile.objects.create(user=user)

        else:

            PlayerProfile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        username = data.get('username')
        password = data.get('password')

        if username and password:

            user = authenticate(username=username, password=password)

            if not user:

                raise serializers.ValidationError("Credenziali non valide.")

        else:

            raise serializers.ValidationError("Devi inserire username e password.")

        data['user'] = user

        return data
