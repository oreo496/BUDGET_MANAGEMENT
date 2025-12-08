from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # Filter by authenticated user
        # user_id = self.request.user.id  # Would need custom auth
        return Transaction.objects.all()

    @action(detail=True, methods=['post'])
    def flag_fraud(self, request, pk=None):
        """Flag a transaction as potential fraud."""
        transaction = self.get_object()
        transaction.flagged_fraud = True
        transaction.save()
        return Response({'message': 'Transaction flagged as fraud'})

