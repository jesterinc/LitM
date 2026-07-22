#backend/users/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import MeView, PasswordRecoverView, PlayerViewSet, RegisterView, StorytellerViewSet
from users.api.views import RegisterView, LoginView

router = DefaultRouter()
router.register(r'storytellers', StorytellerViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('recover-password/', PasswordRecoverView.as_view(), name='recover-password'),
]
