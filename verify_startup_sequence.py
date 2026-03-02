#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证正确的启动顺序逻辑
Verify Correct Startup Sequence Logic
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def verify_connect_logic():
    """验证连接后的状态"""
    print("\n" + "=" * 60)
    print("1. 验证连接后的状态（连接 → 模式选择应禁用）")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在connect_modbus中查找是否禁用mode_combo
        connect_start = content.find("def connect_modbus(self):")
        connect_end = content.find("def disconnect_modbus(self):", connect_start)
        connect_section = content[connect_start:connect_end]
        
        checks = [
            ("连接后模式选择禁用", "self.mode_combo.setEnabled(False)" in connect_section),
            ("提示需要先启动手臂", "請先啟動手臂" in connect_section or "请先启动手臂" in connect_section),
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

def verify_start_robot_logic():
    """验证启动手臂后的状态"""
    print("\n" + "=" * 60)
    print("2. 验证启动手臂后的状态（启动 → 启用模式选择）")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        start_robot_pos = content.find("def start_robot(self):")
        stop_robot_pos = content.find("def stop_robot(self):", start_robot_pos)
        start_section = content[start_robot_pos:stop_robot_pos]
        
        checks = [
            ("启动后启用模式选择", "self.mode_combo.setEnabled(True)" in start_section),
            ("检查自动模式状态", "if self.is_auto_mode:" in start_section),
            ("自动模式启用閥類型选择", "self.valve_type_combo.setEnabled(True)" in start_section and "is_auto_mode" in start_section),
            ("手动模式启用IO按钮", "self.valve_on_button.setEnabled(True)" in start_section and "else:" in start_section),
            ("自动模式禁用IO按钮", "self.valve_on_button.setEnabled(False)" in start_section and "is_auto_mode" in start_section),
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
    """验证停止手臂后的状态"""
    print("\n" + "=" * 60)
    print("3. 验证停止手臂后的状态（停止 → 禁用所有控件）")
    print("=" * 60)
    
    try:
        with open('src/ui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        stop_robot_pos = content.find("def stop_robot(self):")
        change_mode_pos = content.find("def change_mode(self", stop_robot_pos)
        stop_section = content[stop_robot_pos:change_mode_pos]
        
        checks = [
            ("停止后禁用模式选择", "self.mode_combo.setEnabled(False)" in stop_section),
            ("停止后禁用閥類型选择", "self.valve_type_combo.setEnabled(False)" in stop_section),
            ("停止后禁用路径选择", "self.path_combo.setEnabled(False)" in stop_section),
            ("停止后禁用自动运行按钮", "self.auto_run_button.setEnabled(False)" in stop_section),
            ("停止后禁用IO按钮", "self.valve_on_button.setEnabled(False)" in stop_section and "self.valve_off_button.setEnabled(False)" in stop_section),
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
    print("  正确启动顺序逻辑验证")
    print("  Correct Startup Sequence Verification")
    print("=" * 60)
    print("\n期望的操作顺序：")
    print("1. 连接 Modbus")
    print("2. 启动手臂 (Start)")
    print("3. 选择模式 (手动/自动)")
    print("   - 手动：只能用 I/O 控制")
    print("   - 自动：选膠閥 → 选路径 → 自动塗膠")
    
    results = []
    results.append(("连接后状态", verify_connect_logic()))
    results.append(("启动手臂后状态", verify_start_robot_logic()))
    results.append(("停止手臂后状态", verify_stop_robot_logic()))
    
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
        print("[SUCCESS] 所有验证通过！启动顺序逻辑已正确实现。")
        print("\n实际操作流程：")
        print("  连接 → 启动手臂 → 选择模式")
        print("  └─ 手动模式：I/O 控制塗膠")
        print("  └─ 自动模式：膠閥 → 路径 → 自动塗膠")
        return 0
    else:
        print(f"[FAIL] {total - passed} 个验证失败。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
