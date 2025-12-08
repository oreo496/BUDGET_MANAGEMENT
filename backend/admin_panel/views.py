from rest_framework import viewsets
from .models import SystemLog, AdminAction
from .serializers import SystemLogSerializer, AdminActionSerializer


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SystemLogSerializer
    queryset = SystemLog.objects.all()


class AdminActionViewSet(viewsets.ModelViewSet):
    serializer_class = AdminActionSerializer
    queryset = AdminAction.objects.all()

