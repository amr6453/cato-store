Cato-Store (Backend)

Quick start (dev):

1. Create a virtualenv and activate it.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata products/fixtures/sample_products.json
python manage.py runserver
```

2. API endpoints (examples):
- `/api/products/` - product list (search, ordering, pagination)
- `/api/orders/` - orders (authenticated)
- `/api/auth/register/` - register (returns token)
- `/api/auth/login/` - login (returns token)
- `/api/auth/profile/me/` - get/update profile
- `/api/payments/stripe/webhook/` - simulated stripe webhook endpoint

See `API.md` for detailed GraphQL and REST examples for frontend developers.

CI/tests have been removed from this workspace for a clean starting point.

Local development convenience:

1. From repo root you can run the included PowerShell helper which opens two windows (backend + frontend):

```powershell
.\start-dev.ps1
```

2. Or manually start backend and frontend in two shells:

Backend (repo root):

Frontend (from `frontend/`):
```powershell
npm run dev
```
