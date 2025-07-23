#!/bin/bash

# 开发环境状态检查脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📊 Checking Development Environment Status..."
echo "============================================="

exec "$SCRIPT_DIR/scripts/service-manager.sh" status