# SanskritiPulse AI (YuktiAi) - Full-Stack Cultural Intelligence Platform

![YuktiAi](https://img.shields.io/badge/YuktiAi-AI%20Data%20Engine-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-38bdf8.svg)
![Leaflet.js](https://img.shields.io/badge/Leaflet.js-GIS%20Map-198754.svg)
![CORS](https://img.shields.io/badge/CORS-Enabled-brightgreen.svg)

Welcome to the full-stack repository for **SanskritiPulse AI (YuktiAi)** — a unified cultural discovery platform, AI recommendation engine, travel itinerary builder, government intelligence system, and live site operations control room for Karnataka's festivals and heritage events.

---

## 🚀 One-Command Launch Guide

Launch the entire full-stack application (backend REST APIs + single-page web UI):

```bash
uvicorn main:app --reload --port 8000
```

Once running, access the interactive prototype in your web browser:
- 🌐 **Live Web Application UI:** [http://localhost:8000](http://localhost:8000)
- 📚 **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **ReDoc OpenAPI Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🎨 Unified Multi-Stakeholder Interactive Web App (`static/index.html`)

The single-page web application features a top navigation tab bar enabling seamless switching between all 3 stakeholder views:

### 1. 🧳 Tourist Discovery Dashboard (Monika's View)
- **Festival Discovery Grid:** Browse over 35 Karnataka festivals with District and Category dropdown filters.
- **Interactive AI Interest Quiz:** Select interest tags (*Food, Folk, Heritage, Sports, Music*) to call `POST /recommend` with Cosine Similarity match percentage badges (e.g. `92% Match`).
- **Festival Detail Modal:** Deep dive into cultural significance, history, local food, attractions, and live broadcast announcements (`GET /announcements/{id}`).
- **Smart Travel & Hotel Planner Modal:** Form calling `POST /travel-plan` returning transit comparisons (Bus vs. Train vs. Car), structured 2-day itineraries, and nearby hotel accommodations (`GET /hotels/{id}`).
- **Multilingual Language Selector:** Toggle between English, ಕನ್ನಡ (Kannada), and हिंदी (Hindi) with real-time UI text translation (`POST /translate`).

### 2. 🏛️ Tourism Department Intelligence (Gov Analytics View)
- **Real-Time KPI Cards:** Displays Total Festivals, Total Expected Visitors (16.5M+), High-Risk Events Count, and Top Trending District.
- **Leaflet.js GIS Interactive Map:** Displays Karnataka festival markers color-coded by Crowd Risk level (🟢 Low `<100k`, 🟡 Medium `100k-500k`, 🔴 High `>500k`) with popups for projected growth % and automated infrastructure advisories.
- **Infrastructure Advisories Panel:** Real-time warnings for Transport, Sanitation, Security, Medical, and Parking logistics.
- **Footfall Distribution Trends:** Visual progress bars displaying district and category footfall shares.

### 3. 🎪 Festival Site Organizer (Tanishi's View)
- **Live Spectator Control Room:** Venue selector dropdown with real-time spectator counters, venue capacity progress bars, peak hours (`6 PM - 9 PM`), and crowd warning flags.
- **Broadcast Announcement Publisher:** Form posting live alerts (`POST /organizer/announcement`) that immediately update the tourist feed across the portal.

---

## 👥 Multi-Stakeholder API Matrix

| Stakeholder Role | Team Member | Primary Module | Endpoint Routes |
| :--- | :--- | :--- | :--- |
| **Member 1** | Tezraj | PostgreSQL DB & Master Metadata | `GET /festivals`, `GET /festivals/{id}` |
| **Member 2** | Nandish | AI Recommendation & Multilingual | `POST /recommend`, `POST /translate` |
| **Member 3** | Simran | Travel & Hotel Engine | `POST /travel-plan`, `GET /hotels/{location}` |
| **Member 4** | Monika | Tourist Discovery Dashboard | `GET /announcements/{festival_id}` |
| **Member 5** | Jhanvi | Department Intelligence & Crowd Risk | `GET /analytics/overview`, `/analytics/map-data`, `/analytics/trends` |
| **Member 6** | Tanishi | Organizer Site Ops | `GET /organizer/overview/{id}`, `POST /organizer/announcement` |

---

## 🧪 Automated Testing & Prototype Verification

Execute end-to-end integration tests across all 12 backend and UI routes:

```bash
python test_full_prototype.py
```

### Test Verification Summary:
```text
================================================================
🚀 Running SanskritiPulse AI Full Prototype Test Suite
================================================================

Testing [GET] / (Single-Page Web UI) ... ✅ PASSED (HTTP 200)
Testing [GET] /festivals (Get Festivals) ... ✅ PASSED (HTTP 200)
Testing [POST] /recommend (AI Recommendation) ... ✅ PASSED (HTTP 200)
Testing [POST] /translate (Multilingual Translation) ... ✅ PASSED (HTTP 200)
Testing [POST] /travel-plan (Travel Route & Itinerary) ... ✅ PASSED (HTTP 200)
Testing [GET] /hotels/mysuru-dasara (Nearby Hotels Search) ... ✅ PASSED (HTTP 200)
Testing [GET] /analytics/overview (Analytics Overview) ... ✅ PASSED (HTTP 200)
Testing [GET] /analytics/map-data (GIS Map GeoJSON) ... ✅ PASSED (HTTP 200)
Testing [GET] /analytics/trends (Analytics Trends) ... ✅ PASSED (HTTP 200)
Testing [GET] /organizer/overview/mysuru-dasara (Site Ops Overview) ... ✅ PASSED (HTTP 200)
Testing [POST] /organizer/announcement (Publish Announcement) ... ✅ PASSED (HTTP 200)
Testing [GET] /announcements/mysuru-dasara (Fetch Announcements) ... ✅ PASSED (HTTP 200)

================================================================
📊 Summary: 12/12 Prototype Routes Verified (HTTP 200 OK)
================================================================
```

---

## 🛠️ Project File Structure

```
YuktiAI/
├── main.py                     # Master FastAPI app (Cors, Routes, Static Files)
├── ai_engine.py                # AI Vector Recommendation & Multilingual Engine
├── travel_engine.py            # Route matrices, 2-day itineraries, and hotel lookup
├── analytics_engine.py         # Footfall prediction, Crowd Risk & GIS GeoJSON
├── organizer_engine.py         # Live spectator metrics & broadcast announcements
├── test_full_prototype.py      # Automated e2e verification suite (12/12 tests)
├── static/
│   └── index.html              # Unified HTML5/Tailwind single-page web app
├── festivals_backup.csv        # Seeding data backups
├── requirements.txt            # Python dependencies
└── README.md                   # Full-stack documentation
```
