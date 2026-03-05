#!/usr/bin/env python3
"""
Delta DRV 硬體診斷工具 (進階版)
使用正式的 Modbus 地址表進行診斷
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import configparser
from src.modbus_client import ModbusClient
import time

def test_with_address_table():
    """使用完整地址表進行測試"""
    
    # 載入配置
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    host = config.get('MODBUS', 'HOST')
    port = config.getint('MODBUS', 'PORT')
    
    print("="*70)
    print("🤖 Delta DRV 機械臂 Modbus 診斷測試 (進階版)")
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
    
    # 讀取控制器狀態
    print(f"\n[步驟 2] 讀取控制器狀態")
    print(f"   嘗試讀取寄存器 0x0138 (系統狀態)...")
    try:
        result = modbus.read_register(0x0138, count=1)
        if result:
            print(f"   ✅ 系統狀態: {result[0]} (0=正常, 2=暫停, 3=運行+暫停)")
        else:
            print(f"   ⚠️  無法讀取")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}")
    
    # 讀取控制器就緒狀態
    print(f"\n[步驟 3] 讀取控制器就緒狀態")
    print(f"   嘗試讀取寄存器 0x0202 (控制器就緒)...")
    try:
        result = modbus.read_register(0x0202, count=1)
        if result:
            print(f"   ✅ 控制器就緒狀態: {result[0]}")
        else:
            print(f"   ⚠️  無法讀取")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}")
    
    # 測試基本寫入 - 寫入 DO (用戶 DO 控制)
    print(f"\n[步驟 4] 測試基本寫入操作 (User DO Control)")
    print(f"   嘗試寫入寄存器 0x02FE (User DO Control)...")
    try:
        # 先寫入 0x0001
        print(f"   寫入值: 0x0001")
        result = modbus.write_do(0x02FE, 0x0001)
        print(f"   結果: {'✅ 成功' if result else '❌ 失敗'}")
        if not result:
            print(f"   錯誤詳情: {modbus.last_error}")
        
        time.sleep(0.5)
        
        # 再寫入 0x0000 (關閉)
        print(f"   寫入值: 0x0000")
        result = modbus.write_do(0x02FE, 0x0000)
        print(f"   結果: {'✅ 成功' if result else '❌ 失敗'}")
        if not result:
            print(f"   錯誤詳情: {modbus.last_error}")
    except Exception as e:
        print(f"   ❌ 異常: {e}")
    
    time.sleep(1)
    
    # 測試 Servo OFF (確保安全)
    print(f"\n[步驟 5] 執行 Servo OFF (關閉伺服 - 安全操作)")
    print(f"   寄存器: 0x0010 (J1~J6 Servo)")
    print(f"   寫入值: 0x0002 (Servo OFF)")
    result_off = modbus.servo_off()
    print(f"   結果: {'✅ 成功' if result_off else '❌ 失敗'}")
    if not result_off:
        print(f"   錯誤詳情: {modbus.last_error}")
    
    time.sleep(1)
    
    # 測試 Servo ON
    print(f"\n[步驟 6] 執行 Servo ON (啟動伺服)")
    print(f"   寄存器: 0x0010 (J1~J6)  ")
    print(f"   寫入值: 0x0001 (Servo ON)")
    result_on = modbus.servo_on()
    print(f"   結果: {'✅ 成功' if result_on else '❌ 失敗'}")
    if not result_on:
        print(f"   錯誤詳情: {modbus.last_error}")
    
    time.sleep(1)
    
    # 再次 Servo OFF 以保持安全
    print(f"\n[步驟 7] 再次執行 Servo OFF (保持安全)")
    result_off2 = modbus.servo_off()
    print(f"   結果: {'✅ 成功' if result_off2 else '❌ 失敗'}")
    
    # 關閉連接
    print(f"\n[步驟 8] 關閉連接...")
    modbus.disconnect()
    print(f"   ✅ 連接已關閉")
    
    # 摘要
    print("\n" + "="*70)
    print("📊 測試摘要")
    print("="*70)
    print(f"Servo ON:  {'✅ 成功' if result_on else '❌ 失敗'}")
    print(f"Servo OFF: {'✅ 成功' if result_off else '❌ 失敗'}")
    
    if result_on and result_off:
        print("\n✅ 所有測試通過 - 硬體通訊正常")
    elif result_on or result_off:
        print("\n⚠️  部分測試成功 - 可能存在硬體問題")
    else:
        print("\n❌ 測試失敗")
        print("\n🔧 可能的故障排除:")
        print("   1. 檢查硬體是否已開機")
        print("   2. 檢查網路連接")
        print("   3. 確認 IP 地址和端口是否正確")
        print("   4. 檢查防火牆設置")
        print("   5. 查看硬體手冊確認寄存器地址")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    test_with_address_table()
