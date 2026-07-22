#backend/charatcers/api/serializers.py
from rest_framework import serializers
from characters.models import Character, FellowshipRelation, ThemeCard, Tag

class FellowshipRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FellowshipRelation
        fields = ['id', 'companion_name', 'relationship_tag']

class ThemeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeCard
        fields = [
            'id', 'card_type', 'type_name',
            'notes_main', 'notes_secondary',
            'quest_notes', 'abandon_marks', 'improve_marks'
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'number', 'description']

class CharacterSerializer(serializers.ModelSerializer):
    fellowship_relations = FellowshipRelationSerializer(many=True, required=False)
    theme_cards = ThemeCardSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    player_name = serializers.CharField(source='player.user.username', read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 'name', 'concept', 'promise_marks',
            'quintessence_1', 'quintessence_2', 'quintessence_3', 'quintessence_4',
            'backpack', 'notes',
            'fellowship_theme_notes', 'quest_notes',
            'abandon_milestone_marks', 'improve_milestone_marks',
            'special_improvements',
            'history', 'portrait_url',
            'player', 'player_name', 'campaign',
            'fellowship_relations', 'theme_cards', 'tags'
        ]
        read_only_fields = ['player']

    def create(self, validated_data):

        relations_data = validated_data.pop('fellowship_relations', [])
        themes_data = validated_data.pop('theme_cards', [])
        tags_data = validated_data.pop('tags', [])
        character = Character.objects.create(**validated_data)

        for relation_data in relations_data:

            FellowshipRelation.objects.create(character=character, **relation_data)

        for theme_data in themes_data:

            ThemeCard.objects.create(character=character, **theme_data)

        for tag_data in tags_data:

            Tag.objects.create(character=character, **tag_data)

        return character

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.concept = validated_data.get('concept', instance.concept)
        instance.promise_marks = validated_data.get('promise_marks', instance.promise_marks)
        instance.quintessence_1 = validated_data.get('quintessence_1', instancce.quintessence_1)
        instance.quintessence_2 = validated_data.get('quintessence_2', instancce.quintessence_2)
        instance.quintessence_3 = validated_data.get('quintessence_3', instancce.quintessence_3)
        instance.quintessence_4 = validated_data.get('quintessence_4', instancce.quintessence_4)
        instance.backpack = validated_data.get('backpack', instancce.backpack)
        instance.notes = validated_data.get('notes', instancce.notes)
        instance.fellowship_theme_notes = validated_data.get('fellowship_theme_notes', instancce.fellowship_theme_notes)
        instance.quest_notes = validated_data.get('quest_notes', instancce.quest_notes)
        instance.abandon_milestone_marks = validated_data.get('abandon_milestone_marks', instancce.abandon_milestone_marks)
        instance.improve_milestone_marks = validated_data.get('improve_milestone_marks', instancce.improve_milestone_marks)
        instance.special_improvements = validated_data.get('special_improvements', instancce.special_improvements)
        instance.history = validated_data.get('history', instancce.history)
        instance.portrait_url = validated_data.get('portrait_url', instancce.portrait_url)
        instance.save()

        if 'fellowship_relations' in validated_data:

            instance.fellowship_relations.all().delete()

            for relation_data in validated_data['fellowship_relations']:

                FellowshipRelation.objects.create(character=instance, **relation_data)


        if 'theme_cards' in validated_data:

            instance.theme_cards.all().delete()

            for theme_data in validated_data['theme_cards']:

                ThemeCard.objects.create(character=instance, **theme_data)


        if 'tags' in validated_data:

            instance.tags.all().delete()

            for tag_data in validated_data['tags']:

                Tag.objects.create(character=instance, **tag_data)

        return instance
