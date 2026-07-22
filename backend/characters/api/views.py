#backend/charatcers/api/views.py
from rest_framework import viewsets, permissions

from characters.models import Character
from users.models import PlayerProfile

from characters.api.serializers import CharacterSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()

    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        if hasattr(user, 'player_profile'):
            return Character.objects.filter(player=user.player_profile)
        return Character.objects.none()

    def perform_create(self, serializer):

        player = PlayerProfile.objects.get(user=self.request.user)
        serializer.save(player=player)
