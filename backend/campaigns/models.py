from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from users.models import StorytellerProfile, PlayerProfile
import uuid

class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    storyteller = models.ForeignKey(StorytellerProfile, on_delete=models.CASCADE, related_name='created_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

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
