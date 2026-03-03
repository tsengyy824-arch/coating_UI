"""
Pymodbus 3.x API 測試
"""
from pymodbus.client import ModbusTcpClient
import time

print("=== Pymodbus 3.x API 測試 ===")
print("連接到 192.168.1.103:502...")

client = ModbusTcpClient("192.168.1.103", port=502, timeout=10)

if client.connect():
    print("✅ TCP 連接成功\n")
    
    # 測試 1: 不帶 slave/unit 參數
    print("測試 1: write_register(766, 0x0004) - 不帶 slave 參數")
    try:
        result = client.write_register(766, 0x0004)
        print(f"   結果類型: {type(result)}")
        print(f"   結果: {result}")
        if hasattr(result, 'isError'):
            if result.isError():
                print(f"   ❌ Modbus 錯誤")
            else:
                print(f"   ✅ 成功!")
        else:
            print(f"   ✅ 可能成功（無isError屬性）")
    except Exception as e:
        print(f"   ❌ 異常: {e}")
    
    time.sleep(2)
    
    # 測試 2: 使用 unit 參數
    print("\n測試 2: write_register(766, 0x0004, unit=1)")
    try:
        result = client.write_register(766, 0x0004, unit=1)
        print(f"   結果: {result}")
        if hasattr(result, 'isError'):
            if result.isError():
                print(f"   ❌ Modbus 錯誤")
            else:
                print(f"   ✅ 成功!")
        else:
            print(f"   ✅ 可能成功")
    except Exception as e:
        print(f"   ❌ 異常: {e}")
    
    time.sleep(2)
    
    # 測試 3: 讀取測試
    print("\n測試 3: 讀取寄存器 764")
    try:
        result = client.read_holding_registers(764, 2, unit=1)
        print(f"   結果: {result}")
        if hasattr(result, 'registers'):
            print(f"   寄存器值: {result.registers}")
            print(f"   寄存器 764: 0x{result.registers[0]:04X}")
            print(f"   ✅ 讀取成功!")
        elif hasattr(result, 'isError') and result.isError():
            print(f"   ❌ Modbus 錯誤")
    except Exception as e:
        print(f"   ❌ 異常: {e}")
    
    client.close()
    print("\n連接已關閉")
else:
    print("❌ 無法建立 TCP 連接")

print("\n=== 測試完成 ===")
