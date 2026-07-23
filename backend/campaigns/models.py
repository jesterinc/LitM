from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.models import StorytellerProfile, PlayerProfile
import uuid

class Campaign(models.Model):
    STATUS_CHOICES = [
      ('RECRUITING', 'In Reclutamento'),
      ('STARTED', 'Aavviata'),
      ('PAUSED', 'In Pausa'),
      ('CONCLUDED', 'Conclusa'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    storyteller = models.ForeignKey(StorytellerProfile, on_delete=models.CASCADE, related_name='created_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECRUITING')
    max_players = models.IntegerField(default=5, help_text="Numero minimo di giocatori per poter partire")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def slots_left(self):

        current_members = self.members.count()
        return max(0, self.max_players - current_members)

class CampaignMember(models.Model):
    ROLE_CHOICES = [
        ('player', 'Giocatore'),
        ('observer', 'Osservatore'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='members')
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='campaign_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'player')

    def __str__(self):
        return f"{self.player.user.username} in {self.campaign.title}"
