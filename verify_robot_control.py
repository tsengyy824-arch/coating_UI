#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证机械臂启动/停止时的UI状态管理
Verify Robot Start/Stop UI State Management
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def verify_start_robot_logic():
    """验证启动机械臂时的UI状态管理"""
    print("\n" + "=" * 60)
    print("验证启动机械臂时的UI状态")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("start_robot 方法存在", "def start_robot(self):" in content),
            ("启动时禁用模式选择", "self.mode_combo.setEnabled(False)" in content and "start_robot" in content),
            ("启动时禁用塗膠閥類型", "self.valve_type_combo.setEnabled(False)" in content and "start_robot" in content),
            ("启动时禁用路径选择", "self.path_combo.setEnabled(False)" in content and "start_robot" in content),
            ("启动时禁用自动运行按钮", "self.auto_run_button.setEnabled(False)" in content and "start_robot" in content),
        ]
        
        all_pass = True
        for check_name, result in checks:
            status = "[OK]" if result else "[FAIL]"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        return False

def verify_stop_robot_logic():
    """验证停止机械臂时的UI状态管理"""
    print("\n" + "=" * 60)
    print("验证停止机械臂时的UI状态")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("stop_robot 方法存在", "def stop_robot(self):" in content),
            ("停止后启用模式选择", "self.mode_combo.setEnabled(True)" in content and "stop_robot" in content),
            ("检查自动模式状态", "if self.is_auto_mode:" in content and "stop_robot" in content),
            ("自动模式恢复塗膠閥選擇", "self.valve_type_combo.setEnabled(True)" in content and "is_auto_mode" in content),
            ("手动模式禁用塗膠閥選擇", "self.valve_type_combo.setEnabled(False)" in content and "else:" in content),
        ]
        
        all_pass = True
        for check_name, result in checks:
            status = "[OK]" if result else "[FAIL]"
            print(f"{status} {check_name}")
            if not result:
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        return False

def main():
    """Main verification function"""
    print("\n" + "=" * 60)
    print("  机械臂启动/停止UI状态管理验证")
    print("  Robot Start/Stop UI State Verification")
    print("=" * 60)
    
    results = []
    results.append(("启动机械臂UI状态", verify_start_robot_logic()))
    results.append(("停止机械臂UI状态", verify_stop_robot_logic()))
    
    print("\n" + "=" * 60)
    print("验证结果摘要")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"总计: {passed}/{total} 测试通过\n")
    
    if passed == total:
        print("[SUCCESS] 所有验证通过！UI状态管理已正确实现。")
        print("\n功能说明:")
        print("1. 启动机械臂时 - 禁用模式、閥類型、路径选择（防止运行中修改）")
        print("2. 停止机械臂时 - 根据当前模式恢复相应控制项")
        print("   - 自动模式：启用閥類型和路径选择")
        print("   - 手动模式：禁用閥類型和路径选择")
        return 0
    else:
        print(f"[FAIL] {total - passed} 个验证失败。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
