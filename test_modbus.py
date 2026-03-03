"""
Modbus 通訊測試腳本
用於診斷 DRA 連接問題
"""

import sys
import time
from src.modbus_client import ModbusClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_modbus_connection():
    """測試 Modbus 連接和基本讀寫功能"""
    
    # 創建 Modbus 客戶端
    client = ModbusClient(
        host="192.168.1.103",
        port=502,
        timeout=10,
        retries=3
    )
    
    print("\n=== DRA Modbus 通訊測試 ===")
    print("正在連接到 192.168.1.103:502...")
    
    # 1. 測試連接
    if not client.connect():
        print("❌ 連接失敗")
        return False
    
    print("✅ TCP 連接成功")
    time.sleep(1)
    
    # 2. 測試讀取 - 機器人運動狀態 (寄存器 224)
    print("\n測試 1: 讀取機器人運動狀態 (寄存器 224 / 0x00E0)")
    result = client.read_register(224, 1)
    if result is not None:
        print(f"✅ 讀取成功: {result[0]} (0: 停止; 1: 動作中)")
    else:
        print("❌ 讀取失敗")
    
    time.sleep(1)
    
    # 3. 測試讀取 - 控制器預備狀態 (寄存器 514)
    print("\n測試 2: 讀取控制器預備狀態 (寄存器 514 / 0x0202)")
    result = client.read_register(514, 1)
    if result is not None:
        print(f"✅ 讀取成功: {result[0]}")
    else:
        print("❌ 讀取失敗")
    
    time.sleep(1)
    
    # 4. 測試讀取 - 用戶輸出 DO 資訊 (寄存器 764)
    print("\n測試 3: 讀取用戶輸出 DO 資訊 (寄存器 764 / 0x02FC)")
    result = client.read_register(764, 2)
    if result is not None:
        print(f"✅ 讀取成功: {result}")
        print(f"   DO 狀態: 0x{result[0]:04X} (二進制: {bin(result[0])})")
    else:
        print("❌ 讀取失敗")
    
    time.sleep(1)
    
    # 5. 測試寫入 - 寫入 DO-3 (圍壩膠氣缸伸出)
    print("\n測試 4: 寫入 DO-3 (寄存器 766 / 0x02FE, 值: 0x0004)")
    result = client.write_do(766, 0x0004)
    if result:
        print("✅ 寫入成功")
        
        # 讀回確認
        time.sleep(0.5)
        print("   讀回確認...")
        check = client.read_register(764, 2)
        if check is not None:
            print(f"   當前 DO 狀態: 0x{check[0]:04X} (二進制: {bin(check[0])})")
    else:
        print("❌ 寫入失敗")
    
    time.sleep(1)
    
    # 6. 清除 DO
    print("\n測試 5: 清除所有 DO (寄存器 766 / 0x02FE, 值: 0x0000)")
    result = client.write_do(766, 0x0000)
    if result:
        print("✅ 寫入成功")
    else:
        print("❌ 寫入失敗")
    
    client.disconnect()
    print("\n=== 測試完成 ===")
    
    return True

if __name__ == "__main__":
    try:
        test_modbus_connection()
    except KeyboardInterrupt:
        print("\n用戶中斷測試")
    except Exception as e:
        print(f"\n測試出現錯誤: {e}")
        import traceback
        traceback.print_exc()
