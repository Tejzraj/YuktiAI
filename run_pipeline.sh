#!/usr/bin/env bash

# ==============================================================================
# SanskritiPulse AI - One-Click Developer Pipeline Setup
# ==============================================================================
# Automates environment verification, container spin-up, dependency installation,
# database seeding, and REST API server initialization.
# ==============================================================================

set -e

# Color definitions for visual clarity
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}"
echo "================================================================="
echo "   🚀 SANSKRITIPULSE AI — AUTOMATED BACKEND PIPELINE SETUP"
echo "================================================================="
echo -e "${NC}"

# 1. Dependency Checks: Git, Python 3, Docker
echo -e "${BLUE}▶ Step 1: Checking System Prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Git is installed: $(git --version)"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.10+${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Python 3 is installed: $(python3 --version)"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker & Docker Desktop.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker is installed: $(docker --version)"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker Desktop and retry.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker daemon is actively running"

echo ""

# 2. Launch PostgreSQL Container via Docker Compose
echo -e "${BLUE}▶ Step 2: Spinning up PostgreSQL Container...${NC}"

if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}❌ docker compose plugin or docker-compose binary not found.${NC}"
    exit 1
fi

$DOCKER_COMPOSE_CMD up -d
echo -e "  ${GREEN}✓${NC} PostgreSQL container started on port 5432"

# Wait for PostgreSQL to be ready to accept connections
echo -e "  ${YELLOW}⏳ Waiting for PostgreSQL database to be healthy...${NC}"
MAX_RETRIES=20
RETRY_COUNT=0
until docker exec sanskritipulse_postgres pg_isready -U postgres &> /dev/null || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ Timed out waiting for PostgreSQL to start. Check docker logs with: docker logs sanskritipulse_postgres${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} PostgreSQL is fully initialized and accepting connections!"

echo ""

# 3. Setup Python Virtual Environment
echo -e "${BLUE}▶ Step 3: Configuring Python Virtual Environment...${NC}"

VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "  Creating virtual environment at ./${VENV_DIR}..."
    python3 -m venv "$VENV_DIR"
    echo -e "  ${GREEN}✓${NC} Virtual environment created"
else
    echo -e "  ${GREEN}✓${NC} Existing virtual environment found"
fi

# Activate virtual environment
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# 4. Install Dependencies
echo -e "${BLUE}▶ Step 4: Installing Project Dependencies...${NC}"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo -e "  ${GREEN}✓${NC} Dependencies successfully installed from requirements.txt"

echo ""

# 5. Populate Database with Seed Data
echo -e "${BLUE}▶ Step 5: Seeding Database with Cultural Festival Datasets...${NC}"
python seed.py
echo -e "  ${GREEN}✓${NC} Seeding completed successfully"

echo ""

# 6. Launch FastAPI Server
echo -e "${GREEN}${BOLD}=================================================================${NC}"
echo -e "${GREEN}${BOLD}   🎉 SETUP COMPLETE! STARTING SANSKRITIPULSE REST API SERVER    ${NC}"
echo -e "${GREEN}${BOLD}=================================================================${NC}"
echo -e "${CYAN}  • Base API:        ${BOLD}http://localhost:8000${NC}"
echo -e "${CYAN}  • Swagger Docs:    ${BOLD}http://localhost:8000/docs${NC}"
echo -e "${CYAN}  • ReDoc:           ${BOLD}http://localhost:8000/redoc${NC}"
echo -e "${CYAN}  • Filter Endpoint: ${BOLD}http://localhost:8000/festivals?district=Mysuru${NC}"
echo -e "${GREEN}${BOLD}=================================================================${NC}"
echo ""

exec uvicorn main:app --reload --port 8000
