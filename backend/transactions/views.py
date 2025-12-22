from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return Transaction.objects.filter(user=user).order_by('-date', '-created_at')
        return Transaction.objects.none()

    def perform_create(self, serializer):
        # Default to MANUAL source if not provided
        data = serializer.validated_data
        if not data.get('source'):
            serializer.save(user=self.request.user, source='MANUAL')
        else:
            serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def flag_fraud(self, request, pk=None):
        """Flag a transaction as potential fraud."""
        transaction = self.get_object()
        transaction.flagged_fraud = True
        transaction.save()
        return Response({'message': 'Transaction flagged as fraud'})

