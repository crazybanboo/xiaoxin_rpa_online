#!/bin/bash

# 开发环境快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting Development Environment..."
echo "======================================="

exec "$SCRIPT_DIR/scripts/service-manager.sh" dev