from rest_framework import viewsets
from .models import AIAlert
from .serializers import AIAlertSerializer


class AIAlertViewSet(viewsets.ModelViewSet):
    serializer_class = AIAlertSerializer

    def get_queryset(self):
        return AIAlert.objects.all()

