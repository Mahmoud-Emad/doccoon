#!/bin/bash
set -e

echo "=== Doccoon Deployment Script ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Copying from .env.example${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env with your values before running again${NC}"
        exit 1
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
fi

# Function to check if Docker is running
check_docker() {
    if docker info > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start Docker daemon
start_docker() {
    echo "Starting Docker daemon..."
    pkill dockerd 2>/dev/null || true
    sleep 2
    dockerd > /var/log/dockerd.log 2>&1 &
    sleep 10

    if check_docker; then
        echo -e "${GREEN}Docker started successfully${NC}"
    else
        echo -e "${RED}Failed to start Docker${NC}"
        exit 1
    fi
}

# Function to fix Docker storage driver
fix_docker_storage() {
    echo "Configuring Docker storage driver..."
    pkill dockerd 2>/dev/null || true
    sleep 3

    # Unmount any docker mounts
    mount | grep docker | awk '{print $3}' | xargs -I {} umount -l {} 2>/dev/null || true

    # Remove old docker data
    rm -rf /var/lib/docker 2>/dev/null || true

    # Create config directory
    mkdir -p /etc/docker

    # Set vfs storage driver (works on any filesystem)
    cat > /etc/docker/daemon.json << 'EOF'
{
    "storage-driver": "vfs"
}
EOF

    echo "Docker configured with vfs storage driver"
    start_docker
}

# Function to clean Docker
clean_docker() {
    echo "Cleaning Docker..."
    docker system prune -af --volumes 2>/dev/null || true
    docker builder prune -af 2>/dev/null || true
}

# Main deployment
echo ""
echo "Step 1: Checking Docker..."

if ! check_docker; then
    echo "Docker not running, attempting to start..."
    start_docker
fi

if ! check_docker; then
    echo -e "${YELLOW}Docker failed to start, fixing storage driver...${NC}"
    fix_docker_storage
fi

echo ""
echo "Step 2: Building and starting services..."

# Try to build, if it fails with overlay error, fix storage driver
if ! docker compose up --build -d 2>&1 | tee /tmp/docker-build.log; then
    if grep -q "overlay" /tmp/docker-build.log && grep -q "invalid argument" /tmp/docker-build.log; then
        echo -e "${YELLOW}Overlay filesystem error detected, fixing...${NC}"
        fix_docker_storage
        clean_docker
        echo "Retrying build..."
        docker compose up --build -d
    else
        echo -e "${RED}Build failed${NC}"
        cat /tmp/docker-build.log
        exit 1
    fi
fi

echo ""
echo "Step 3: Waiting for services to be ready..."
sleep 10

echo ""
echo "Step 4: Checking service status..."
docker compose ps

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "Services:"
echo "  - Frontend: http://localhost (port 80)"
echo "  - Backend:  http://localhost:8000"
echo "  - Database: PostgreSQL (internal)"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f        # View logs"
echo "  docker compose ps             # Check status"
echo "  docker compose down           # Stop services"
echo "  docker compose restart        # Restart services"
