#backend/charatcers/api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from game_engine.models import DiceRoll
from characters.models import Character
from game_engine.logic import resolve_action

class DiceRollViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):

        character_id = request.data.get('character_id')
        num_dice = request.data.get('num_dice', 1)
        modifier = request.data.get('modifier', 0)
        tags = request.data.get('tags', [])
        description = request.data.get('description', '')

        try:

            character = Character.objects.get(id=character_id, player__user=request.user)

        except Character.DoesNotExist:

            return Response({"error": "Personaggio non trovato"}, status=status.HTTP_404_NOT_FOUND)

        result = resolve_action(num_dice, modifier, tags)
        roll_instance = DiceRoll.objects.create(
            character=character,
            num_dice=num_dice,
            modifier=modifier,
            raw_results=result['rolls'],
            total=result['final_total'],
            success_level=result['success_level'],
            description=description,
            tags_applied=tags
        )

        return Response({
            "roll_id": str(roll_instance.id),
            "result": result
        }, status=status.HTTP_201_CREATED)
