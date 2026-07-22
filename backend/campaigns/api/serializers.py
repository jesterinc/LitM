#backend/campaigns/api/serializers.py
from rest_framework import serializers
from campaigns.models import Campaign, CampaignMember
from users.models import PlayerProfile
from users.api.serializers import PlayerSerializer

class CampaignMemberSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.PrimaryKeyRelatedField(queryset=PlayerProfile.objects.all(), source='player', write_only=True)

    class Meta:
        model = CampaignMember
        fields = ['id', 'player', 'player_id', 'role']

class CampaignSerializer(serializers.ModelSerializer):
    storyteller_username = serializers.CharField(source='storyteller.user.username', read_only=True)
    members = CampaignMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'storyteller', 'storyteller_username', 'members', 'is_active', 'created_at']
        read_only_fields = ['storyteller']
