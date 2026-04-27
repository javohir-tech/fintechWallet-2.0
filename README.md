<div align="center">

# 💳 Fintech Wallet 2.0

**A modern digital wallet — money transfers, transaction history, and personal finance management**

[![Nuxt](https://img.shields.io/badge/Nuxt-4.x-00DC82?logo=nuxt&logoColor=white)](https://nuxt.com)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.x-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🔗 GitHub](https://github.com/javohir-tech/fintechWallet-2.0) • [🐛 Bug Report](https://github.com/javohir-tech/fintechWallet-2.0/issues)

</div>

---

## ✨ Features

| Module | Description |
|---|---|
|  **Authentication** | Sign up, login, email/phone verification, password reset |
|  **Wallet** | Balance overview, card details, daily/weekly/monthly/yearly chart |
|  **Transfer** | Card number search, cached cards, quick transfer |
|  **Transactions** | Transaction history with filters (direction / status / type / search), PDF export |
|  **Profile** | User info, avatar, wallet balance |
|  **Settings** | Primary color (17 options), theme (light/dark/system), sidebar position, language |
|  **i18n** | English 🇬🇧 / O'zbek 🇺🇿 / Русский 🇷🇺 |

---

## 🏗 Architecture

```
fintechWallet/
├── client/                 # Nuxt 4 + Vue 3 + TypeScript
│   ├── app/
│   │   ├── pages/          # Routes (transfer, transactions, profile, settings...)
│   │   ├── components/     # UI components (BalanceCard, WalletChart, ...)
│   │   ├── composables/    # useBalance, useTransaction, useAuth
│   │   ├── store/          # Pinia stores (useUser, useSettings)
│   │   ├── services/       # API service layer
│   │   ├── plugins/        # settings.client.ts
│   │   └── types/          # TypeScript interfaces
│   └── i18n/
│       └── locales/        # uz.json, ru.json, en.json
│
└── server/                 # Django 5 + Django REST Framework
    ├── users/              # Auth, JWT, email/phone verification
    ├── wallet/             # Wallet, balance, statistics
    ├── cards/              # Card model & lookup
    └── transactions/       # Create, list, detail
```

---

## 🚀 Getting Started

### Prerequisites

- Python `3.12+`
- Node.js `20+`
- npm or pnpm

---

### Backend (Django)

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Server runs at `http://localhost:8000`

---

### Frontend (Nuxt)

```bash
cd client

# Install dependencies
npm install

# Start dev server
npm run dev
```

App runs at `http://localhost:3000`

---

## 🔌 API Reference

### Auth — `/auth/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup/` | Register a new user |
| POST | `/auth/verify/` | Verify confirmation code |
| POST | `/auth/login/` | Login |
| POST | `/auth/logout/` | Logout |
| POST | `/auth/forget/` | Request password reset |
| POST | `/auth/password/` | Set new password |
| PATCH | `/auth/update/` | Update username & password |
| PUT | `/auth/avatar/` | Upload avatar |

### Wallet — `/wallet/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/wallet/me/` | Get balance & card info |
| GET | `/wallet/stats/?period=monthly` | Statistics — `daily` / `weekly` / `monthly` / `yearly` |

### Card — `/card/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/card/look/` | Look up user by card number |

### Transactions — `/transactions/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/create-transfer/` | Create a transfer |
| GET | `/transactions/transactions/` | List all transactions (filter: `status`, `txtype`, `direction`) |
| GET | `/transactions/transactions/<id>/` | Transaction detail |

---

## 🛠 Tech Stack

**Frontend**
- [Nuxt 4](https://nuxt.com) + [Vue 3](https://vuejs.org)
- [Nuxt UI 4](https://ui.nuxt.com) — component library
- [Pinia](https://pinia.vuejs.org) — state management
- [Chart.js](https://www.chartjs.org) — charts & graphs
- [Tailwind CSS 4](https://tailwindcss.com)
- [@nuxtjs/i18n](https://i18n.nuxtjs.org) — internationalization
- [Axios](https://axios-http.com) — HTTP client

**Backend**
- [Django 5](https://www.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io) — JWT authentication
- SQLite (development) / PostgreSQL (production)

---

## 📸 Screenshots

> Coming soon

---

## 👨‍💻 Author

**Javohir** — [GitHub](https://github.com/javohir-tech)

---

<div align="center">

⭐ If you like this project, please consider giving it a star!

</div>
