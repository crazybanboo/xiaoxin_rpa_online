-- 小新RPA在线平台数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS xiaoxin_rpa;

-- 使用数据库
\c xiaoxin_rpa;

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建基础表结构将在后续任务中通过SQLAlchemy创建