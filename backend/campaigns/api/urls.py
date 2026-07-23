#backend/campaigns/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaigns.api.views import CampaignViewSet, CampaignMemberViewSet

router = DefaultRouter()

# 1. Registriamo le campagne alla radice ('') perché l'include principale ha già 'campaigns/'
router.register(r'', CampaignViewSet, basename='campaign')

# 2. Registriamo i membri (opzionale, se vuoi usarli via router)
router.register(r'members', CampaignMemberViewSet, basename='campaign-member')

urlpatterns = [
    path('', include(router.urls)),
]
