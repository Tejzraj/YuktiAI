# 🛠️ Developer Setup & Pipeline Guide — YuktiAi

This document provides zero-friction instructions to set up, seed, and run the complete backend service on any fresh macOS, Linux, or Windows machine. Built by **Tezraj** for teammates **Nandish**, **Simran**, **Monika**, **Janvi**, and **Tanishi** (see [`TEAM_ROLES.md`](TEAM_ROLES.md)).

---

## ⚡ Quickstart (One-Line Setup)

Clone the repository and run the automated pipeline script:

```bash
git clone https://github.com/Tejzraj/YuktiAI.git
cd YuktiAI
chmod +x run_pipeline.sh && ./run_pipeline.sh
```

### What `run_pipeline.sh` Automates:
1. **Validates System Prerequisites:** Checks for `git`, `python3` (3.10+), `docker`, and verifies the Docker daemon is running.
2. **PostgreSQL Containerization:** Starts the PostgreSQL 15 database container via `docker compose up -d` and waits until the database is healthy.
3. **Virtual Environment:** Automatically creates and activates `./venv`.
4. **Dependency Management:** Installs and upgrades all required packages from `requirements.txt`.
5. **Database Seeding:** Automatically runs `seed.py` to ingest 30+ Karnataka festival records with images, hotels, and transit routes.
6. **Starts API Server:** Boots the FastAPI server with live-reloading on [http://localhost:8000](http://localhost:8000).

---

## 💻 Manual Setup (Step-by-Step)

If you prefer running commands manually or are on Windows PowerShell:

### 1. Clone the Repository
```bash
git clone https://github.com/Tejzraj/YuktiAI.git
cd YuktiAI
```

### 2. Start PostgreSQL Container
```bash
docker compose up -d
```

### 3. Create & Activate Virtual Environment
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Seed the Database
```bash
python seed.py
```

### 6. Start the REST API
```bash
uvicorn main:app --reload --port 8000
```

---

## 🔍 Verifying the Service

Once started, test these URLs in your browser or with `curl`:
- **API Status:** [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI Interactive Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Get All Festivals:** [http://localhost:8000/festivals](http://localhost:8000/festivals)
- **Filter by District:** [http://localhost:8000/festivals?district=Mysuru](http://localhost:8000/festivals?district=Mysuru)
- **Get Specific Festival:** [http://localhost:8000/festivals/1](http://localhost:8000/festivals/1)

---

## 🔧 Troubleshooting & Common Issues

### 1. Docker Daemon Not Running
**Symptom:** `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`  
**Fix:** 
- Open **Docker Desktop** application on your machine and wait for the status indicator to turn green.
- On Linux, start the system service: `sudo systemctl start docker`.

---

### 2. Port 5432 or 8000 Already in Use
**Symptom:** `bind: address already in use` or `[Errno 48] Address already in use`

- **Port 5432 (PostgreSQL Conflict):**
  If you have a local PostgreSQL server running outside Docker:
  - Stop local PostgreSQL:
    - **macOS (Homebrew):** `brew services stop postgresql`
    - **Linux:** `sudo systemctl stop postgresql`
    - **Windows:** Open Services (`services.msc`), find `postgresql-x64-XX` and click **Stop**.
  - Alternatively, change the host port mapping in `docker-compose.yml` (e.g., `"5433:5432"`), and update `DB_CONFIG` / `POSTGRES_PORT=5433`.

- **Port 8000 (FastAPI Conflict):**
  To find and kill the process using port 8000:
  - **macOS / Linux:** `lsof -ti:8000 | xargs kill -9`
  - **Windows (PowerShell):**
    ```powershell
    Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
    ```
  - Or run Uvicorn on another port:
    ```bash
    uvicorn main:app --reload --port 8080
    ```

---

### 3. Python Virtual Environment Permissions / Execution Policy
**Symptom (Windows):** `cannot be loaded because running scripts is disabled on this system.`  
**Fix:** Run PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 4. Database Reset & Fresh Re-Seeding
If you need to wipe existing records and re-seed from scratch:
```bash
# Clean reset tables and identity keys
python seed.py --reset
```
Or restart the entire Docker container and its volume:
```bash
docker compose down -v
docker compose up -d
python seed.py
```
