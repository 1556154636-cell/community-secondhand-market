#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
社区二手交易平台 - 启动脚本
"""

import os
import sys
import subprocess
import platform

def main():
    print("="*60)
    print("     邻里闲置 - 社区二手交易平台")
    print("         Community Secondhand Market")
    print("="*60)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj2.settings')
    
    print("\n📋 系统信息:")
    print(f"  Python版本: {sys.version}")
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  当前目录: {os.getcwd()}")
    
    try:
        import django
        print(f"  Django版本: {django.VERSION}")
    except ImportError:
        print("  ⚠️  Django未安装，请先安装依赖")
        return
    
    print("\n🚀 启动开发服务器...")
    print("  服务器地址: http://localhost:5000")
    print("  管理后台: http://localhost:5000/admin")
    print("\n按 Ctrl+C 停止服务器")
    print("-"*60)
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:5000'])
    except KeyboardInterrupt:
        print("\n✋ 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")
        print("\n💡 可能的解决方案:")
        print("  1. 确保已安装所有依赖: pip install -r requirements.txt")
        print("  2. 确保MySQL数据库已启动")
        print("  3. 检查dj2/settings.py中的数据库配置")

if __name__ == '__main__':
    main()
