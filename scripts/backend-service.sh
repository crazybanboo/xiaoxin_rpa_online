#!/bin/bash

# 后端服务管理脚本
# 用于启动、停止、重启和监控后端服务

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
LOG_DIR="$PROJECT_ROOT/logs"
PID_FILE="$LOG_DIR/backend.pid"
LOG_FILE="$LOG_DIR/backend.log"
ERROR_LOG_FILE="$LOG_DIR/backend-error.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# 检查进程是否运行
is_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            # PID文件存在但进程不存在，清理PID文件
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# 获取进程状态
get_status() {
    if is_running; then
        local pid=$(cat "$PID_FILE")
        local cpu_usage=$(ps -p "$pid" -o %cpu --no-headers 2>/dev/null || echo "N/A")
        local memory_usage=$(ps -p "$pid" -o %mem --no-headers 2>/dev/null || echo "N/A")
        local start_time=$(ps -p "$pid" -o lstart --no-headers 2>/dev/null || echo "N/A")
        
        success "Backend service is running"
        echo "  PID: $pid"
        echo "  CPU Usage: ${cpu_usage}%"
        echo "  Memory Usage: ${memory_usage}%"
        echo "  Started: $start_time"
        return 0
    else
        warning "Backend service is not running"
        return 1
    fi
}

# 启动服务
start_service() {
    log "Starting backend service..."
    
    if is_running; then
        warning "Backend service is already running (PID: $(cat "$PID_FILE"))"
        return 0
    fi
    
    # 检查后端目录
    if [ ! -d "$BACKEND_DIR" ]; then
        error "Backend directory not found: $BACKEND_DIR"
        return 1
    fi
    
    # 进入后端目录
    cd "$BACKEND_DIR"
    
    # 检查虚拟环境
    if [ ! -d ".env" ]; then
        error "Virtual environment not found. Please run: python -m venv .env"
        return 1
    fi
    
    # 激活虚拟环境
    source .env/bin/activate
    
    # 检查依赖
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt not found"
        return 1
    fi
    
    # 启动服务（后台运行）
    log "Starting uvicorn server..."
    nohup python -m uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        > "$LOG_FILE" 2> "$ERROR_LOG_FILE" &
    
    local pid=$!
    echo "$pid" > "$PID_FILE"
    
    # 等待服务启动
    sleep 3
    
    if is_running; then
        success "Backend service started successfully (PID: $pid)"
        log "Logs: $LOG_FILE"
        log "Error logs: $ERROR_LOG_FILE"
        
        # 显示最近的日志
        if [ -f "$LOG_FILE" ]; then
            echo ""
            log "Recent logs:"
            tail -n 10 "$LOG_FILE"
        fi
    else
        error "Failed to start backend service"
        if [ -f "$ERROR_LOG_FILE" ]; then
            echo ""
            error "Error logs:"
            tail -n 10 "$ERROR_LOG_FILE"
        fi
        return 1
    fi
}

# 停止服务
stop_service() {
    log "Stopping backend service..."
    
    if ! is_running; then
        warning "Backend service is not running"
        return 0
    fi
    
    local pid=$(cat "$PID_FILE")
    
    # 发送TERM信号
    kill -TERM "$pid" 2>/dev/null || true
    
    # 等待进程结束
    local count=0
    while is_running && [ $count -lt 30 ]; do
        sleep 1
        ((count++))
    done
    
    if is_running; then
        warning "Process did not stop gracefully, forcing termination..."
        kill -KILL "$pid" 2>/dev/null || true
        sleep 2
    fi
    
    if ! is_running; then
        rm -f "$PID_FILE"
        success "Backend service stopped successfully"
    else
        error "Failed to stop backend service"
        return 1
    fi
}

# 重启服务
restart_service() {
    log "Restarting backend service..."
    stop_service
    sleep 2
    start_service
}

# 查看日志
view_logs() {
    local lines=${1:-50}
    
    if [ -f "$LOG_FILE" ]; then
        log "Showing last $lines lines of backend logs:"
        echo "----------------------------------------"
        tail -n "$lines" "$LOG_FILE"
    else
        warning "Log file not found: $LOG_FILE"
    fi
}

# 查看错误日志
view_error_logs() {
    local lines=${1:-50}
    
    if [ -f "$ERROR_LOG_FILE" ]; then
        log "Showing last $lines lines of backend error logs:"
        echo "----------------------------------------"
        tail -n "$lines" "$ERROR_LOG_FILE"
    else
        warning "Error log file not found: $ERROR_LOG_FILE"
    fi
}

# 实时监控日志
monitor_logs() {
    if [ -f "$LOG_FILE" ]; then
        log "Monitoring backend logs (Press Ctrl+C to stop):"
        echo "----------------------------------------"
        tail -f "$LOG_FILE"
    else
        warning "Log file not found: $LOG_FILE"
    fi
}

# 健康检查
health_check() {
    log "Performing health check..."
    
    if ! is_running; then
        error "Service is not running"
        return 1
    fi
    
    # 检查API健康状态
    local health_response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:8000/api/health 2>/dev/null || echo "000")
    
    if [ "$health_response" = "200" ]; then
        success "Health check passed"
        return 0
    else
        error "Health check failed (HTTP: $health_response)"
        return 1
    fi
}

# 显示帮助
show_help() {
    echo "Backend Service Management Script"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|error-logs|monitor|health|help}"
    echo ""
    echo "Commands:"
    echo "  start       Start the backend service"
    echo "  stop        Stop the backend service"
    echo "  restart     Restart the backend service"
    echo "  status      Show service status"
    echo "  logs [N]    Show last N lines of logs (default: 50)"
    echo "  error-logs [N] Show last N lines of error logs (default: 50)"
    echo "  monitor     Monitor logs in real-time"
    echo "  health      Perform health check"
    echo "  help        Show this help message"
    echo ""
    echo "Files:"
    echo "  PID file: $PID_FILE"
    echo "  Log file: $LOG_FILE"
    echo "  Error log: $ERROR_LOG_FILE"
}

# 主函数
main() {
    case "${1:-help}" in
        start)
            start_service
            ;;
        stop)
            stop_service
            ;;
        restart)
            restart_service
            ;;
        status)
            get_status
            ;;
        logs)
            view_logs "$2"
            ;;
        error-logs)
            view_error_logs "$2"
            ;;
        monitor)
            monitor_logs
            ;;
        health)
            health_check
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"