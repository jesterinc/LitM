#backend/charatcers/api/views.py
from rest_framework import viewsets, permissions
from characters.models import Character
from characters.api.serializers import CharacterSerializer

class IsOwnerOrStoryteller(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.player.user == request.user:

            return True

        if obj.campaign and obj.campaign.storyteller.user == request.user:

            return True

        return False

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStoryteller]

    queryset = Character.objects.all()

    def get_queryset(self):

        user = self.request.user
        qs = Character.objects.filter(player__user=user)

        if hasattr(user, 'storyteller_profile'):

            campaigns_narrated = user.storyteller_profile.created_campaigns.values_list('id', flat=True)
            qs = qs | Character.objects.filter(campaign__id__in=campaigns_narrated)

        return qs.distinct()
