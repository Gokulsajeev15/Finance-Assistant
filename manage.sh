#!/bin/bash

# 🚀 Finance Assistant - Project Management Script
# Usage: ./manage.sh [command]
# Commands: start, stop, clean, test, dev, build

set -e

PROJECT_NAME="Finance Assistant"
BASE_URL="http://localhost:8000"
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}🚀 $PROJECT_NAME - $1${NC}"
    echo "=================================="
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    # Check if we're in the right directory
    if [ ! -f "pyproject.toml" ]; then
        print_error "Please run this from the Finance-Assistant root directory"
        exit 1
    fi

    # Check uv
    if ! command -v uv &> /dev/null; then
        print_error "uv is required but not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi

    # Check node/npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed. Install Node.js from: https://nodejs.org"
        exit 1
    fi
}

setup_env() {
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_warning "Please edit .env file and add your OpenAI API key"
        print_warning "Get your key from: https://platform.openai.com/api-keys"
        return 1
    fi
    return 0
}

start_backend() {
    print_header "Starting Backend Server"
    
    if setup_env; then
        echo "🐍 Starting Python backend on port $BACKEND_PORT..."
        cd "$(dirname "$0")"
        uv run python start_backend.py &
        BACKEND_PID=$!
        echo $BACKEND_PID > .backend.pid
        
        # Wait a moment for server to start
        sleep 3
        
        if curl -s "$BASE_URL/docs" > /dev/null; then
            print_success "Backend started successfully!"
            echo "📖 API Documentation: $BASE_URL/docs"
            echo "🔗 API Base URL: $BASE_URL"
        else
            print_error "Backend failed to start properly"
            return 1
        fi
    else
        print_error "Please configure .env file first"
        return 1
    fi
}

start_frontend() {
    print_header "Starting Frontend Development Server"
    
    echo "⚛️  Starting React frontend on port $FRONTEND_PORT..."
    cd frontend
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    npm run dev &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../.frontend.pid
    cd ..
    
    sleep 3
    print_success "Frontend started successfully!"
    echo "🌐 Frontend URL: http://localhost:$FRONTEND_PORT"
}

stop_services() {
    print_header "Stopping Services"
    
    # Stop backend
    if [ -f ".backend.pid" ]; then
        BACKEND_PID=$(cat .backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            print_success "Backend stopped"
        fi
        rm -f .backend.pid
    fi
    
    # Stop frontend  
    if [ -f ".frontend.pid" ]; then
        FRONTEND_PID=$(cat .frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            print_success "Frontend stopped"
        fi
        rm -f .frontend.pid
    fi
    
    # Kill any remaining processes on our ports
    lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true
    lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null || true
}

clean_project() {
    print_header "Cleaning Project"
    
    echo "🧹 Cleaning Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    
    echo "🧹 Cleaning Node.js cache..."
    rm -rf frontend/node_modules/.cache 2>/dev/null || true
    rm -rf frontend/dist 2>/dev/null || true
    
    echo "🧹 Cleaning temporary files..."
    rm -f .backend.pid .frontend.pid
    rm -f *.log
    
    print_success "Project cleaned!"
}

test_apis() {
    print_header "Testing APIs"
    
    # Check if backend is running
    if ! curl -s "$BASE_URL/docs" > /dev/null; then
        print_error "Backend is not running. Start it first with: ./manage.sh start"
        exit 1
    fi
    
    echo "🧪 Testing Company Search..."
    if curl -s "$BASE_URL/api/v1/companies/search?q=apple" | grep -q "Apple"; then
        print_success "Company search working"
    else
        print_error "Company search failed"
    fi
    
    echo "🧪 Testing Technical Analysis..."
    if curl -s "$BASE_URL/api/v1/technical-analysis/AAPL" | grep -q "ticker"; then
        print_success "Technical analysis working"
    else
        print_error "Technical analysis failed"
    fi
    
    echo "🧪 Testing AI Chat..."
    if curl -s -X POST "$BASE_URL/api/v1/ai/query?query=Hello" | grep -q "success"; then
        print_success "AI chat working"
    else
        print_warning "AI chat may not be configured (check OpenAI API key)"
    fi
    
    print_success "API tests completed!"
}

dev_mode() {
    print_header "Starting Development Mode"
    
    check_dependencies
    
    # Stop any existing services
    stop_services
    
    # Start both services
    start_backend
    if [ $? -eq 0 ]; then
        start_frontend
        
        print_success "Development environment ready!"
        echo ""
        echo "🔗 Frontend: http://localhost:$FRONTEND_PORT"
        echo "🔗 Backend API: $BASE_URL"
        echo "📖 API Docs: $BASE_URL/docs"
        echo ""
        echo "Press Ctrl+C to stop all services"
        
        # Wait for interrupt
        trap stop_services INT
        wait
    fi
}

build_frontend() {
    print_header "Building Frontend for Production"
    
    cd frontend
    
    echo "📦 Installing dependencies..."
    npm install
    
    echo "🏗️  Building production build..."
    npm run build
    
    cd ..
    print_success "Frontend built successfully!"
    echo "📁 Build files are in: frontend/dist/"
}

show_help() {
    echo "🚀 Finance Assistant - Project Management"
    echo ""
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start     - Start backend server only"
    echo "  dev       - Start both backend and frontend in development mode"
    echo "  stop      - Stop all running services"
    echo "  clean     - Clean cache files and temporary data"
    echo "  test      - Test all API endpoints"
    echo "  build     - Build frontend for production"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh dev     # Start development environment"
    echo "  ./manage.sh test    # Test all APIs"
    echo "  ./manage.sh clean   # Clean project files"
}

# Main command handling
case "${1:-help}" in
    "start")
        check_dependencies
        start_backend
        ;;
    "dev")
        dev_mode
        ;;
    "stop")
        stop_services
        ;;
    "clean")
        clean_project
        ;;
    "test")
        test_apis
        ;;
    "build")
        build_frontend
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
