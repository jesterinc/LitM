#backend/campaigns/api/serializers.py
from rest_framework import serializers
from campaigns.models import Campaign, CampaignMember
from users.models import PlayerProfile

class CampaignMemberSerializer(serializers.ModelSerializer):
    player_username = serializers.CharField(source='player.user.username', read_only=True)

    class Meta:
        model = CampaignMember
        fields = ['id', 'player', 'player_username', 'role', 'joined_at']

class CampaignSerializer(serializers.ModelSerializer):
    storyteller_username = serializers.CharField(source='storyteller.user.username', read_only=True)
    members = CampaignMemberSerializer(many=True, read_only=True)

    # Calcoliamo i posti liberi dinamicamente
    slots_left = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        # AGGIUNGIAMO I NUOVI CAMPI ALLA LISTA
        fields = [
            'id', 'title', 'description', 'storyteller', 'storyteller_username',
            'members', 'is_active', 'status', 'max_players', 'slots_left', 'created_at'
        ]
        read_only_fields = ['storyteller', 'created_at']

    def get_slots_left(self, obj):
        # Assumendo che tu abbia aggiunto max_players al modello
        current_members = obj.members.count()
        return max(0, obj.max_players - current_members)
