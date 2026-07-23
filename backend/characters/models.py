#backend/charatcers/api/views.py
# backend/characters/models.py
from django.db import models
from users.models import PlayerProfile
from campaigns.models import Campaign
import uuid

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='characters')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='characters')
    concept = models.TextField(blank=True, help_text="Concetto del personaggio")
    promise = models.TextField(blank=True, help_text="La promessa del personaggio") # NUOVO
    promise_marks = models.IntegerField(default=0, help_text="Da 0 a 5")
    quintessence = models.IntegerField(default=0, help_text="Da 0 a 5") # SOSTITUISCE i 4 campi separati
    backpack = models.JSONField(default=list, blank=True, help_text="Lista di oggetti: [{name, qty}]")
    notes = models.TextField(blank=True) # SEMPLIFICATO in testo libero per ora
    fellowship_theme_title = models.CharField(max_length=100, blank=True)
    fellowship_theme_desc = models.TextField(blank=True)
    fellowship_quest = models.TextField(blank=True)
    fellowship_tracks = models.JSONField(default=dict, blank=True, help_text="{'abandon': 0, 'improve': 0, 'milestone': 0}")
    fellowship_rags_lines = models.JSONField(default=list, blank=True, help_text="[{'text': '', 'type': 'slash'}]")
    fellowship_special_improvements = models.JSONField(default=list, blank=True)
    history = models.TextField(blank=True)
    portrait_url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FellowshipRelation(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='fellowship_relations')
    companion_name = models.CharField(max_length=100)
    relationship_tag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.character.name} -> {self.companion_name}"

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

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='theme_cards')
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, default='CIRCUMSTANCE')
    type_name = models.CharField(max_length=100, blank=True, help_text="Titolo specifico del tema")
    description = models.TextField(blank=True, help_text="Descrizione positiva o negativa")
    sentiment = models.CharField(max_length=10, default='neutral', choices=[('positive', 'Positivo'), ('negative', 'Negativo'), ('neutral', 'Neutro')])
    quest = models.TextField(blank=True)
    tracks = models.JSONField(default=dict, blank=True, help_text="{'abandon': 0, 'improve': 0}")
    special_improvements = models.JSONField(default=list, blank=True, help_text="Lista di miglioramenti speciali")

    def __str__(self):
        return f"{self.get_card_type_display()}: {self.type_name}"

class Tag(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='tags')
    number = models.IntegerField() # Da 1 a 6
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('character', 'number')
