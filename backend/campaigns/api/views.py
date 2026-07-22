#backend/campaigns/api/views.py
from rest_framework import viewsets, permissions
from campaigns.models import Campaign, CampaignMember
from campaigns.api.serializers import CampaignSerializer, CampaignMemberSerializer
from users.models import StorytellerProfile

class CampaignViewSet(viewsets.ModelViewSet):
    # Aggiunto queryset base per il Router
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if hasattr(user, 'storyteller_profile'):

            return Campaign.objects.filter(storyteller=user.storyteller_profile)

        elif hasattr(user, 'player_profile'):

            return Campaign.objects.filter(members__player=user.player_profile)

        return Campaign.objects.none()

    def perform_create(self, serializer):

        storyteller = StorytellerProfile.objects.get(user=self.request.user)
        serializer.save(storyteller=storyteller)

class CampaignMemberViewSet(viewsets.ModelViewSet):
    queryset = CampaignMember.objects.all()
    serializer_class = CampaignMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        campaign_id = self.kwargs.get('campaign_pk')

        if campaign_id:

            return CampaignMember.objects.filter(campaign_id=campaign_id)

        return CampaignMember.objects.none()
