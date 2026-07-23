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
    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        
        request = self.context['request']

        if validated_data.get('entity_type') == 'PC':

            if hasattr(request.user, 'player_profile'):

                validated_data['player'] = request.user.player_profile

        return super().create(validated_data)