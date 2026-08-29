<div align="center">

# 🏛️ YuktiAI — SanskritiPulse

### *Unified Cultural Intelligence & Live Event Management Platform*

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=github-actions)](https://github.com/Tejzraj/YuktiAI)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue?style=for-the-badge)](https://github.com/Tejzraj/YuktiAI)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-4169E1?style=for-the-badge&logo=postgresql)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)

**YuktiAI is an end-to-end AI-powered cultural intelligence platform that integrates real-time tourist event recommendations, GIS crowd risk analytics, smart travel routing, and live venue site operations into a single interactive dashboard.**

[Quick Start](#-quick-start) • [Key Features](#-key-features) • [System Architecture](#%EF%B8%8F-system-architecture) • [API Matrix](#-multi-stakeholder-api-matrix) • [Testing](#-verification--testing)

</div>

---

## ⚡ Quick Start

Launch the full-stack REST API and interactive web application using a single command:

```bash
# Clone the repository
git clone https://github.com/Tejzraj/YuktiAI.git && cd YuktiAI

# Install dependencies and start the application
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

| Service Endpoint | Description | Link |
| :--- | :--- | :--- |
| 🌐 **Live Web Application** | Interactive single-page multi-stakeholder web dashboard | [http://localhost:8000](http://localhost:8000) |
| 📚 **Swagger OpenAPI Docs** | Interactive API testing interface | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📖 **ReDoc Documentation** | Structural API spec reference | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 🌟 Key Features

### 🧳 1. Tourist Cultural Discovery
- **Personalized Vector Match:** Calculates cosine similarity scores to match user preferences with 35+ Karnataka heritage festivals.
- **Smart Itinerary Planner:** Generates multi-modal transit comparisons (Bus, Train, Car) alongside 2-day tailored travel schedules and nearby hotel lookup.
- **Multilingual Support:** Offers instant real-time localized interface translation across English, ಕನ್ನಡ (Kannada), and हिंदी (Hindi).

### 🏛️ 2. Tourism Department Intelligence
- **GIS Crowd Risk Map:** Renders color-coded risk markers (🟢 Low, 🟡 Medium, 🔴 High) powered by Leaflet.js based on projected footfall.
- **Predictive Logistics:** Generates automated advisories for transport capacity, sanitation, medical services, and security deployment.
- **District Analytics:** Tracks footfall distribution and high-risk crowd events in real time.

### 🎪 3. Live Site Event Operations
- **Real-Time Spectator Monitoring:** Tracks live venue occupancy percentages against maximum safety thresholds with peak-hour alerts.
- **Instant Broadcast Alerts:** Enables organizers to publish site notifications that propagate dynamically to tourist feeds.

---

## 🏗️ System Architecture

### 📂 Directory Structure

```text
YuktiAI/
├── main.py                     # Master FastAPI application, CORS policy & router mounting
├── ai_engine.py                # Cosine similarity vector matcher & multilingual translation engine
├── travel_engine.py            # Transit route matrix, multi-day itinerary builder & hotel locator
├── analytics_engine.py         # Crowd risk assessment, footfall forecasting & GIS GeoJSON generator
├── organizer_engine.py         # Live spectator telemetry & broadcast alert publisher
├── test_full_prototype.py      # E2E automated test suite (12/12 routes verified)
├── static/
│   └── index.html              # Single-page HTML5/TailwindCSS & Leaflet.js web application
├── database/
│   ├── init.sql                # PostgreSQL relational database schema definition
│   └── mock_festivals.json     # Baseline dataset for festival records & metadata
├── requirements.txt            # Python dependencies (FastAPI, Uvicorn, Requests, Pydantic)
├── Dockerfile                  # Container build instructions for backend service
└── docker-compose.yml          # Multi-container orchestration (FastAPI + PostgreSQL)
```

### 🔄 Data & Execution Flow

```text
  [ Web Browser / Client ]
             │
             ▼
      ┌──────────────┐
      │  main.py     │  ◄── FastAPI REST Gateway & Static File Server
      └──────┬───────┘
             │
 ┌───────────┼───────────────┬──────────────────┐
 ▼           ▼               ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌────────────────┐ ┌──────────────────┐
│ ai_engine    │ │ travel_engine│ │analytics_engine│ │ organizer_engine │
├──────────────┤ ├──────────────┤ ├────────────────┤ ├──────────────────┤
│• Vector Match│ │• Transit Plan│ │• Hotels Data │ │• GIS GeoJSON   │ │• Live Telemetry  │
│• Translation │ │• Hotels Data │ │• Crowd Risk    │ │• Broadcast Alerts│
└──────────────┘ └──────────────┘ └────────────────┘ └──────────────────┘
```

---

## 👥 Multi-Stakeholder API Matrix

| Stakeholder Domain | Core Module | Route Endpoint | HTTP Method | Functionality |
| :--- | :--- | :--- | :--- | :--- |
| **Festival Core** | `main.py` | `/festivals` | `GET` | Retrieve complete festival catalog & filtering metadata |
| **Festival Core** | `main.py` | `/festivals/{id}` | `GET` | Fetch specific festival profile details |
| **AI Intelligence** | `ai_engine.py` | `/recommend` | `POST` | Execute vector similarity matching against user quiz tags |
| **AI Intelligence** | `ai_engine.py` | `/translate` | `POST` | Translate UI text dynamically (EN, KN, HI) |
| **Travel & Logistics** | `travel_engine.py` | `/travel-plan` | `POST` | Compute multi-modal route options & 2-day itinerary |
| **Travel & Logistics** | `travel_engine.py` | `/hotels/{id}` | `GET` | Find nearby accommodation options by festival ID |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/overview` | `GET` | Fetch macro tourism KPIs, total footfall & risk counters |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/map-data` | `GET` | Generate Leaflet-compatible GeoJSON feature collections |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/trends` | `GET` | Get district & category footfall distribution metrics |
| **Site Operations** | `organizer_engine.py` | `/organizer/overview/{id}`| `GET` | Monitor live venue spectator stats & safety thresholds |
| **Site Operations** | `organizer_engine.py` | `/organizer/announcement`| `POST` | Dispatch live emergency or general event broadcasts |
| **Tourist Feed** | `organizer_engine.py` | `/announcements/{id}` | `GET` | Stream broadcast announcements to tourist dashboard |

---

## 🧪 Verification & Testing

Verify system integrity across all 12 backend endpoints with the automated integration suite:

```bash
python test_full_prototype.py
```

### Test Suite Execution Output:

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

## 🐳 Docker Deployment

Run the complete containerized stack using Docker Compose:

```bash
# Build and run containers in detached mode
docker-compose up -d --build

# View application logs
docker-compose logs -f
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
