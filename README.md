<div align="center">

# 💳 Fintech Wallet 2.0

**Zamonaviy raqamli hamyon — pul o'tkazma, tranzaksiya tarixi va shaxsiy moliyaviy boshqaruv**

[![Nuxt](https://img.shields.io/badge/Nuxt-4.x-00DC82?logo=nuxt&logoColor=white)](https://nuxt.com)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.x-38BDF8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🔗 GitHub](https://github.com/javohir-tech/fintechWallet-2.0) • [🐛 Bug report](https://github.com/javohir-tech/fintechWallet-2.0/issues)

</div>

---

## ✨ Imkoniyatlar

| Modul | Tavsif |
|---|---|
| 🔐 **Auth** | Ro'yxatdan o'tish, kirish, email/telefon orqali tasdiqlash, parol tiklash |
| 💼 **Wallet** | Balans ko'rish, karta ma'lumotlari, kunlik/oylik/yillik statistika diagrammasi |
| 💸 **Transfer** | Karta raqami bo'yicha qidirish, saqlangan kartalar cache, tez o'tkazma |
| 📋 **Transactions** | O'tkazmalar tarixi, filter (yo'nalish / holat / tur / qidiruv), PDF yuklab olish |
| 👤 **Profile** | Foydalanuvchi ma'lumotlari, avatar, balans |
| ⚙️ **Settings** | Asosiy rang (17 ta), mavzu (light/dark/system), sidebar tomoni, til (uz/ru/en) |
| 🌐 **i18n** | O'zbek 🇺🇿 / Русский 🇷🇺 / English 🇬🇧 |

---

## 🏗 Arxitektura

```
fintechWallet/
├── client/                 # Nuxt 4 + Vue 3 + TypeScript
│   ├── app/
│   │   ├── pages/          # Sahifalar (transfer, transactions, profile, settings...)
│   │   ├── components/     # UI komponentlar (BalanceCard, WalletChart, ...)
│   │   ├── composables/    # useBalance, useTransaction, useAuth
│   │   ├── store/          # Pinia (useUser, useSettings)
│   │   ├── services/       # API chaqiruvlar
│   │   ├── plugins/        # settings.client.ts
│   │   └── locales/        # i18n (uz, ru, en) — DEPRECATED, i18n/locales/ da
│   └── i18n/locales/       # uz.json, ru.json, en.json
│
└── server/                 # Django 5 + Django REST Framework
    ├── users/              # Auth, JWT, tasdiqlash
    ├── wallet/             # Wallet, balans, statistika
    ├── cards/              # Karta modeli
    └── transactions/       # Tranzaksiya yaratish, ro'yxat, detail
```

---

## 🚀 Ishga tushirish

### Talablar

- Python `3.12+`
- Node.js `20+`
- npm / pnpm

---

### Backend (Django)

```bash
cd server

# Virtual muhit yaratish
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Paketlarni o'rnatish
pip install -r requirements.txt

# Ma'lumotlar bazasini tayyorlash
python manage.py migrate

# Supefoydalanuvchi yaratish (ixtiyoriy)
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

Server: `http://localhost:8000`

---

### Frontend (Nuxt)

```bash
cd client

# Paketlarni o'rnatish
npm install

# Dev server
npm run dev
```

Ilova: `http://localhost:3000`

---

## 🔌 API Endpointlar

### Auth — `/auth/`
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/auth/signup/` | Ro'yxatdan o'tish |
| POST | `/auth/verify/` | Kodni tasdiqlash |
| POST | `/auth/login/` | Kirish |
| POST | `/auth/logout/` | Chiqish |
| POST | `/auth/forget/` | Parol tiklash |
| POST | `/auth/password/` | Yangi parol |
| PATCH | `/auth/update/` | Username va parol yangilash |
| PUT | `/auth/avatar/` | Avatar yuklash |

### Wallet — `/wallet/`
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/wallet/me/` | Balans va karta ma'lumotlari |
| GET | `/wallet/stats/?period=monthly` | Statistika (daily/weekly/monthly/yearly) |

### Card — `/card/`
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/card/look/` | Karta raqami bo'yicha foydalanuvchi qidirish |

### Transactions — `/transactions/`
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/transactions/create-transfer/` | Pul o'tkazma |
| GET | `/transactions/transactions/` | Barcha tranzaksiyalar (filter: status, txtype, direction) |
| GET | `/transactions/transactions/<id>/` | Bitta tranzaksiya detail |

---

## 🛠 Texnologiyalar

**Frontend**
- [Nuxt 4](https://nuxt.com) + [Vue 3](https://vuejs.org)
- [Nuxt UI 4](https://ui.nuxt.com) — komponent kutubxona
- [Pinia](https://pinia.vuejs.org) — state management
- [Chart.js](https://www.chartjs.org) — diagrammalar
- [Tailwind CSS 4](https://tailwindcss.com)
- [@nuxtjs/i18n](https://i18n.nuxtjs.org) — ko'p tillilik
- [Axios](https://axios-http.com) — HTTP client

**Backend**
- [Django 5](https://www.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io) — JWT autentifikatsiya
- SQLite (development) / PostgreSQL (production)

---

## 👨‍💻 Muallif

**Javohir** — [GitHub](https://github.com/javohir-tech)

---

<div align="center">

⭐ Loyiha yoqsa, yulduzcha qo'yishni unutmang!

</div>
