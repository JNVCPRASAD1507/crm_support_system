# CRM Support System — React + TypeScript Frontend

This frontend was prepared from the existing project and converted from React JavaScript (`.jsx`) to React TypeScript (`.tsx`).

## Main file extensions

- `.tsx` — React components/pages containing JSX
- `.ts` — TypeScript services, API clients, types, utilities
- `.css` — stylesheets

## Install

Open PowerShell in this folder:

```powershell
npm install
```

## Configure backend URL

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

The default is:

```env
VITE_API_URL=http://localhost:8000
```

## Run

```powershell
npm run dev
```

Frontend:
http://localhost:5173

Backend:
http://localhost:8000

## Important

The backend does not need to be changed for the initial frontend integration. The frontend will consume the existing FastAPI APIs.
