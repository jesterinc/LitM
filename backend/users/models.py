#backend/users/models.py
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid

class StorytellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='storyteller_profile')
    token_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Narratore: {self.user.username}"

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    token_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Giocatore: {self.user.username}"
