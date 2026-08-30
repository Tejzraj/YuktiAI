<!-- ======================= HERO SECTION ======================= -->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=300&section=header&text=YuktiAI%20%E2%80%94%20SanskritiPulse&fontSize=60&fontAlignY=38&animation=fadeIn&fontColor=fff&desc=Unified%20Cultural%20Intelligence%20%26%20Live%20Event%20Management%20Platform&descSize=20&descAlignY=62" width="100%" alt="YuktiAI Header Banner"/>

<a href="https://github.com/Tejzraj/YuktiAI" target="_blank">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=24&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=800&height=50&lines=AI-Powered+Tourist+Event+Recommendations+%F0%9F%A7%B3;GIS+Crowd+Risk+%26+Predictive+Logistics+%F0%9F%8F%9B%EF%B8%8F;Real-Time+Venue+Spectator+Telemetry+%F0%9F%8E%AA;Multi-Modal+Transit+%26+Hotel+Planner+%F0%9F%9A%97;Multilingual+Interface%3A+English+%E2%80%A2+%E0%B2%95%E0%B2%AE%E0%B3%8D%E0%B2%A8%E0%B2%A1+%E2%80%A2+%E0%A4%B9%E0%A4%BF%E0%A4%82%E0%A4%A6%E0%A4%BF+%F0%9F%8C%90" alt="Typing SVG" />
</a>

<br/>

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=github-actions&logoColor=white&labelColor=0D1117)](https://github.com/Tejzraj/YuktiAI)
&nbsp;
[![Version](https://img.shields.io/badge/version-v1.0.0-58A6FF?style=for-the-badge&logo=git&logoColor=white&labelColor=0D1117)](https://github.com/Tejzraj/YuktiAI)
&nbsp;
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0D1117)](https://fastapi.tiangolo.com)
&nbsp;
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.0-4169E1?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=0D1117)](https://www.postgresql.org)
&nbsp;
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white&labelColor=0D1117)](LICENSE)

<br/>

**YuktiAI (SanskritiPulse)** is an end-to-end AI-powered cultural intelligence platform that integrates real-time tourist event recommendations, GIS crowd risk analytics, smart travel routing, and live venue site operations into a single interactive dashboard.

<br/>

<a href="#-quick-start"><b>⚡ Quick Start</b></a> •
<a href="#-key-features"><b>🌟 Key Features</b></a> •
<a href="#%EF%B8%8F-system-architecture"><b>🏗️ Architecture</b></a> •
<a href="#-multi-stakeholder-api-matrix"><b>🔌 API Matrix</b></a> •
<a href="#-verification--testing"><b>🧪 Testing</b></a> •
<a href="#-docker-deployment"><b>🐳 Docker</b></a>

</div>

<br/>

---

<!-- ======================= SYSTEM OVERVIEW ======================= -->

## 🏛️ System Overview

<table>
<tr>
<td valign="top" width="55%">

```python
class YuktiAISanskritiPulse:

    def __init__(self):
        self.name = "YuktiAI — SanskritiPulse"
        self.version = "1.0.0"
        self.stack = ["FastAPI", "PostgreSQL", "Leaflet.js", "Python"]
        
        self.stakeholder_domains = {
            "tourist": "Personalized Recs & Multi-Modal Routing",
            "government": "GIS Crowd Risk & Logistics Intelligence",
            "organizer": "Live Telemetry & Broadcast Operations"
        }
        
        self.ai_features = [
            "Cosine Similarity Vector Matcher",
            "Dynamic Translation (EN, KN, HI)",
            "GIS GeoJSON Crowd Risk Heatmap",
            "Real-Time Venue Occupancy Telemetry"
        ]

    def status(self):
        return "12/12 Endpoints Verified & Operational 🚀"
```

</td>

<td valign="top" width="45%">

### 🎯 Mission Statement

> **Preserving cultural heritage while ensuring safe, intelligent, and seamless festival experiences across Karnataka.**

<br/>

### 👥 Primary Stakeholders

* 🧳 **Tourists & Pilgrims** — Vector match quiz, multi-modal travel, nearby hotels & localized translations.
* 🏛️ **Tourism Department** — Real-time GIS crowd density mapping, footfall forecasting & automated logistics planning.
* 🎪 **Event Organizers** — Live venue occupancy monitoring & instant emergency/event broadcasts.

</td>
</tr>
</table>

---

<!-- ======================= KEY FEATURES ======================= -->

## 🌟 Key Features

<div align="center">

<table>
<tr>

<td width="33%" valign="top">

### 🧳 1. Tourist Discovery
*AI-Driven Recommendation Engine*

- **Vector Matching:** Calculates cosine similarity scores against 35+ Karnataka heritage festivals.
- **Smart Itinerary Planner:** Tailored 2-day schedules, multi-modal transit (Bus, Train, Car) & hotel lookups.
- **Multilingual Support:** Instant UI translation across **English**, **ಕನ್ನಡ (Kannada)**, and **हिंदी (Hindi)**.

</td>

<td width="33%" valign="top">

### 🏛️ 2. Tourism Dept Intelligence
*GIS Analytics & Risk Mitigation*

- **GIS Crowd Risk Map:** Renders color-coded markers (🟢 Low, 🟡 Medium, 🔴 High) powered by Leaflet.js.
- **Predictive Logistics:** Automated advisories for transport, sanitation, medical services, and security.
- **District Analytics:** Real-time footfall distribution and high-density risk monitoring.

</td>

<td width="33%" valign="top">

### 🎪 3. Live Site Operations
*Real-Time Venue Telemetry*

- **Spectator Telemetry:** Monitors live venue occupancy against safety thresholds with peak alerts.
- **Broadcast Alerts:** Enables site organizers to publish instant notifications directly to tourist feeds.
- **Emergency Dispatch:** Dynamic propagation of critical advisory updates.

</td>

</tr>
</table>

</div>

---

<!-- ======================= SYSTEM ARCHITECTURE ======================= -->

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
                               ┌───────────────────────────┐
                               │  Web Browser / Single UI  │
                               └─────────────┬─────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │     main.py     │  ◄── FastAPI REST Gateway
                                    └────────┬────────┘
                                             │
      ┌──────────────────────┬───────────────┴───────────────┬──────────────────────┐
      ▼                      ▼                               ▼                      ▼
┌──────────────┐      ┌──────────────┐                ┌────────────────┐    ┌──────────────────┐
│  ai_engine   │      │ travel_engine│                │analytics_engine│    │ organizer_engine │
├──────────────┤      ├──────────────┤                ├────────────────┤    ├──────────────────┤
│• Vector Match│      │• Transit Plan│                │• Hotels Data   │    │• Live Telemetry  │
│• Translation │      │• Hotels Data │                │• Crowd Risk    │    │• Broadcast Alerts│
└──────────────┘      └──────────────┘                └────────────────┘    └──────────────────┘
```

---

<!-- ======================= TECH STACK ======================= -->

## 🛠️ Tech Stack & Technologies

<div align="center">

### 💻 Core Backend & API Framework
<p>
  <img src="https://skillicons.dev/icons?i=python,fastapi,postgres,docker&theme=dark" alt="Backend Stack"/>
</p>

### 🎨 Frontend & Mapping Pipeline
<p>
  <img src="https://skillicons.dev/icons?i=html,css,js,tailwind&theme=dark" alt="Frontend Stack"/>
</p>

<br/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Leaflet.js-199900?style=for-the-badge&logo=leaflet&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>

</div>

---

<!-- ======================= QUICK START ======================= -->

## ⚡ Quick Start

Launch the full-stack REST API and interactive web application using a single command:

```bash
# Clone the repository
git clone https://github.com/Tejzraj/YuktiAI.git && cd YuktiAI

# Install dependencies
pip install -r requirements.txt

# Start the application server
uvicorn main:app --reload --port 8000
```

<br/>

<div align="center">

| Service Endpoint | Description | Direct Access |
| :--- | :--- | :--- |
| 🌐 **Live Web Application** | Interactive single-page multi-stakeholder dashboard | [`http://localhost:8000`](http://localhost:8000) |
| 📚 **Swagger OpenAPI Docs** | Interactive API testing interface | [`http://localhost:8000/docs`](http://localhost:8000/docs) |
| 📖 **ReDoc Documentation** | Structural API specification reference | [`http://localhost:8000/redoc`](http://localhost:8000/redoc) |

</div>

---

<!-- ======================= API MATRIX ======================= -->

## 🔌 Multi-Stakeholder API Matrix

| Stakeholder Domain | Core Module | Route Endpoint | Method | Functionality Description |
| :--- | :--- | :--- | :---: | :--- |
| **Festival Core** | `main.py` | `/festivals` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Retrieve complete festival catalog & filtering metadata |
| **Festival Core** | `main.py` | `/festivals/{id}` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Fetch specific festival profile details |
| **AI Intelligence** | `ai_engine.py` | `/recommend` | `<img src="https://img.shields.io/badge/POST-98C379?style=flat-square&logoColor=white"/>` | Execute vector similarity matching against user quiz tags |
| **AI Intelligence** | `ai_engine.py` | `/translate` | `<img src="https://img.shields.io/badge/POST-98C379?style=flat-square&logoColor=white"/>` | Translate UI text dynamically (English, Kannada, Hindi) |
| **Travel & Logistics** | `travel_engine.py` | `/travel-plan` | `<img src="https://img.shields.io/badge/POST-98C379?style=flat-square&logoColor=white"/>` | Compute multi-modal route options & 2-day itinerary |
| **Travel & Logistics** | `travel_engine.py` | `/hotels/{id}` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Find nearby accommodation options by festival ID |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/overview` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Fetch macro tourism KPIs, total footfall & risk counters |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/map-data` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Generate Leaflet-compatible GeoJSON feature collections |
| **Gov Analytics** | `analytics_engine.py` | `/analytics/trends` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Get district & category footfall distribution metrics |
| **Site Operations** | `organizer_engine.py` | `/organizer/overview/{id}`| `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Monitor live venue spectator stats & safety thresholds |
| **Site Operations** | `organizer_engine.py` | `/organizer/announcement`| `<img src="https://img.shields.io/badge/POST-98C379?style=flat-square&logoColor=white"/>` | Dispatch live emergency or general event broadcasts |
| **Tourist Feed** | `organizer_engine.py` | `/announcements/{id}` | `<img src="https://img.shields.io/badge/GET-61AFEF?style=flat-square&logoColor=white"/>` | Stream broadcast announcements to tourist dashboard |

---

<!-- ======================= TESTING ======================= -->

## 🧪 Verification & Automated Testing

Verify system integrity across all 12 backend endpoints with the automated integration suite:

```bash
python test_full_prototype.py
```

### 📋 Test Suite Execution Output:

```text
================================================================
🚀 Running SanskritiPulse AI Full Prototype Test Suite
================================================================

Testing [GET] / (Single-Page Web UI) ........................ ✅ PASSED (HTTP 200)
Testing [GET] /festivals (Get Festivals) .................... ✅ PASSED (HTTP 200)
Testing [POST] /recommend (AI Recommendation) ............... ✅ PASSED (HTTP 200)
Testing [POST] /translate (Multilingual Translation) ........ ✅ PASSED (HTTP 200)
Testing [POST] /travel-plan (Travel Route & Itinerary) ...... ✅ PASSED (HTTP 200)
Testing [GET] /hotels/mysuru-dasara (Nearby Hotels Search) .. ✅ PASSED (HTTP 200)
Testing [GET] /analytics/overview (Analytics Overview) ...... ✅ PASSED (HTTP 200)
Testing [GET] /analytics/map-data (GIS Map GeoJSON) ......... ✅ PASSED (HTTP 200)
Testing [GET] /analytics/trends (Analytics Trends) ......... ✅ PASSED (HTTP 200)
Testing [GET] /organizer/overview/mysuru-dasara (Site Ops) .. ✅ PASSED (HTTP 200)
Testing [POST] /organizer/announcement (Publish Broadcast) ... ✅ PASSED (HTTP 200)
Testing [GET] /announcements/mysuru-dasara (Fetch Feed) ..... ✅ PASSED (HTTP 200)

================================================================
📊 Summary: 12/12 Prototype Routes Verified (HTTP 200 OK)
================================================================
```

---

<!-- ======================= DOCKER ======================= -->

## 🐳 Docker Deployment

Run the complete containerized stack using Docker Compose:

```bash
# Build and launch containers in detached mode
docker-compose up -d --build

# View application logs
docker-compose logs -f
```

---

<!-- ======================= LICENSE & CREDITS ======================= -->

## 📜 License & Author

This project is open-source and licensed under the [MIT License](LICENSE).

<div align="center">

<br/>

<a href="https://github.com/Tejzraj" target="_blank">
  <img src="https://img.shields.io/badge/Author-Likhith%20Raj%20(%40Tejzraj)-58A6FF?style=for-the-badge&logo=github&logoColor=white&labelColor=0D1117" alt="Author"/>
</a>

<br/><br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=130&section=footer" width="100%" alt="Footer Banner"/>

<br/>

<sub>⭐ Built for Cultural Intelligence & Smart Tourism · <a href="https://github.com/Tejzraj/YuktiAI" target="_blank">YuktiAI — SanskritiPulse</a> ⭐</sub>

</div>
