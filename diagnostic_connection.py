#!/usr/bin/env python3
"""
Modbus 網路連接診斷工具
檢查 IP、端口、防火牆和 Modbus 連接狀態
"""

import socket
import time
import configparser
from pathlib import Path

def test_network_connectivity(host, port, timeout=3):
    """測試網路連接"""
    print(f"\n{'='*60}")
    print(f"🔍 測試網路連接: {host}:{port}")
    print(f"{'='*60}")
    
    try:
        print(f"[1] 嘗試解析 IP 地址: {host}")
        ip = socket.gethostbyname(host)
        print(f"    ✅ 解析成功: {host} -> {ip}")
    except socket.gaierror as e:
        print(f"    ❌ 解析失敗: {e}")
        return False
    
    try:
        print(f"\n[2] 嘗試連接到 {host}:{port} (超時: {timeout}秒)")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"    ✅ 端口開放，可以連接")
            return True
        else:
            print(f"    ❌ 連接失敗 (錯誤代碼: {result})")
            print(f"       可能原因:")
            print(f"       - 目標主機未開機")
            print(f"       - 防火牆阻止了連接")
            print(f"       - 網路路由配置不正確")
            return False
    except socket.timeout:
        print(f"    ❌ 連接超時 - 無法到達主機")
        return False
    except Exception as e:
        print(f"    ❌ 連接錯誤: {e}")
        return False

def test_modbus_connection(host, port, timeout=3):
    """測試 Modbus TCP 連接"""
    print(f"\n{'='*60}")
    print(f"🔍 測試 Modbus TCP 連接")
    print(f"{'='*60}")
    
    try:
        from pymodbus.client import ModbusTcpClient
        
        print(f"[1] 建立 Modbus TCP 客戶端")
        client = ModbusTcpClient(host=host, port=port, timeout=timeout)
        
        print(f"[2] 連接到伺服器...")
        if client.connect():
            print(f"    ✅ Modbus 連接成功")
            
            print(f"\n[3] 嘗試讀取寄存器以驗證通訊")
            result = client.read_holding_registers(0, 1)
            
            if result.isError():
                print(f"    ⚠️  讀取失敗: {result}")
            else:
                print(f"    ✅ 讀取成功: {result.registers}")
            
            client.close()
            print(f"\n    ✅ Modbus 通訊正常")
            return True
        else:
            print(f"    ❌ Modbus 連接失敗")
            return False
    except Exception as e:
        print(f"    ❌ Modbus 錯誤: {e}")
        return False

def load_config():
    """載入配置文件"""
    config_path = Path("config/config.ini")
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return None
    
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

def main():
    print("\n" + "="*60)
    print("🤖 機械臂 Modbus 連接診斷工具")
    print("="*60)
    
    # 載入配置
    config = load_config()
    if not config:
        return
    
    try:
        host = config.get('MODBUS', 'HOST', fallback='127.0.0.1')
        port = config.getint('MODBUS', 'PORT', fallback=5020)
        timeout = config.getint('MODBUS', 'TIMEOUT', fallback=3)
    except Exception as e:
        print(f"❌ 讀取配置失敗: {e}")
        return
    
    print(f"\n📋 當前配置:")
    print(f"   HOST: {host}")
    print(f"   PORT: {port}")
    print(f"   TIMEOUT: {timeout}秒")
    
    # 測試網路連接
    network_ok = test_network_connectivity(host, port, timeout=timeout)
    
    if not network_ok:
        print(f"\n{'='*60}")
        print("❌ 網路連接失敗")
        print(f"{'='*60}")
        print("\n🔧 故障排除建議:")
        print("   1. 檢查網路線是否正確連接")
        print("   2. 確認目標主機 IP 地址是否正確")
        print("   3. 確認目標主機是否已開機")
        print("   4. 檢查防火牆設置，確保允許 TCP 端口通訊")
        print("   5. 嘗試在命令行執行: ping " + host)
        print("   6. 嘗試在命令行執行: Test-NetConnection -ComputerName " + host + " -Port " + str(port))
        return
    
    # 測試 Modbus 連接
    modbus_ok = test_modbus_connection(host, port, timeout=timeout)
    
    print(f"\n{'='*60}")
    if modbus_ok:
        print("✅ 所有診斷測試通過 - 連接正常")
    else:
        print("⚠️  部分診斷測試失敗 - 需要進一步檢查")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
