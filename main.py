"""
機械臂控制系統 - 主程序入口
"""

import sys
import os

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui import main

if __name__ == '__main__':
    main()