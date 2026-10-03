# Novas Backend API

Production-ready Django REST Framework backend for the **Novas Defence, Maritime & Industrial Solutions** platform, architected using the decoupled Service Layer pattern.

---

## Tech Stack
- **Python**: 3.12+
- **Django**: 6.1.1
- **Django REST Framework**: 3.18.1
- **CORS Headers**: django-cors-headers
- **Image Processing**: Pillow

---

## Project Structure
```
novas/
├── core/
│   ├── catalog/         # Products, Categories (incl. Agriculture), Specs, Vessels
│   ├── consultancy/     # 5 Variations (International, IT/Telecom, Project, Tender, Real Estate), Services
│   ├── inquiries/       # RFQ Inquiries with items, Contact messages, Newsletter
│   ├── projects/        # Turnkey engineering & defense projects, specs
│   ├── sectors/         # Strategic sectors (Defence, Maritime, Industry, Geospatial, ICT, Logistics)
│   ├── site_content/    # Company profile, pillars, blueprints, dynamic hero banner slides
│   ├── users/           # Custom User model
│   ├── core/            # Project configuration (settings, root urls, wsgi/asgi)
│   ├── manage.py
│   └── seed_data.json   # Full initial dataset from frontend
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone & Set Up Virtual Environment
```bash
git clone git@github.com:Mehedi19087/novas-backend.git
cd novas-backend

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
cd core
python manage.py migrate
```

### 3. Seed Initial Frontend Data
Populates products, categories, consultancy variations, projects, sectors, and banner slides into the database:
```bash
python manage.py seed_novas_data
```

### 4. Create an Admin Superuser
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```
API endpoints will be available at `http://127.0.0.1:8000/api/v1/` and admin portal at `http://127.0.0.1:8000/admin/`.

---

## Running Automated Tests
```bash
cd core
python manage.py test
```
Runs the full test suite across all 6 domain applications.
