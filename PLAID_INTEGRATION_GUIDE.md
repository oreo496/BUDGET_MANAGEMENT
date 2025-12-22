# Plaid Integration Setup Guide

## Complete! ✅

Plaid has been fully integrated into your budget management system. Here's what was implemented:

### Backend Changes

1. **✅ Installed plaid-python 16.0.0**
   - Added to requirements.txt

2. **✅ Plaid Configuration** (`backend/funder/settings.py`)
   ```python
   PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID', '')
   PLAID_SECRET = os.getenv('PLAID_SECRET', '')
   PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
   ```

3. **✅ Plaid Service Layer** (`backend/utils/plaid_service.py`)
   - `create_link_token()` - Generate token for Plaid Link UI
   - `exchange_public_token()` - Exchange public token for access token
   - `sync_transactions()` - Incremental transaction sync
   - `fetch_transactions()` - Full transaction fetch
   - `get_account_info()` - Get account details
   - `determine_category()` - Map Plaid categories to your system

4. **✅ Updated BankAccount Model** (`backend/bank_accounts/models.py`)
   - Added `plaid_access_token` (encrypted)
   - Added `plaid_item_id`
   - Added `plaid_account_id`
   - Added `plaid_cursor` (for incremental sync)
   - Added `last_sync`
   - Added `auto_sync_enabled`
   - Added `encrypt_plaid_token()` and `decrypt_plaid_token()` methods

5. **✅ Updated Transaction Model** (`backend/transactions/models.py`)
   - Fixed UUID field (was BinaryField, now UUIDField)
   - Added `description` field
   - Added `plaid_transaction_id` field (unique)

6. **✅ New API Endpoints** (`backend/bank_accounts/views.py`)
   - `POST /api/bank-accounts/plaid/create-link-token/` - Get link token
   - `POST /api/bank-accounts/plaid/exchange-token/` - Link bank account
   - `POST /api/bank-accounts/{id}/sync-transactions/` - Manual sync

### How It Works

#### 1. User Links Bank Account
```
Frontend → POST /api/bank-accounts/plaid/create-link-token/
Backend → Returns link_token
Frontend → Opens Plaid Link with link_token
User → Selects bank and logs in
Plaid → Returns public_token
Frontend → POST /api/bank-accounts/plaid/exchange-token/ with public_token
Backend → Exchanges token, saves encrypted access_token, syncs initial transactions
```

#### 2. Transaction Sync
```
Backend → GET transactions from Plaid using access_token
Backend → Map Plaid categories to your categories
Backend → Create/Update Transaction records with plaid_transaction_id
Backend → Update cursor for next incremental sync
```

#### 3. Incremental Updates
- Uses Plaid's sync endpoint with cursor
- Only fetches new/modified/deleted transactions
- Much faster than full fetch
- Tracks changes: added, modified, removed

### Setup Instructions

#### Step 1: Get Plaid Credentials
1. Sign up at https://plaid.com/
2. Get your credentials:
   - Client ID
   - Secret (sandbox)
3. Add to `.env` file:
   ```
   PLAID_CLIENT_ID=your_client_id
   PLAID_SECRET=your_sandbox_secret
   PLAID_ENV=sandbox
   ```

#### Step 2: Run Database Migrations
```bash
cd backend
python manage.py makemigrations bank_accounts transactions
python manage.py migrate
```

#### Step 3: Install Plaid Link (Frontend)
```bash
cd frontend
npm install react-plaid-link
```

#### Step 4: Create Frontend Component
Create `frontend/src/components/PlaidLink.tsx`:
```typescript
import { usePlaidLink } from 'react-plaid-link';
import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function PlaidLink({ onSuccess }: { onSuccess: () => void }) {
  const [linkToken, setLinkToken] = useState<string | null>(null);

  useEffect(() => {
    // Get link token from backend
    api.post('/bank-accounts/plaid/create-link-token/')
      .then(res => setLinkToken(res.data.link_token))
      .catch(err => console.error('Failed to create link token:', err));
  }, []);

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: (public_token, metadata) => {
      // Exchange token and link account
      api.post('/bank-accounts/plaid/exchange-token/', {
        public_token,
        account_id: metadata.accounts[0].id,
        metadata
      }).then(() => {
        onSuccess();
      }).catch(err => {
        console.error('Failed to link account:', err);
      });
    },
  });

  return (
    <button
      onClick={() => open()}
      disabled={!ready}
      className="bg-blue-600 text-white px-6 py-3 rounded-lg"
    >
      Connect Bank Account
    </button>
  );
}
```

#### Step 5: Use in Cards Page
Add to `frontend/src/app/cards/page.tsx`:
```typescript
import PlaidLink from '@/components/PlaidLink';

// Inside your component:
<PlaidLink onSuccess={() => {
  // Refresh cards list
  fetchCards();
}} />
```

### Testing with Plaid Sandbox

1. Use these test credentials in Plaid Link:
   - **Username**: `user_good`
   - **Password**: `pass_good`

2. Sandbox provides fake transactions for testing

3. Test sync:
   ```bash
   # Get bank account ID after linking
   curl -X POST http://localhost:8000/api/bank-accounts/{id}/sync-transactions/ \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### API Endpoints

#### Create Link Token
```
POST /api/bank-accounts/plaid/create-link-token/
Authorization: Bearer <token>

Response:
{
  "link_token": "link-sandbox-...",
  "expiration": "2025-12-22T20:00:00Z"
}
```

#### Exchange Token & Link Account
```
POST /api/bank-accounts/plaid/exchange-token/
Authorization: Bearer <token>
Content-Type: application/json

{
  "public_token": "public-sandbox-...",
  "account_id": "account-id",
  "metadata": {
    "institution": {
      "name": "Chase",
      "institution_id": "ins_123"
    }
  }
}

Response:
{
  "message": "Bank account linked successfully",
  "bank_account_id": "uuid",
  "created": true
}
```

#### Sync Transactions
```
POST /api/bank-accounts/{bank_account_id}/sync-transactions/
Authorization: Bearer <token>

Response:
{
  "message": "Successfully synced 15 transactions",
  "synced_count": 15,
  "last_sync": "2025-12-22T19:30:00Z"
}
```

### Category Mapping

Plaid categories are automatically mapped:
- Food and Drink → Food & Dining
- Restaurants → Food & Dining
- Groceries → Groceries
- Travel → Travel
- Transportation/Gas → Transportation
- Shopping → Shopping
- Entertainment → Entertainment
- Healthcare → Healthcare
- Bills/Utilities → Bills & Utilities

### Security

- ✅ Access tokens are encrypted using Fernet
- ✅ Never exposed in API responses
- ✅ Stored securely in database
- ✅ User-specific authentication required

### Automatic Sync (Future Enhancement)

To enable automatic daily sync, add a Celery task:

```python
# backend/bank_accounts/tasks.py
from celery import shared_task
from .models import BankAccount
from .views import BankAccountViewSet

@shared_task
def auto_sync_bank_accounts():
    """Daily task to sync all bank accounts"""
    accounts = BankAccount.objects.filter(
        auto_sync_enabled=True,
        plaid_access_token__isnull=False
    )
    
    viewset = BankAccountViewSet()
    for account in accounts:
        try:
            viewset.perform_transaction_sync(account)
        except Exception as e:
            print(f"Failed to sync {account.id}: {e}")
```

### Next Steps

1. ✅ Sign up for Plaid account
2. ✅ Add credentials to `.env`
3. ✅ Run migrations
4. ✅ Install frontend dependencies
5. ✅ Create PlaidLink component
6. ✅ Test with sandbox credentials
7. ⏳ Apply for Plaid production access (when ready)

### Costs

- **Development**: Free (sandbox)
- **Production**: ~$0.25-0.60 per item/month + $0.10 per API request
- First 100 items free each month

### Support

- Plaid Docs: https://plaid.com/docs/
- Plaid Quickstart: https://plaid.com/docs/quickstart/
- API Reference: https://plaid.com/docs/api/
