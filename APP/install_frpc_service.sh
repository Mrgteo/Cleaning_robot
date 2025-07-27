#!/bin/bash
# FRP客户端服务安装脚本

set -e

echo "🚀 FRP客户端服务安装脚本"
echo "=========================="

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo运行此脚本"
    echo "用法: sudo bash install_frpc_service.sh"
    exit 1
fi

# 获取当前目录
CURRENT_DIR=$(pwd)
PROJECT_DIR="/home/sunrise/rj/qs"

echo "📁 当前目录: $CURRENT_DIR"
echo "📁 项目目录: $PROJECT_DIR"

# 检查必要文件
echo "🔍 检查必要文件..."

if [ ! -f "$PROJECT_DIR/frpc.ini" ]; then
    echo "❌ 未找到frpc.ini配置文件"
    echo "请确保在项目目录下运行: cd $PROJECT_DIR"
    exit 1
fi

if [ ! -f "/usr/bin/frpc" ]; then
    echo "❌ 未找到frpc可执行文件"
    echo "请先安装frpc客户端"
    exit 1
fi

echo "✅ 必要文件检查完成"

# 检查用户是否存在
if ! id "sunrise" &>/dev/null; then
    echo "❌ 用户 'sunrise' 不存在"
    echo "请修改frpc.service文件中的用户名"
    exit 1
fi

echo "✅ 用户检查完成"

# 复制服务文件
echo "📋 安装systemd服务..."

if [ -f "$CURRENT_DIR/frpc.service" ]; then
    cp "$CURRENT_DIR/frpc.service" /etc/systemd/system/
    echo "✅ 服务文件已复制到 /etc/systemd/system/"
else
    echo "❌ 未找到frpc.service文件"
    exit 1
fi

# 设置文件权限
chmod 644 /etc/systemd/system/frpc.service
echo "✅ 服务文件权限已设置"

# 重新加载systemd
echo "🔄 重新加载systemd..."
systemctl daemon-reload

# 启用服务
echo "⚡ 启用frpc服务..."
systemctl enable frpc.service

# 启动服务
echo "🚀 启动frpc服务..."
systemctl start frpc.service

# 等待一下让服务启动
sleep 3

# 检查服务状态
echo "📊 检查服务状态..."
if systemctl is-active --quiet frpc.service; then
    echo "✅ frpc服务运行正常"
else
    echo "⚠️ frpc服务可能有问题"
fi

# 显示服务状态
echo ""
echo "📋 服务状态:"
systemctl status frpc.service --no-pager -l

echo ""
echo "🎉 安装完成!"
echo ""
echo "📋 常用命令:"
echo "  查看状态: sudo systemctl status frpc"
echo "  启动服务: sudo systemctl start frpc"
echo "  停止服务: sudo systemctl stop frpc"
echo "  重启服务: sudo systemctl restart frpc"
echo "  查看日志: sudo journalctl -u frpc -f"
echo "  禁用开机启动: sudo systemctl disable frpc"
echo ""
echo "🔧 如需修改配置:"
echo "  1. 编辑 $PROJECT_DIR/frpc.ini"
echo "  2. 重启服务: sudo systemctl restart frpc"
