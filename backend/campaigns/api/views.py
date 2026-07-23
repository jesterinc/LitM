# backend/campaigns/api/views.py
from rest_framework import viewsets, permissions
from campaigns.models import Campaign, CampaignMember
from campaigns.api.serializers import CampaignSerializer, CampaignMemberSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet per la gestione delle Campagne.
    - GET: Lista campagne filtrate per utente (Narratore o Giocatore)
    - POST: Creazione nuova campagna (solo Narratori)
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Se è un Narratore, vede le sue campagne
        if hasattr(user, 'storyteller_profile'):
            return Campaign.objects.filter(storyteller=user.storyteller_profile)

        # Se è un Giocatore, vede le campagne a cui è iscritto
        elif hasattr(user, 'player_profile'):
            return Campaign.objects.filter(members__player=user.player_profile)

        return Campaign.objects.none()

    def perform_create(self, serializer):
        """
        Assegna automaticamente lo storyteller corrente alla nuova campagna.
        """
        user = self.request.user

        if not hasattr(user, 'storyteller_profile'):
            raise permissions.PermissionDenied("Solo gli utenti con profilo Narratore possono creare campagne.")

        # Salviamo UNA SOLA VOLTA passando lo storyteller
        serializer.save(storyteller=user.storyteller_profile)


class CampaignMemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet per gestire i membri di una specifica campagna.
    """
    serializer_class = CampaignMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Recupera l'ID della campagna dall'URL (nested router o query param)
        campaign_id = self.kwargs.get('campaign_pk') or self.request.query_params.get('campaign')

        if campaign_id:
            return CampaignMember.objects.filter(campaign_id=campaign_id)

        return CampaignMember.objects.none()

    def perform_create(self, serializer):
        """
        Assicura che il membro venga associato alla campagna corretta.
        """
        campaign_id = self.kwargs.get('campaign_pk') or self.request.data.get('campaign')
        if campaign_id:
            serializer.save(campaign_id=campaign_id)
        else:
            raise permissions.ValidationError("È necessario specificare una campagna.")
