#backend/users/api/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from characters.models import Character
from users.models import StorytellerProfile, PlayerProfile
from users.api.serializers import StorytellerSerializer, PlayerSerializer, UserSerializer, RegisterSerializer, LoginSerializer

class StorytellerViewSet(viewsets.ModelViewSet):
    queryset = StorytellerProfile.objects.all()
    serializer_class = StorytellerSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):

    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Crea l'utente e il profilo associato
        user = serializer.save()

        # Recupera il profilo appena creato per ottenere il token
        profile = None
        role = request.data.get('role')

        if role == 'storyteller':
            profile = user.storyteller_profile
        else:
            profile = user.player_profile

        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "token_uuid": str(profile.token_uuid),
            "role": role
        }, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        profile = None
        role = None

        if hasattr(user, 'storyteller_profile'):

            profile = user.storyteller_profile
            role = 'storyteller'

        elif hasattr(user, 'player_profile'):

            profile = user.player_profile
            role = 'player'

        return Response({
            "user": {"username": user.username, "email": user.email},
            "token_uuid": str(profile.token_uuid),
            "role": role
        })


class PasswordRecoverView(APIView):
    permission_classes = [] # Chiunque può provare a recuperare

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # Qui andrebbe la logica per inviare una mail con un link di reset
            # Per ora simuliamo il successo
            return Response({"message": f"Istruzioni inviate a {email}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Per sicurezza, non riveliamo se l'email esiste o meno
            return Response({"message": "Se l'account esiste, riceverai istruzioni."}, status=status.HTTP_404_NOT_FOUND)


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        profile = None
        role = None

        if hasattr(user, 'storyteller_profile'):

            profile = user.storyteller_profile
            role = 'storyteller'

        elif hasattr(user, 'player_profile'):

            profile = user.player_profile
            role = 'player'

        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "token_uuid": str(profile.token_uuid),
            "role": role
        })
