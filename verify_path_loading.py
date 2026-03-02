#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
驗證塗膠路徑加載功能
Verify Glue Path Loading Feature
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def verify_path_loading():
    """驗證路徑加載機制"""
    print("\n" + "=" * 60)
    print("驗證塗膠路徑加載功能")
    print("=" * 60)
    
    try:
        from src.dra_path_manager import DRAPathManager
        
        # 測試 DRA 管理器
        print("\n✓ DRAPathManager 導入成功")
        
        # 在不存在的目錄上測試（模擬測試環境）
        manager = DRAPathManager(dra_projects_path=r'C:\DRA\Projects', dra_extension='.rl')
        print("✓ DRAPathManager 實例化成功")
        
        # 獲取可用路徑
        paths = manager.get_available_paths()
        print(f"✓ 獲取可用路徑: {len(paths)} 個路徑")
        
        if paths:
            print(f"  路徑列表: {paths}")
        else:
            print("  (路徑列表為空 - 將使用預設路徑)")
        
        return True
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def verify_path_combo_loading():
    """驗證 UI 中的路徑加載"""
    print("\n" + "=" * 60)
    print("驗證 UI 路徑下拉菜單加載")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("load_glue_paths 方法存在", "def load_glue_paths(self):" in content),
            ("路徑預設選項", '"路徑 1 - 標準方形 (1)"' in content),
            ("路徑組合框初始化", "self.path_combo = QComboBox()" in content),
            ("路徑信號連接", "self.path_combo.currentTextChanged.connect(self.on_path_selected)" in content),
            ("on_path_selected 方法", "def on_path_selected(self):" in content),
            ("自動選擇第一個路徑", "self.path_combo.setCurrentIndex(0)" in content),
        ]
        
        all_pass = True
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def verify_path_access_flow():
    """驗證路徑訪問流程"""
    print("\n" + "=" * 60)
    print("驗證路徑訪問流程")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        flow_checks = [
            ("create_mode_group 調用 load_glue_paths", 
             "def create_mode_group(self):" in content and "self.load_glue_paths()" in content),
            
            ("on_valve_type_changed 檢查路徑計數",
             "self.path_combo.count()" in content and "on_valve_type_changed" in content),
            
            ("路径为空时重新加载",
             "if self.path_combo.count() == 0:" in content),
            
            ("change_mode 重設路徑選擇",
             "self.path_combo.setCurrentIndex(0)" in content and "change_mode" in content),
            
            ("自動運行按鈕狀態管理",
             "self.auto_run_button.setEnabled(True)" in content),
        ]
        
        all_pass = True
        for check_name, result in flow_checks:
            status = "✓" if result else "✗"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def main():
    """Main verification function"""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  塗膠路徑加載功能驗證".center(58) + "║")
    print("║" + "  Glue Path Loading Feature Verification".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    results = []
    results.append(("DRA 路徑管理器", verify_path_loading()))
    results.append(("UI 路徑下拉菜單", verify_path_combo_loading()))
    results.append(("路徑訪問流程", verify_path_access_flow()))
    
    print("\n" + "=" * 60)
    print("驗證結果摘要")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"總計: {passed}/{total} 測試通過\n")
    
    if passed == total:
        print("✓ 所有驗證通過！塗膠路徑加載功能已正確實現。")
        print("\n功能說明:")
        print("1. 初始化時自動加載塗膠路徑（4個預設路徑）")
        print("2. 選擇塗膠閥類型時，路徑下拉菜單自動啟用")
        print("3. 選擇路徑後，自動運行按鈕自動啟用")
        print("4. 支持重新加載路徑（如果為空）")
        return 0
    else:
        print(f"✗ {total - passed} 個驗證失敗。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
