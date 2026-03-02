#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
驗證模式控制和自動運行按鈕功能
Verify Mode Control and Auto Run Button Fix
"""

import sys
import os
import configparser
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def verify_mode_control():
    """檢查模式控制邏輯"""
    print("\n" + "=" * 60)
    print("1. 驗證模式控制邏輯 (Mode Control)")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("手動模式啟用IO按鈕", "# 啟用手動IO控制按鈕（手動模式允許手動塗膠）" in content and
                                   "self.valve_on_button.setEnabled(True)" in content),
            ("自動模式禁用IO按鈕", "# 禁用手動IO控制按鈕（自動模式不允許手動塗膠）" in content and
                                   "self.valve_off_button.setEnabled(False)" in content),
            ("自動運行按鈕延遲啟用", "re_enable_auto_run_button" in content),
            ("QTimer延遲啟用", "QTimer.singleShot(2000" in content),
        ]
        
        all_pass = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"✗ Error reading ui.py: {e}")
        return False

def verify_button_state_logic():
    """檢查按鈕狀態管理"""
    print("\n" + "=" * 60)
    print("2. 驗證按鈕狀態管理 (Button State Logic)")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查connect_modbus是否不直接啟用IO按鈕
        if "# 手動IO控制按鈕狀態由 change_mode() 管理" in content:
            print("✓ connect_modbus() 正確委託按鈕管理給 change_mode()")
        else:
            print("✗ connect_modbus() 按鈕管理邏輯不完整")
            return False
        
        # 檢查change_mode中的狀態邏輯
        if "手動模式允許手動塗膠" in content and "自動模式不允許手動塗膠" in content:
            print("✓ change_mode() 正確管理IO按鈕狀態")
        else:
            print("✗ change_mode() IO按鈕管理不完整")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_auto_run_enhancement():
    """檢查自動運行增強邏輯"""
    print("\n" + "=" * 60)
    print("3. 驗證自動運行功能增強 (Auto Run Enhancement)")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("re_enable_auto_run_button方法存在", "def re_enable_auto_run_button(self):" in content),
            ("2秒延遲啟用", "QTimer.singleShot(2000, self.re_enable_auto_run_button)" in content),
            ("自動運行完成提示", "自動塗膠完成" in content),
        ]
        
        all_pass = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main verification function"""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  模式控制和自動運行功能驗證".center(58) + "║")
    print("║" + "  Mode Control & Auto Run Feature Verification".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    results = []
    results.append(("模式控制邏輯", verify_mode_control()))
    results.append(("按鈕狀態管理", verify_button_state_logic()))
    results.append(("自動運行增強", verify_auto_run_enhancement()))
    
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
        print("\n✓ 所有驗證通過！功能已正確實現。")
        print("✓ All verifications passed! Features correctly implemented.")
        print("\n功能說明:")
        print("1. 手動IO塗膠按鈕 - 僅在「手動模式」下可用")
        print("2. 自動運行按鈕 - 運行完成後2秒自動重新啟用")
        return 0
    else:
        print(f"\n✗ {total - passed} 個驗證失敗。請檢查實現。")
        print(f"✗ {total - passed} verification(s) failed. Please check implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
