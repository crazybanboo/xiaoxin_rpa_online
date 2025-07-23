#!/bin/bash

# 开发环境快速停止脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🛑 Stopping Development Environment..."
echo "======================================"

exec "$SCRIPT_DIR/scripts/service-manager.sh" stop