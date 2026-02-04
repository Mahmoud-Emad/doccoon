#!/bin/bash
set -e

echo "=== Doccoon Deployment Script ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# ============================================
# Step 1: Install required packages
# ============================================
echo ""
echo -e "${GREEN}Step 1: Installing required packages...${NC}"

apt-get update
apt-get install -y git curl vim

echo -e "${GREEN}Packages installed${NC}"

# ============================================
# Step 2: Setup environment file
# ============================================
echo ""
echo -e "${GREEN}Step 2: Setting up environment file...${NC}"

if [ ! -f .env ]; then
    cat > .env << 'EOF'
# ===========================================
# Doccoon Environment Configuration
# ===========================================

# Environment
ENV=production
DJANGO_DEBUG=False

# Security - CHANGE THESE!
DJANGO_SECRET_KEY=change-this-to-a-random-secret-key-in-production

# Domain Configuration
SERVER_DOMAIN_NAME=api.doccoon.com
CLIENT_DOMAIN_NAME=doccoon.com

# Database (used by Docker)
DATABASE_NAME=doccoon
DATABASE_USER=doccoon
DATABASE_PASSWORD=doccoon_password_change_me
DATABASE_HOST=db
DATABASE_PORT=5432

# Frontend API URL
VITE_API_BASE_URL=http://localhost:8000/api

# OAuth (optional)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# VITE_GOOGLE_CLIENT_ID=
# GITHUB_CLIENT_ID=
# GITHUB_CLIENT_SECRET=
# VITE_GITHUB_CLIENT_ID=

# Email (optional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL=
# EMAIL_PASSWORD=
EOF
    echo -e "${YELLOW}.env file created. Please edit it with your values:${NC}"
    echo "  nano .env"
    echo ""
    echo -e "${YELLOW}Then run this script again.${NC}"
    exit 0
else
    echo -e "${GREEN}.env file already exists${NC}"
fi

# ============================================
# Step 3: Install Docker
# ============================================
echo ""
echo -e "${GREEN}Step 3: Checking Docker installation...${NC}"

if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."

    # Install Docker using official script
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh

    echo -e "${GREEN}Docker installed${NC}"
else
    echo -e "${GREEN}Docker already installed${NC}"
fi

# Check if Docker daemon is running
check_docker() {
    docker info > /dev/null 2>&1
}

start_docker() {
    echo "Starting Docker daemon..."

    # Try systemctl first
    if command -v systemctl &> /dev/null && systemctl is-system-running &> /dev/null; then
        systemctl start docker
        systemctl enable docker
    else
        # Fallback: start dockerd directly
        pkill dockerd 2>/dev/null || true
        sleep 2
        dockerd > /var/log/dockerd.log 2>&1 &
        sleep 10
    fi
}

if ! check_docker; then
    start_docker
fi

if ! check_docker; then
    echo -e "${RED}Failed to start Docker. Please check manually.${NC}"
    exit 1
fi

echo -e "${GREEN}Docker is running${NC}"

# ============================================
# Step 4: Fix Docker storage driver if needed
# ============================================
fix_docker_storage() {
    echo -e "${YELLOW}Fixing Docker storage driver...${NC}"

    # Stop Docker
    if command -v systemctl &> /dev/null && systemctl is-system-running &> /dev/null; then
        systemctl stop docker
    else
        pkill dockerd 2>/dev/null || true
    fi
    sleep 3

    # Unmount docker mounts
    mount | grep docker | awk '{print $3}' | xargs -I {} umount -l {} 2>/dev/null || true

    # Remove old docker data
    rm -rf /var/lib/docker 2>/dev/null || true

    # Configure vfs storage driver
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json << 'EOF'
{
    "storage-driver": "vfs"
}
EOF

    # Start Docker
    start_docker
    sleep 5

    if check_docker; then
        echo -e "${GREEN}Docker storage driver fixed${NC}"
    else
        echo -e "${RED}Failed to fix Docker. Please check manually.${NC}"
        exit 1
    fi
}

# ============================================
# Step 5: Build and deploy
# ============================================
echo ""
echo -e "${GREEN}Step 4: Building and deploying services...${NC}"

# Function to deploy
deploy() {
    docker compose down 2>/dev/null || true
    docker compose up --build -d
}

# Try to deploy, fix storage driver if overlay error occurs
if ! deploy 2>&1 | tee /tmp/docker-build.log; then
    if grep -q "overlay" /tmp/docker-build.log && grep -q "invalid argument" /tmp/docker-build.log; then
        echo -e "${YELLOW}Overlay filesystem error detected. Fixing...${NC}"
        fix_docker_storage
        docker system prune -af 2>/dev/null || true
        echo "Retrying deployment..."
        deploy
    else
        echo -e "${RED}Deployment failed. Check logs above.${NC}"
        exit 1
    fi
fi

# ============================================
# Step 6: Wait and verify
# ============================================
echo ""
echo -e "${GREEN}Step 5: Waiting for services to start...${NC}"
sleep 15

echo ""
echo -e "${GREEN}Step 6: Checking service status...${NC}"
docker compose ps

# ============================================
# Done
# ============================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}       Deployment Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Services running:"
echo "  Frontend: http://localhost (port 80)"
echo "  Backend:  http://localhost:8000"
echo "  Database: PostgreSQL (internal)"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f        # View logs"
echo "  docker compose ps             # Check status"
echo "  docker compose down           # Stop services"
echo "  docker compose restart        # Restart services"
echo ""
