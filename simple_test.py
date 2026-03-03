"""
簡單的 Modbus 寫入測試
"""
from pymodbus.client import ModbusTcpClient
import time

print("=== 簡單 Modbus 測試 ===")
print("連接到 192.168.1.103:502...")

# 創建客戶端
client = ModbusTcpClient("192.168.1.103", port=502, timeout=10)

# 連接
if client.connect():
    print("✅ TCP 連接成功\n")
    
    # 測試不同的 device_id
    for device_id in [0, 1, 255]:
        print(f"\n--- 測試 device_id={device_id} ---")
        
        # 嘗試寫入 DO-3（圍壩膠氣缸伸出）
        # 寄存器 766 (0x02FE), 值 0x0004
        print(f"寫入寄存器 766, 值 0x0004, device_id={device_id}")
        
        try:
            result = client.write_register(766, 0x0004, slave=device_id)
            print(f"   結果: {result}")
            
            if hasattr(result, 'isError') and result.isError():
                print(f"   ❌ 錯誤: {result}")
            else:
                print(f"   ✅ 成功!")
                
                # 讀回確認
                time.sleep(0.5)
                read_result = client.read_holding_registers(764, 2, slave=device_id)
                if hasattr(read_result, 'registers'):
                    print(f"   讀回寄存器 764: 0x{read_result.registers[0]:04X}")
                
        except Exception as e:
            print(f"   ❌ 異常: {e}")
        
        time.sleep(1)
    
    client.close()
    print("\n連接已關閉")
else:
    print("❌ 無法建立 TCP 連接")

print("\n=== 測試完成 ===")
