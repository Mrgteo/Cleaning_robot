# -*- coding: utf-8 -*-
"""
简化配置文件 - 只包含RTSP和FRP配置
"""

# 摄像头配置
CAMERA_CONFIG = {
    "device": "/dev/video0",  # 摄像头设备路径
    "width": 640,             # 视频宽度
    "height": 480,            # 视频高度
    "fps": 30,                # 帧率
    "format": "yuyv422",      # 视频格式
}

# FFmpeg编码配置
FFMPEG_CONFIG = {
    "codec": "libx264",       # 视频编码器
    "preset": "ultrafast",    # 编码预设
    "bitrate": "800k",        # 码率
    "profile": "baseline",    # H.264配置文件
    "level": "3.0",           # H.264级别
}

# MediaMTX配置
MEDIAMTX_CONFIG = {
    "executable": "./mediamtx",  # MediaMTX可执行文件路径
    "config": "mediamtx.yml",    # 配置文件路径
}

# 流配置
STREAM_CONFIG = {
    "name": "live",           # 流名称
    "protocol": "rtsp",       # 协议
}

# RTSP服务器配置
RTSP_CONFIG = {
    "host": "localhost",
    "port": 8554,
    "stream_path": "live",
}

# FRP内网穿透配置
FRP_CONFIG = {
    "enabled": True,  # 是否启用内网穿透
    "server_addr": "103.40.14.14",  # FRP服务器地址
    "server_port": 8000,  # FRP服务器端口
    "token": "",  # FRP服务器token（如果需要）
    "user": "camera_user",  # 用户名前缀
    "metadata_id": "ENqfs5JH4K",  # 元数据ID
    "heartbeat_interval": 120,  # 心跳间隔
    "heartbeat_timeout": 240,  # 心跳超时
    "proxies": {
        "rtsp": {
            "name": "271a8aee-4f11-421d-a7fb-1c254ecbc594",
            "type": "tcp",
            "local_ip": "127.0.0.1",
            "local_port": 8554,
            "remote_port": 0,  # 0表示由服务器分配
        },
        "ssh": {
            "name": "e0b8af85-19dc-4198-b5b6-57b500eee0c1",
            "type": "tcp", 
            "local_ip": "127.0.0.1",
            "local_port": 22,
            "remote_port": 0,  # 0表示由服务器分配
        }
    }
}

def get_rtsp_url():
    """获取RTSP流地址"""
    return f"rtsp://{RTSP_CONFIG['host']}:{RTSP_CONFIG['port']}/{RTSP_CONFIG['stream_path']}"

def get_frp_rtsp_url():
    """获取FRP远程RTSP流地址"""
    return f"rtsp://{FRP_CONFIG['server_addr']}:33577/{RTSP_CONFIG['stream_path']}"
