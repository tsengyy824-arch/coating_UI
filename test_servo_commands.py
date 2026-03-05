#!/usr/bin/env python3
"""
Servo ON/OFF 命令測試診斷
直接測試 Servo ON 和 Servo OFF 命令
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import configparser
from src.modbus_client import ModbusClient
import time

def test_servo_commands():
    # 載入配置
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    host = config.get('MODBUS', 'HOST')
    port = config.getint('MODBUS', 'PORT')
    
    print("="*70)
    print("🤖 Servo ON/OFF 命令測試")
    print("="*70)
    
    print(f"\n📋 配置信息:")
    print(f"   HOST: {host}")
    print(f"   PORT: {port}")
    
    # 建立連接
    print(f"\n[步驟 1] 建立 Modbus 連接...")
    modbus = ModbusClient(host=host, port=port, timeout=10)
    
    if not modbus.connect():
        print(f"   ❌ 連接失敗: {modbus.last_error}")
        return
    
    print(f"   ✅ 連接成功")
    
    # 讀取當前伺服狀態
    print(f"\n[步驟 2] 讀取寄存器 D16 (伺服狀態)...")
    try:
        result = modbus.read_register(16, count=1)
        if result:
            print(f"   ✅ 讀取成功: {result}")
        else:
            print(f"   ⚠️  讀取返回 None")
    except Exception as e:
        print(f"   ⚠️  讀取異常: {e}")
    
    # 測試 Servo ON
    print(f"\n[步驟 3] 執行 Servo ON...")
    print(f"   寫入: D16 = 1")
    result_on = modbus.servo_on()
    print(f"   結果: {'✅ 成功' if result_on else '❌ 失敗'}")
    if not result_on:
        print(f"   錯誤詳情: {modbus.last_error}")
    
    time.sleep(1)
    
    # 讀取伺服狀態
    print(f"\n[步驟 4] 確認伺服狀態 (Servo ON 後)...")
    try:
        result = modbus.read_register(16, count=1)
        if result:
            print(f"   寄存器 D16: {result}")
        else:
            print(f"   讀取返回 None")
    except Exception as e:
        print(f"   異常: {e}")
    
    time.sleep(1)
    
    # 測試 Servo OFF
    print(f"\n[步驟 5] 執行 Servo OFF...")
    print(f"   寫入: D16 = 2")
    result_off = modbus.servo_off()
    print(f"   結果: {'✅ 成功' if result_off else '❌ 失敗'}")
    if not result_off:
        print(f"   錯誤詳情: {modbus.last_error}")
    
    time.sleep(1)
    
    # 讀取伺服狀態
    print(f"\n[步驟 6] 確認伺服狀態 (Servo OFF 後)...")
    try:
        result = modbus.read_register(16, count=1)
        if result:
            print(f"   寄存器 D16: {result}")
        else:
            print(f"   讀取返回 None")
    except Exception as e:
        print(f"   異常: {e}")
    
    # 關閉連接
    print(f"\n[步驟 7] 關閉連接...")
    modbus.disconnect()
    print(f"   ✅ 連接已關閉")
    
    print("\n" + "="*70)
    print("✅ 測試完成")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_servo_commands()
