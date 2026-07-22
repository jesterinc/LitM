#backend/charatcers/models.py
from django.db import models

# Create your models here.
from characters.models import Character
import uuid

class DiceRoll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='dice_rolls')
    dice_type = models.CharField(max_length=10, default='d6') # Es: d6, d10
    num_dice = models.IntegerField(default=1)
    modifier = models.IntegerField(default=0)
    raw_results = models.JSONField(default=list) # Es: [3, 5, 1]
    total = models.IntegerField()
    success_level = models.CharField(max_length=20, blank=True) # Es: "Critical", "Success", "Fail"
    description = models.TextField(blank=True) # Cosa stava facendo il PG
    tags_applied = models.JSONField(default=list, blank=True) # Quali tag hanno influenzato il tiro
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Tiro di {self.character.name}: {self.total}"
