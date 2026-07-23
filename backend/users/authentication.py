# users/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User, PlayerProfile, StorytellerProfile

class UUIDTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_X_UUID_TOKEN')

        if not token:
            return None

        try:
            # 1. Prova a cercare nel PlayerProfile
            try:
                player_profile = PlayerProfile.objects.get(token_uuid=token)
                return (player_profile.user, None)
            except PlayerProfile.DoesNotExist:
                pass

            # 2. Se non c'è, prova nello StorytellerProfile
            try:
                storyteller_profile = StorytellerProfile.objects.get(token_uuid=token)
                return (storyteller_profile.user, None)
            except StorytellerProfile.DoesNotExist:
                pass

            # 3. Se non è in nessuno dei due, il token non è valido
            raise AuthenticationFailed('Invalid token.')

        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')
