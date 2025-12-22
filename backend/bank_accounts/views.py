from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import BankAccount
from .serializers import BankAccountSerializer
from transactions.models import Transaction
from categories.models import Category
from utils.plaid_service import (
    create_link_token,
    exchange_public_token,
    sync_transactions,
    get_account_info
)
import logging

logger = logging.getLogger(__name__)


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='plaid/create-link-token')
    def create_plaid_link_token(self, request):
        """
        Create a Plaid Link token for the user to connect their bank account.
        This token is used by Plaid Link on the frontend.
        """
        try:
            link_data = create_link_token(
                user_id=str(request.user.id),
                client_name='Funder Budget App'
            )
            return Response(link_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to create Plaid link token: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='plaid/exchange-token')
    def exchange_plaid_token(self, request):
        """
        Exchange a Plaid public token for an access token and create/update BankAccount.
        Called after user successfully links their account through Plaid Link.
        """
        public_token = request.data.get('public_token')
        account_id = request.data.get('account_id')
        metadata = request.data.get('metadata', {})
        
        if not public_token:
            return Response(
                {'error': 'public_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token_data = exchange_public_token(public_token)
            access_token = token_data['access_token']
            item_id = token_data['item_id']
            
            accounts = get_account_info(access_token)
            account_info = next((acc for acc in accounts if acc['account_id'] == account_id), accounts[0] if accounts else {})
            
            bank_account, created = BankAccount.objects.get_or_create(
                user=request.user,
                plaid_item_id=item_id,
                defaults={
                    'institution_name': metadata.get('institution', {}).get('name', 'Unknown Bank'),
                    'account_type': account_info.get('subtype', 'checking'),
                    'token': b'',
                    'plaid_account_id': account_id,
                }
            )
            
            bank_account.encrypt_plaid_token(access_token)
            bank_account.plaid_item_id = item_id
            bank_account.plaid_account_id = account_id
            bank_account.institution_name = metadata.get('institution', {}).get('name', bank_account.institution_name)
            bank_account.save()
            
            self.perform_transaction_sync(bank_account)
            
            return Response({
                'message': 'Bank account linked successfully',
                'bank_account_id': str(bank_account.id),
                'created': created
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Failed to exchange Plaid token: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='sync-transactions')
    def sync_transactions_action(self, request, pk=None):
        """Manually sync transactions from Plaid for a specific bank account."""
        bank_account = self.get_object()
        
        if not bank_account.plaid_access_token:
            return Response(
                {'error': 'This account is not linked to Plaid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            synced_count = self.perform_transaction_sync(bank_account)
            return Response({
                'message': f'Successfully synced {synced_count} transactions',
                'synced_count': synced_count,
                'last_sync': bank_account.last_sync
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to sync transactions: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_transaction_sync(self, bank_account):
        """Internal method to perform transaction sync for a bank account."""
        access_token = bank_account.decrypt_plaid_token()
        if not access_token:
            raise Exception('No Plaid access token found')
        
        sync_data = sync_transactions(access_token, cursor=bank_account.plaid_cursor)
        synced_count = 0
        
        for txn_data in sync_data['added']:
            category = None
            if txn_data.get('category'):
                category, _ = Category.objects.get_or_create(
                    user=bank_account.user,
                    name=txn_data['category'],
                    defaults={'type': txn_data['type']}
                )
            
            Transaction.objects.update_or_create(
                plaid_transaction_id=txn_data['plaid_transaction_id'],
                defaults={
                    'user': bank_account.user,
                    'bank_account': bank_account,
                    'amount': txn_data['amount'],
                    'type': txn_data['type'],
                    'description': txn_data['description'],
                    'date': txn_data['date'],
                    'category': category,
                }
            )
            synced_count += 1
        
        for txn_data in sync_data['modified']:
            try:
                transaction = Transaction.objects.get(
                    plaid_transaction_id=txn_data['plaid_transaction_id']
                )
                transaction.amount = txn_data['amount']
                transaction.description = txn_data['description']
                transaction.date = txn_data['date']
                transaction.save()
                synced_count += 1
            except Transaction.DoesNotExist:
                pass
        
        for txn_id in sync_data['removed']:
            Transaction.objects.filter(plaid_transaction_id=txn_id).delete()
        
        bank_account.plaid_cursor = sync_data['next_cursor']
        bank_account.last_sync = timezone.now()
        bank_account.save()
        
        return synced_count

