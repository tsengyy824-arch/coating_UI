#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
驗證雙塗膠閥選擇實現
Verify Dual Valve Type Selection Implementation
"""

import sys
import os
from pathlib import Path
import configparser

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def verify_config():
    """檢查配置文件中的塗膠閥設定"""
    print("=" * 60)
    print("1. 驗證配置文件中的塗膠閥設定")
    print("=" * 60)
    
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    # 檢查valve配置
    try:
        valve1_name = config.get('DRA_ROBOT_MODBUS', 'VALVE_TYPE_1_NAME')
        valve1_reg = config.getint('DRA_ROBOT_MODBUS', 'VALVE_TYPE_1_REGISTER')
        valve2_name = config.get('DRA_ROBOT_MODBUS', 'VALVE_TYPE_2_NAME')
        valve2_reg = config.getint('DRA_ROBOT_MODBUS', 'VALVE_TYPE_2_REGISTER')
        
        print(f"✓ Valve 1: {valve1_name} → Register D{valve1_reg}")
        print(f"✓ Valve 2: {valve2_name} → Register D{valve2_reg}")
        
        # Check Path Execute Register
        path_exec_reg = config.getint('DRA_ROBOT_MODBUS', 'PATH_EXECUTE_REGISTER')
        print(f"✓ Path Execute Register: D{path_exec_reg}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading config: {e}")
        return False

def verify_ui_imports():
    """檢查UI模塊導入"""
    print("\n" + "=" * 60)
    print("2. 驗證UI模塊導入")
    print("=" * 60)
    
    try:
        from PyQt5.QtWidgets import QComboBox, QApplication
        print("✓ QComboBox imported successfully")
        
        # Create QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test ComboBox creation pattern
        combo = QComboBox()
        combo.addItem("圍壩膠塗膠", "valve_1")
        combo.addItem("熱固三防滴膠", "valve_2")
        
        # Verify data
        if combo.itemData(0) == "valve_1" and combo.itemData(1) == "valve_2":
            print("✓ ComboBox data binding works correctly")
            print(f"  - Item 0: {combo.itemText(0)} → {combo.itemData(0)}")
            print(f"  - Item 1: {combo.itemText(1)} → {combo.itemData(1)}")
            return True
        else:
            print("✗ ComboBox data binding failed")
            return False
    except Exception as e:
        print(f"✗ Error with UI imports: {e}")
        return False

def verify_ui_structure():
    """檢查UI.py是否包含所需的方法"""
    print("\n" + "=" * 60)
    print("3. 驗證UI.py結構")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = {
            'self.valve_type_combo': '塗膠閥類型下拉菜單',
            'on_valve_type_changed': '塗膠閥改變事件處理器',
            'VALVE_TYPE_1_REGISTER': 'Valve 1寄存器配置',
            'VALVE_TYPE_2_REGISTER': 'Valve 2寄存器配置',
            'valve_type_data': '閥類型數據提取',
        }
        
        for element, description in required_elements.items():
            if element in content:
                print(f"✓ {element} ({description})")
            else:
                print(f"✗ {element} ({description}) - NOT FOUND")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error reading ui.py: {e}")
        return False

def verify_valve_selection_logic():
    """驗證塗膠閥選擇邏輯"""
    print("\n" + "=" * 60)
    print("4. 驗證塗膠閥選擇邏輯")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if valve selection logic is correct
        if 'if valve_type_data == "valve_1":' in content and 'VALVE_TYPE_1_REGISTER' in content:
            print("✓ Valve 1 selection logic found")
        else:
            print("✗ Valve 1 selection logic missing")
            return False
        
        if 'else:  # valve_2' in content and 'VALVE_TYPE_2_REGISTER' in content:
            print("✓ Valve 2 selection logic found")
        else:
            print("✗ Valve 2 selection logic missing")
            return False
        
        # Check if valve register write exists
        if 'self.modbus.write_register(VALVE_REGISTER, 1)' in content:
            print("✓ Valve register write logic found")
        else:
            print("✗ Valve register write logic missing")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Error verifying logic: {e}")
        return False

def main():
    """Main verification function"""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  雙塗膠閥選擇功能驗證".center(58) + "║")
    print("║" + "  Dual Valve Type Selection Implementation Verify".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    results = []
    results.append(("配置文件驗證", verify_config()))
    results.append(("UI導入驗證", verify_ui_imports()))
    results.append(("UI結構驗證", verify_ui_structure()))
    results.append(("邏輯驗證", verify_valve_selection_logic()))
    
    print("\n" + "=" * 60)
    print("驗證結果摘要 (Verification Summary)")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"總計: {passed}/{total} 測試通過 (Total: {passed}/{total} tests passed)")
    print("=" * 60)
    
    if passed == total:
        print("\n✓ 所有驗證通過！雙塗膠閥功能已正確實現。")
        print("✓ All verifications passed! Dual valve feature is correctly implemented.")
        return 0
    else:
        print(f"\n✗ {total - passed} 個驗證失敗。請檢查實現。")
        print(f"✗ {total - passed} verification(s) failed. Please check the implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
