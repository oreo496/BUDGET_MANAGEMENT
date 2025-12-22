# Quick Setup Card - Plaid Integration

## 🚀 Get Started in 5 Steps

### Step 1: Get Plaid Credentials (2 minutes)
1. Go to https://plaid.com/
2. Sign up for free account
3. Get your credentials from dashboard:
   - Client ID
   - Sandbox Secret

### Step 2: Configure Backend (1 minute)
Add to `backend/.env`:
```bash
PLAID_CLIENT_ID=your_client_id_here
PLAID_SECRET=your_sandbox_secret_here
PLAID_ENV=sandbox
```

### Step 3: Run Migrations (1 minute)
```bash
cd backend
python manage.py makemigrations bank_accounts transactions
python manage.py migrate
```

### Step 4: Install Frontend Package (1 minute)
```bash
cd frontend
npm install react-plaid-link
```

### Step 5: Create Plaid Component (5 minutes)
Create `frontend/src/components/PlaidLink.tsx`:
```typescript
import { usePlaidLink } from 'react-plaid-link';
import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function PlaidLink({ onSuccess }: { onSuccess: () => void }) {
  const [linkToken, setLinkToken] = useState<string | null>(null);

  useEffect(() => {
    api.post('/bank-accounts/plaid/create-link-token/')
      .then(res => setLinkToken(res.data.link_token))
      .catch(err => console.error(err));
  }, []);

  const { open, ready } = usePlaidLink({
    token: linkToken,
    onSuccess: (public_token, metadata) => {
      api.post('/bank-accounts/plaid/exchange-token/', {
        public_token,
        account_id: metadata.accounts[0].id,
        metadata
      }).then(() => onSuccess());
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

### Step 6: Use Component (1 minute)
In your cards/accounts page:
```typescript
import PlaidLink from '@/components/PlaidLink';

<PlaidLink onSuccess={() => {
  // Refresh your list
  fetchBankAccounts();
}} />
```

---

## 🧪 Test It

### Sandbox Test Credentials
- **Username**: `user_good`
- **Password**: `pass_good`
- **Bank**: Chase (or any shown)

### What You'll See
1. Plaid Link modal opens
2. Select "Chase" (or another bank)
3. Enter test credentials
4. Select checking account
5. Success! Account linked
6. Transactions automatically synced

### Verify It Worked
```bash
# Check bank accounts
curl http://localhost:8000/api/bank-accounts/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check transactions
curl http://localhost:8000/api/transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Manual sync
curl -X POST http://localhost:8000/api/bank-accounts/BANK_ID/sync-transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📱 What Users Will Do

1. Click "Connect Bank Account" button
2. See Plaid modal
3. Search for their bank (e.g., "Chase", "Bank of America")
4. Enter online banking credentials
5. Select which account to link
6. Done! Transactions automatically imported

---

## 🔐 Security Notes

- ✅ Your app never sees user's bank credentials
- ✅ Plaid handles authentication
- ✅ Access tokens encrypted in your database
- ✅ User can revoke access anytime
- ✅ Bank-level security standards

---

## 💰 Pricing

**Sandbox (Development)**
- FREE forever
- Unlimited testing

**Production**
- $0.25-0.60 per connected account/month
- $0.10 per API request
- First 100 accounts FREE each month

---

## 🆘 Troubleshooting

### Link Token Error
```
Error: Missing PLAID_CLIENT_ID
```
**Fix**: Add credentials to `.env` file

### Import Error
```
ImportError: No module named 'plaid'
```
**Fix**: `pip install plaid-python==16.0.0`

### Frontend Error
```
Module not found: react-plaid-link
```
**Fix**: `npm install react-plaid-link`

### No Transactions
**Check**:
1. Account linked? Check `bank_accounts` table
2. Access token saved? Check `plaid_access_token` field
3. Manual sync: `POST /sync-transactions/`

---

## 📞 Support

- **Plaid Docs**: https://plaid.com/docs/
- **Plaid Support**: https://dashboard.plaid.com/support
- **Your Implementation**: See [PLAID_INTEGRATION_GUIDE.md](PLAID_INTEGRATION_GUIDE.md)

---

## ✅ Checklist

- [ ] Signed up for Plaid
- [ ] Added credentials to `.env`
- [ ] Ran migrations
- [ ] Installed `react-plaid-link`
- [ ] Created PlaidLink component
- [ ] Added button to UI
- [ ] Tested with sandbox
- [ ] Verified transactions synced

**Once all checked, you're live!** 🎉
