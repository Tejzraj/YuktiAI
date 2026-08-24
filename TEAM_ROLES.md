# 👥 YuktiAi — Team Roles & Architecture Matrix

This document outlines the assigned roles, core deliverables, and technical handoff points for all team members on the YuktiAi project.

---

## 🚀 Status: Day 1 Core Backend is LIVE

> [!NOTE]
> **Tezraj's Core Database and REST API endpoints are fully active, seeded, and CORS-enabled.**  
> All team members (Nandish, Simran, Monika, Janvi, and Tanishi) can immediately pull and connect to `http://localhost:8000`.

---

## 🏛️ Team Member Responsibilities & Deliverables

| Team Member | Role | Core Deliverables | Consumed APIs / Endpoints |
| :--- | :--- | :--- | :--- |
| **Tezraj** | **Database & Core APIs** *(Lead Backend)* | • PostgreSQL 15 schema ([`init.sql`](init.sql))<br>• Docker orchestration ([`docker-compose.yml`](docker-compose.yml))<br>• Dataset ingestion & seeding pipeline ([`seed.py`](seed.py))<br>• Core REST APIs & CORS Middleware ([`main.py`](main.py))<br>• One-click developer setup ([`run_pipeline.sh`](run_pipeline.sh)) | *Provides all base endpoints to the team* |
| **Nandish** | **AI / NLP & Recommendation** | • AI-powered festival recommendation algorithm<br>• Semantic search & NLP tag embeddings<br>• Cultural sentiment analysis & interest-based filtering | `GET /festivals`<br>`GET /festivals/{id}` |
| **Simran** | **Travel Planner & Hotels** | • Multi-day cultural itinerary generator<br>• Hotel distance & price comparison cards<br>• Transit routes, estimated costs, and travel durations | `GET /festivals/{id}` *(hotels & travel_options arrays)* |
| **Monika** | **Tourist Dashboard UI** | • Interactive tourist web / mobile interface<br>• Geo-map discovery with pins (`lat`/`lng`)<br>• Rich media carousels, food guides & attractions view | `GET /festivals?district=...`<br>`GET /festivals?category=...`<br>`GET /festivals/{id}` |
| **Janvi** | **Government Dashboard** | • State tourism analytics & analytics reporting<br>• Footfall forecasting & crowd heatmaps<br>• Economic impact & seasonal tourism trends | `GET /festivals`<br>`GET /festivals?date=...` |
| **Tanishi** | **Organizer Dashboard & Integration** | • Festival organizer portal & event management<br>• Schedule, performer & stall management<br>• End-to-end frontend/backend integration testing | `GET /festivals`<br>`GET /festivals/{id}` |

---

## 🔌 API Integration Quick Reference for Teammates

All teammates can fetch data with zero CORS restrictions from any browser frontend or backend script:

### 1. Monika (Tourist Dashboard) & Janvi (Government Dashboard)
- **Fetch Festivals List:**
  ```javascript
  const response = await fetch("http://localhost:8000/festivals");
  const { count, data } = await response.json();
  ```
- **Filter by District or Category:**
  ```javascript
  const response = await fetch("http://localhost:8000/festivals?district=Mysuru&category=Heritage");
  const { data } = await response.json();
  ```

### 2. Simran (Travel & Hotels) & Tanishi (Organizer & Detailed View)
- **Fetch Single Festival with Hotels & Travel:**
  ```javascript
  const res = await fetch("http://localhost:8000/festivals/1");
  const festival = await res.json();
  console.log(festival.hotels); // Embedded list of nearby hotels
  console.log(festival.travel_options); // Modes of transit, duration, costs
  console.log(festival.images); // HD media gallery URLs
  ```

### 3. Nandish (AI & NLP Pipelines)
- **Python Integration for ML / Vector Search:**
  ```python
  import requests

  festivals = requests.get("http://localhost:8000/festivals").json()["data"]
  for fest in festivals:
      text_corpus = f"{fest['name']} {fest['cultural_significance']} {' '.join(fest['activities'])}"
      # Generate embeddings or train recommendation pipeline
  ```

---

## 🛠️ Getting Started in 1 Minute

To pull the latest updates from Tezraj and run everything locally:

```bash
git pull origin main
chmod +x run_pipeline.sh && ./run_pipeline.sh
```
Interactive documentation is instantly available at [http://localhost:8000/docs](http://localhost:8000/docs).
