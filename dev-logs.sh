#!/bin/bash

# 开发环境日志查看脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📋 Viewing Development Logs..."
echo "=============================="

exec "$SCRIPT_DIR/scripts/service-manager.sh" logs "$@"