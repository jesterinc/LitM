#backend/charatcers/api/urls.py
from django.urls import path
from game_engine.api.views import DiceRollViewSet

urlpatterns = [
    path('roll/', DiceRollViewSet.as_view({'post': 'create'}), name='dice-roll'),
]
