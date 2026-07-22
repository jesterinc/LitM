#backend/charatcers/api/views.py
from django.db import models

# Create your models here.
from django.db import models
from users.models import PlayerProfile
from campaigns.models import Campaign
import uuid

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='characters')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)
    concept = models.TextField(blank=True, help_text="Concetto del personaggio")
    promise_marks = models.IntegerField(default=0) # Le 5 caselle da marcare
    quintessence_1 = models.CharField(max_length=100, blank=True)
    quintessence_2 = models.CharField(max_length=100, blank=True)
    quintessence_3 = models.CharField(max_length=100, blank=True)
    quintessence_4 = models.CharField(max_length=100, blank=True)
    backpack = models.JSONField(default=list, blank=True) # Lista di stringhe
    notes = models.JSONField(default=list, blank=True)     # Lista di stringhe
    fellowship_theme_notes = models.JSONField(default=list, blank=True) # 8 righe
    quest_notes = models.JSONField(default=list, blank=True)            # 4 righe
    abandon_milestone_marks = models.IntegerField(default=0) # 3 caselle
    improve_milestone_marks = models.IntegerField(default=0) # 3 caselle
    special_improvements = models.JSONField(default=list, blank=True)   # 15 righe
    history = models.TextField(blank=True)
    portrait_url = models.CharField(max_length=255, blank=True) # Percorso relativo per l'immagine
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.name

class FellowshipRelation(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='fellowship_relations')
    companion_name = models.CharField(max_length=100)
    relationship_tag = models.CharField(max_length=100)


class ThemeCard(models.Model):
    CARD_TYPES = [
        ('CIRCUMSTANCE', 'Circumstance'),
        ('COMPANION', 'Companion'),
        ('DEVOTION', 'Devotion'),
        ('DUTY', 'Duty'),
        ('KNOWLEDGE', 'Knowledge'),
        ('MAGIC', 'Magic'),
        ('MONSTROSITY', 'Monstrosity'),
        ('PAST', 'Past'),
        ('PEOPLE', 'People'),
        ('PERSONALITY', 'Personality'),
        ('POSSESSIONS', 'Possessions'),
        ('PRODIGIOUS_ABILITY', 'Prodigious Ability'),
        ('RELIC', 'Relic'),
        ('SKILL_OR_TRADE', 'Skill or Trade'),
        ('TRAIT', 'Trait'),
        ('UNCANNY_BEING', 'Uncanny Being'),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='theme_cards', null=True, blank=True)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, default='CIRCUMSTANCE')
    type_name = models.CharField(max_length=100, blank=True, help_text="Es: 'La Spada del Nonno' o 'Occhio Notturno'")
    notes_main = models.JSONField(default=list, blank=True)
    notes_secondary = models.JSONField(default=list, blank=True)
    quest_notes = models.JSONField(default=list, blank=True)
    abandon_marks = models.IntegerField(default=0)
    improve_marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_card_type_display()}: {self.type_name}"

class Tag(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='tags')
    number = models.IntegerField() # Da 1 a 6
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('character', 'number')
