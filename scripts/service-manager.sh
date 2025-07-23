#!/bin/bash

# 服务管理主脚本
# 用于管理前端和后端服务

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_SCRIPT="$SCRIPT_DIR/backend-service.sh"
FRONTEND_SCRIPT="$SCRIPT_DIR/frontend-service.sh"
LOG_DIR="$PROJECT_ROOT/logs"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

info() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# 检查脚本是否存在并可执行
check_scripts() {
    local missing=0
    
    if [ ! -f "$BACKEND_SCRIPT" ]; then
        error "Backend script not found: $BACKEND_SCRIPT"
        missing=1
    elif [ ! -x "$BACKEND_SCRIPT" ]; then
        warning "Making backend script executable..."
        chmod +x "$BACKEND_SCRIPT"
    fi
    
    if [ ! -f "$FRONTEND_SCRIPT" ]; then
        error "Frontend script not found: $FRONTEND_SCRIPT"
        missing=1
    elif [ ! -x "$FRONTEND_SCRIPT" ]; then
        warning "Making frontend script executable..."
        chmod +x "$FRONTEND_SCRIPT"
    fi
    
    if [ $missing -eq 1 ]; then
        error "Missing service scripts. Please ensure all scripts are present."
        return 1
    fi
    
    info "Service scripts are ready"
    return 0
}

# 启动所有服务
start_all() {
    log "Starting all services..."
    echo ""
    
    # 启动后端
    echo -e "${PURPLE}=== Starting Backend Service ===${NC}"
    if ! "$BACKEND_SCRIPT" start; then
        error "Failed to start backend service"
        return 1
    fi
    
    echo ""
    
    # 启动前端
    echo -e "${PURPLE}=== Starting Frontend Service ===${NC}"
    if ! "$FRONTEND_SCRIPT" start; then
        error "Failed to start frontend service"
        warning "Backend service is still running"
        return 1
    fi
    
    echo ""
    success "All services started successfully!"
    
    # 显示服务状态
    show_status
}

# 停止所有服务
stop_all() {
    log "Stopping all services..."
    echo ""
    
    # 停止前端
    echo -e "${PURPLE}=== Stopping Frontend Service ===${NC}"
    "$FRONTEND_SCRIPT" stop || true
    
    echo ""
    
    # 停止后端
    echo -e "${PURPLE}=== Stopping Backend Service ===${NC}"
    "$BACKEND_SCRIPT" stop || true
    
    echo ""
    success "All services stopped"
}

# 重启所有服务
restart_all() {
    log "Restarting all services..."
    stop_all
    sleep 3
    start_all
}

# 显示所有服务状态
show_status() {
    log "Checking service status..."
    echo ""
    
    echo -e "${PURPLE}=== Backend Service Status ===${NC}"
    "$BACKEND_SCRIPT" status
    
    echo ""
    
    echo -e "${PURPLE}=== Frontend Service Status ===${NC}"
    "$FRONTEND_SCRIPT" status
    
    echo ""
    
    # 总结
    local backend_running=$("$BACKEND_SCRIPT" status >/dev/null 2>&1 && echo "true" || echo "false")
    local frontend_running=$("$FRONTEND_SCRIPT" status >/dev/null 2>&1 && echo "true" || echo "false")
    
    echo -e "${PURPLE}=== Summary ===${NC}"
    if [ "$backend_running" = "true" ] && [ "$frontend_running" = "true" ]; then
        success "All services are running"
        info "Backend API: http://localhost:8000"
        info "Frontend App: http://localhost:5173"
        info "API Docs: http://localhost:8000/docs"
    elif [ "$backend_running" = "true" ]; then
        warning "Only backend service is running"
    elif [ "$frontend_running" = "true" ]; then
        warning "Only frontend service is running"
    else
        warning "No services are running"
    fi
}

# 健康检查所有服务
health_check_all() {
    log "Performing health check on all services..."
    echo ""
    
    local backend_healthy=false
    local frontend_healthy=false
    
    echo -e "${PURPLE}=== Backend Health Check ===${NC}"
    if "$BACKEND_SCRIPT" health; then
        backend_healthy=true
    fi
    
    echo ""
    
    echo -e "${PURPLE}=== Frontend Health Check ===${NC}"
    if "$FRONTEND_SCRIPT" health; then
        frontend_healthy=true
    fi
    
    echo ""
    echo -e "${PURPLE}=== Health Check Summary ===${NC}"
    
    if $backend_healthy && $frontend_healthy; then
        success "All services are healthy"
        return 0
    elif $backend_healthy; then
        warning "Backend is healthy, frontend has issues"
        return 1
    elif $frontend_healthy; then
        warning "Frontend is healthy, backend has issues"
        return 1
    else
        error "Both services have health issues"
        return 1
    fi
}

# 查看综合日志
view_logs() {
    local service="${1:-all}"
    local lines="${2:-50}"
    
    case "$service" in
        backend)
            "$BACKEND_SCRIPT" logs "$lines"
            ;;
        frontend)
            "$FRONTEND_SCRIPT" logs "$lines"
            ;;
        all|*)
            echo -e "${PURPLE}=== Backend Logs (last $lines lines) ===${NC}"
            "$BACKEND_SCRIPT" logs "$lines"
            echo ""
            echo -e "${PURPLE}=== Frontend Logs (last $lines lines) ===${NC}"
            "$FRONTEND_SCRIPT" logs "$lines"
            ;;
    esac
}

# 查看错误日志
view_error_logs() {
    local service="${1:-all}"
    local lines="${2:-50}"
    
    case "$service" in
        backend)
            "$BACKEND_SCRIPT" error-logs "$lines"
            ;;
        frontend)
            "$FRONTEND_SCRIPT" error-logs "$lines"
            ;;
        all|*)
            echo -e "${PURPLE}=== Backend Error Logs (last $lines lines) ===${NC}"
            "$BACKEND_SCRIPT" error-logs "$lines"
            echo ""
            echo -e "${PURPLE}=== Frontend Error Logs (last $lines lines) ===${NC}"
            "$FRONTEND_SCRIPT" error-logs "$lines"
            ;;
    esac
}

# 开发模式启动
dev_start() {
    log "Starting development environment..."
    echo ""
    
    # 首先启动后端
    echo -e "${PURPLE}=== Starting Backend (Development) ===${NC}"
    if ! "$BACKEND_SCRIPT" start; then
        error "Failed to start backend service"
        return 1
    fi
    
    echo ""
    info "Waiting for backend to be ready..."
    sleep 5
    
    # 检查后端健康状态
    if ! "$BACKEND_SCRIPT" health >/dev/null 2>&1; then
        warning "Backend health check failed, but continuing..."
    fi
    
    # 启动前端
    echo -e "${PURPLE}=== Starting Frontend (Development) ===${NC}"
    if ! "$FRONTEND_SCRIPT" start; then
        error "Failed to start frontend service"
        return 1
    fi
    
    echo ""
    success "Development environment started!"
    echo ""
    info "🌐 Frontend: http://localhost:5173"
    info "🔗 Backend API: http://localhost:8000"
    info "📚 API Documentation: http://localhost:8000/docs"
    info "📊 API Redoc: http://localhost:8000/redoc"
    echo ""
    info "Use 'service-manager.sh logs' to view logs"
    info "Use 'service-manager.sh stop' to stop all services"
}

# 生产构建
production_build() {
    log "Building for production..."
    echo ""
    
    # 构建前端
    echo -e "${PURPLE}=== Building Frontend ===${NC}"
    if ! "$FRONTEND_SCRIPT" build; then
        error "Frontend build failed"
        return 1
    fi
    
    echo ""
    
    # 运行测试（如果有的话）
    echo -e "${PURPLE}=== Running Tests ===${NC}"
    if [ -f "$PROJECT_ROOT/backend/run_tests.sh" ]; then
        cd "$PROJECT_ROOT/backend"
        if ! ./run_tests.sh; then
            warning "Some tests failed"
        fi
    else
        info "No test script found, skipping tests"
    fi
    
    echo ""
    success "Production build completed"
}

# 清理日志
cleanup_logs() {
    log "Cleaning up old logs..."
    
    local days=${1:-7}
    
    # 清理超过指定天数的日志文件
    find "$LOG_DIR" -name "*.log" -type f -mtime +$days -delete 2>/dev/null || true
    find "$LOG_DIR" -name "*.log.*" -type f -mtime +$days -delete 2>/dev/null || true
    
    success "Cleaned up logs older than $days days"
}

# 显示系统信息
show_system_info() {
    echo -e "${PURPLE}=== System Information ===${NC}"
    echo "OS: $(uname -s)"
    echo "Kernel: $(uname -r)"
    echo "Architecture: $(uname -m)"
    echo "Hostname: $(hostname)"
    echo "User: $(whoami)"
    echo "Working Directory: $(pwd)"
    echo "Project Root: $PROJECT_ROOT"
    echo ""
    
    if command -v python3 >/dev/null 2>&1; then
        echo "Python: $(python3 --version)"
    fi
    
    if command -v node >/dev/null 2>&1; then
        echo "Node.js: $(node --version)"
    fi
    
    if command -v npm >/dev/null 2>&1; then
        echo "npm: $(npm --version)"
    fi
    
    echo ""
    echo "Log Directory: $LOG_DIR"
    if [ -d "$LOG_DIR" ]; then
        echo "Log Files:"
        ls -la "$LOG_DIR"
    fi
}

# 显示帮助
show_help() {
    echo -e "${PURPLE}Service Manager - 小新RPA在线平台${NC}"
    echo ""
    echo "Usage: $0 {command} [options]"
    echo ""
    echo -e "${CYAN}Main Commands:${NC}"
    echo "  start           Start all services"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show all services status"
    echo "  dev             Start development environment"
    echo ""
    echo -e "${CYAN}Monitoring Commands:${NC}"
    echo "  health          Perform health check on all services"
    echo "  logs [service] [lines]   Show logs (service: all|backend|frontend)"
    echo "  error-logs [service] [lines]  Show error logs"
    echo ""
    echo -e "${CYAN}Build Commands:${NC}"
    echo "  build           Build for production"
    echo ""
    echo -e "${CYAN}Maintenance Commands:${NC}"
    echo "  cleanup [days]  Clean up logs older than N days (default: 7)"
    echo "  info            Show system information"
    echo ""
    echo -e "${CYAN}Individual Service Commands:${NC}"
    echo "  backend {cmd}   Run backend service command"
    echo "  frontend {cmd}  Run frontend service command"
    echo ""
    echo -e "${CYAN}Help:${NC}"
    echo "  help            Show this help message"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  $0 dev                    # Start development environment"
    echo "  $0 logs backend 100       # Show last 100 backend logs"
    echo "  $0 backend status         # Check backend status"
    echo "  $0 frontend build         # Build frontend"
    echo "  $0 cleanup 3              # Clean logs older than 3 days"
}

# 主函数
main() {
    # 检查脚本
    if ! check_scripts; then
        exit 1
    fi
    
    case "${1:-help}" in
        start)
            start_all
            ;;
        stop)
            stop_all
            ;;
        restart)
            restart_all
            ;;
        status)
            show_status
            ;;
        dev)
            dev_start
            ;;
        health)
            health_check_all
            ;;
        logs)
            view_logs "$2" "$3"
            ;;
        error-logs)
            view_error_logs "$2" "$3"
            ;;
        build)
            production_build
            ;;
        cleanup)
            cleanup_logs "$2"
            ;;
        info)
            show_system_info
            ;;
        backend)
            shift
            "$BACKEND_SCRIPT" "$@"
            ;;
        frontend)
            shift
            "$FRONTEND_SCRIPT" "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"