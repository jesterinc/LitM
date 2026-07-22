#backend/campaigns/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaigns.api.views import CampaignViewSet, CampaignMemberViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('campaigns/<uuid:campaign_pk>/members/', CampaignMemberViewSet.as_view({'get': 'list', 'post': 'create'})),
]
