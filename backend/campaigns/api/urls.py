#backend/campaigns/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from campaigns.api.views import CampaignViewSet, CampaignMemberViewSet

router = DefaultRouter()
router.register(r'', CampaignViewSet, basename='campaign')

urlpatterns = [
  path('', include(router.urls)),
  path('<uuid:campaign_pk>/members/',CampaignMemberViewSet.as_view({'get': 'list','post': 'create'}),name='campaign-members-list'),
  path('<uuid:campaign_pk>/members/<int:pk>/',CampaignMemberViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}),name='campaign-members-detail'),
]
