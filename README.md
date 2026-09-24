# 🚗 OTO DriveCare — Django Project

A roadside assistance web application that connects vehicle owners with nearby garages, mechanics, and towing services in real-time.

---

## 📁 Project Structure

```
otodrivecare/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── otodrivecare/          ← Main project config
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/              ← User auth & profiles
├── providers/             ← Garage/mechanic profiles
├── services/              ← Services offered
├── emergency/             ← Emergency request system
├── reviews/               ← Ratings & reviews
├── dashboard/             ← User dashboards
├── breakdown/             ← Breakdown redirect
│
├── templates/             ← All HTML templates
│   ├── base.html
│   ├── public/
│   ├── accounts/
│   ├── providers/
│   ├── services/
│   ├── emergency/
│   ├── reviews/
│   └── dashboard/
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
└── media/                 ← Uploaded files (runtime)
```

---

## ⚡ Quick Setup in VS Code

### Step 1 — Open project in VS Code
```
File → Open Folder → select the otodrivecare folder
```

### Step 2 — Open Terminal
```
Ctrl + ` (backtick)   or   View → Terminal
```

### Step 3 — Create & activate virtual environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Create admin superuser
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 7 — Run the development server
```bash
python manage.py runserver
```

### Step 8 — Open in browser
```
http://127.0.0.1:8000/
```

---

## 🔑 Key URLs

| URL | Page |
|-----|------|
| `/` | Home page |
| `/accounts/register/` | User registration |
| `/accounts/login/` | Login |
| `/dashboard/` | User dashboard |
| `/emergency/request/` | Request emergency help |
| `/services/nearby/` | Nearby services map |
| `/providers/` | Provider list |
| `/providers/register/` | Register as provider |
| `/admin/` | Admin panel |

---

## 👤 User Roles

- **Regular User** — register, request help, track status, write reviews
- **Service Provider** — register shop, manage services, accept/complete requests
- **Admin** — manage all users, verify providers, view all data via `/admin/`

---

## 🗺️ Features

- GPS-based emergency requests using Leaflet.js + OpenStreetMap
- Nearest provider auto-matching algorithm
- Real-time request status tracking (Pending → Accepted → On the way → Completed)
- Ratings & reviews with auto-average update
- Admin panel for verifying providers and managing all data
- Fully responsive Bootstrap 5 UI

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x + Django 4.2
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Maps**: Leaflet.js + OpenStreetMap (free, no API key needed)
- **Forms**: django-crispy-forms + crispy-bootstrap5

---

## 📝 Admin Panel Notes

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. **Verify providers**: Providers → select → check "Verified" → Save
4. Manage users, emergency requests, and reviews from here

---

## 🐛 Common Issues

**"No module named django"**
→ Make sure venv is activated: `venv\Scripts\activate`

**"Table doesn't exist"**
→ Run: `python manage.py migrate`

**Static files not loading**
→ Make sure `DEBUG = True` in settings.py during development

**Images not showing**
→ Run with: `python manage.py runserver` (media files need the dev server)
