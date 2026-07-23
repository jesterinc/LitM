#backend/charatcers/api/serializers.py
from rest_framework import serializers
from characters.models import Character, ThemeCard, FellowshipRelation, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['number', 'description']


class FellowshipRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FellowshipRelation
        fields = ['companion_name', 'relationship_tag']


class ThemeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeCard
        fields = [
            'id', 'card_type', 'type_name', 'description', 'sentiment',
            'quest', 'tracks', 'special_improvements'
        ]


class CharacterSerializer(serializers.ModelSerializer):
    theme_cards = ThemeCardSerializer(many=True, read_only=True)
    fellowship_relations = FellowshipRelationSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    player_username = serializers.CharField(source='player.user.username', read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 'name', 'player', 'player_username', 'campaign',
            'concept', 'promise', 'promise_marks', 'quintessence',
            'backpack', 'notes',
            'fellowship_theme_title', 'fellowship_theme_desc', 'fellowship_quest',
            'fellowship_tracks', 'fellowship_rags_lines', 'fellowship_special_improvements',
            'history', 'portrait_url', 'created_at', 'updated_at',
            'theme_cards', 'fellowship_relations', 'tags'
        ]
        read_only_fields = ['player', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Assegna automaticamente il personaggio al giocatore loggato
        request = self.context.get('request')
        if request and hasattr(request.user, 'player_profile'):
            validated_data['player'] = request.user.player_profile
        return super().create(validated_data)
