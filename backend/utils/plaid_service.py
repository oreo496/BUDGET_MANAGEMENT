"""
Plaid API Integration Service
Handles connection to Plaid for bank account linking and transaction sync.
"""
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from django.conf import settings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def get_plaid_client():
    """Initialize and return Plaid API client."""
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox if settings.PLAID_ENV == 'sandbox' else (
            plaid.Environment.Development if settings.PLAID_ENV == 'development' else plaid.Environment.Production
        ),
        api_key={
            'clientId': settings.PLAID_CLIENT_ID,
            'secret': settings.PLAID_SECRET,
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


def create_link_token(user_id, client_name='Funder Budget App'):
    """
    Create a Plaid Link token for initiating the Link flow in frontend.
    
    Args:
        user_id: String ID of the user
        client_name: Name to display in Plaid Link
        
    Returns:
        dict with link_token and expiration
    """
    try:
        client = get_plaid_client()
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=str(user_id)),
            client_name=client_name,
            products=[Products('transactions')],
            country_codes=[CountryCode('US')],
            language='en',
        )
        response = client.link_token_create(request)
        return {
            'link_token': response['link_token'],
            'expiration': response['expiration']
        }
    except plaid.ApiException as e:
        logger.error(f"Plaid link token creation failed: {e}")
        raise Exception(f"Failed to create link token: {e.body}")


def exchange_public_token(public_token):
    """
    Exchange a public token for an access token.
    This is called after user successfully links their bank account.
    
    Args:
        public_token: The public token from Plaid Link
        
    Returns:
        dict with access_token and item_id
    """
    try:
        client = get_plaid_client()
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        return {
            'access_token': response['access_token'],
            'item_id': response['item_id']
        }
    except plaid.ApiException as e:
        logger.error(f"Plaid token exchange failed: {e}")
        raise Exception(f"Failed to exchange token: {e.body}")


def fetch_transactions(access_token, start_date=None, end_date=None):
    """
    Fetch transactions from Plaid for a given access token.
    
    Args:
        access_token: Plaid access token for the account
        start_date: Start date for transactions (defaults to 30 days ago)
        end_date: End date for transactions (defaults to today)
        
    Returns:
        list of transaction dictionaries
    """
    try:
        client = get_plaid_client()
        
        if not end_date:
            end_date = datetime.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
        )
        
        response = client.transactions_get(request)
        transactions = response['transactions']
        
        # Handle pagination if there are more transactions
        while len(transactions) < response['total_transactions']:
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options={
                    'offset': len(transactions)
                }
            )
            response = client.transactions_get(request)
            transactions.extend(response['transactions'])
        
        return [format_transaction(txn) for txn in transactions]
    except plaid.ApiException as e:
        logger.error(f"Plaid fetch transactions failed: {e}")
        raise Exception(f"Failed to fetch transactions: {e.body}")


def sync_transactions(access_token, cursor=None):
    """
    Sync transactions using Plaid's sync endpoint (more efficient for incremental updates).
    
    Args:
        access_token: Plaid access token
        cursor: Optional cursor from previous sync
        
    Returns:
        dict with transactions, added, modified, removed lists and next_cursor
    """
    try:
        client = get_plaid_client()
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=cursor
        )
        response = client.transactions_sync(request)
        
        return {
            'added': [format_transaction(txn) for txn in response.get('added', [])],
            'modified': [format_transaction(txn) for txn in response.get('modified', [])],
            'removed': [txn.get('transaction_id') for txn in response.get('removed', [])],
            'next_cursor': response.get('next_cursor'),
            'has_more': response.get('has_more', False)
        }
    except plaid.ApiException as e:
        logger.error(f"Plaid sync transactions failed: {e}")
        raise Exception(f"Failed to sync transactions: {e.body}")


def format_transaction(plaid_txn):
    """
    Format a Plaid transaction into our database structure.
    
    Args:
        plaid_txn: Raw transaction from Plaid API
        
    Returns:
        dict with formatted transaction data
    """
    return {
        'plaid_transaction_id': plaid_txn.get('transaction_id'),
        'date': plaid_txn.get('date'),
        'description': plaid_txn.get('name', ''),
        'amount': abs(float(plaid_txn.get('amount', 0))),
        'type': 'EXPENSE' if plaid_txn.get('amount', 0) > 0 else 'INCOME',
        'category': determine_category(plaid_txn.get('category', [])),
        'merchant_name': plaid_txn.get('merchant_name'),
        'pending': plaid_txn.get('pending', False),
        'payment_channel': plaid_txn.get('payment_channel'),
    }


def determine_category(plaid_categories):
    """
    Map Plaid categories to our category system.
    
    Args:
        plaid_categories: List of category strings from Plaid
        
    Returns:
        Category name or None
    """
    if not plaid_categories:
        return None
    
    # Map common Plaid categories to our system
    category_mapping = {
        'Food and Drink': 'Food & Dining',
        'Restaurants': 'Food & Dining',
        'Groceries': 'Groceries',
        'Travel': 'Travel',
        'Transportation': 'Transportation',
        'Gas': 'Transportation',
        'Shopping': 'Shopping',
        'Entertainment': 'Entertainment',
        'Healthcare': 'Healthcare',
        'Bills': 'Bills & Utilities',
        'Utilities': 'Bills & Utilities',
        'Transfer': 'Transfer',
        'Payment': 'Payment',
    }
    
    # Check first (most specific) category
    first_category = plaid_categories[0] if plaid_categories else None
    
    for plaid_cat, our_cat in category_mapping.items():
        if first_category and plaid_cat.lower() in first_category.lower():
            return our_cat
    
    # Default to first category if no mapping found
    return first_category


def get_account_info(access_token):
    """
    Get account information for a linked item.
    
    Args:
        access_token: Plaid access token
        
    Returns:
        list of account dictionaries
    """
    try:
        client = get_plaid_client()
        from plaid.model.accounts_get_request import AccountsGetRequest
        
        request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request)
        
        return [{
            'account_id': acc.get('account_id'),
            'name': acc.get('name'),
            'official_name': acc.get('official_name'),
            'type': acc.get('type'),
            'subtype': acc.get('subtype'),
            'mask': acc.get('mask'),  # Last 4 digits
            'balance': acc.get('balances', {}).get('current'),
        } for acc in response.get('accounts', [])]
    except plaid.ApiException as e:
        logger.error(f"Plaid get account info failed: {e}")
        raise Exception(f"Failed to get account info: {e.body}")
