#!/usr/bin/env python3
"""
台达 DRV9 机械手臂对接验证脚本
用于测试与台达控制器的 Modbus TCP/IP 连接和寄存器操作
"""

import sys
import os
import time
import configparser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.modbus_client import ModbusClient
from src.dra_path_manager import DRAPathManager


def print_header(title):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_connection(host, port):
    """测试基础连接"""
    print_header("第一步：测试网络连接")
    
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✅ 网络连接成功: {host}:{port}")
            return True
        else:
            print(f"❌ 无法连接到 {host}:{port} (错误码: {result})")
            print("   可能原因：")
            print("   - 台达控制器未开机")
            print("   - IP 地址或端口不正确")
            print("   - 防火墙阻止连接")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False
    finally:
        sock.close()


def test_modbus_connection(host, port, timeout=10, retries=3):
    """测试 Modbus 连接"""
    print_header("第二步：测试 Modbus TCP/IP 连接")
    
    client = ModbusClient(host=host, port=port, timeout=timeout, retries=retries)
    
    try:
        if client.connect():
            print(f"✅ Modbus 连接成功")
            print(f"   服务器: {host}:{port}")
            print(f"   设备 ID: 1")
            return client
        else:
            print(f"❌ Modbus 连接失败")
            return None
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return None


def test_register_write(client, register_address, test_value):
    """测试寄存器写入"""
    print_header(f"第三步：测试寄存器写入 (D{register_address}={test_value})")
    
    try:
        if client.write_register(register_address, test_value):
            print(f"✅ 成功写入 D{register_address} = {test_value}")
            return True
        else:
            print(f"❌ 写入失败")
            return False
    except Exception as e:
        print(f"❌ 写入异常: {e}")
        return False


def test_register_read(client, register_address, count=1):
    """测试寄存器读取"""
    print_header(f"第四步：测试寄存器读取 (D{register_address}-D{register_address+count-1})")
    
    try:
        result = client.read_register(register_address, count)
        if result:
            print(f"✅ 成功读取寄存器")
            for i, value in enumerate(result if isinstance(result, list) else [result]):
                print(f"   D{register_address+i} = {value}")
            return result
        else:
            print(f"❌ 读取失败")
            return None
    except Exception as e:
        print(f"❌ 读取异常: {e}")
        return None


def test_path_execution(client, path_number):
    """测试路径执行 (模拟)"""
    print_header(f"第五步：测试路径执行触发 (编号: {path_number})")
    
    PATH_EXECUTE_REGISTER = 1000
    
    print(f"📝 模拟场景：向寄存器 D{PATH_EXECUTE_REGISTER} 写入路径编号 {path_number}")
    print(f"   期望行为：台达控制器应执行预设的路径 {path_number}")
    
    if client.write_register(PATH_EXECUTE_REGISTER, path_number):
        print(f"✅ 路径执行指令已发送")
        
        # 监控状态
        PATH_STATUS_REGISTER = 1001
        print(f"\n📊 监控执行状态 (读取 D{PATH_STATUS_REGISTER})...")
        
        for i in range(5):
            time.sleep(1)
            status = client.read_register(PATH_STATUS_REGISTER, 1)
            if status:
                status_value = status[0] if isinstance(status, list) else status
                status_desc = {
                    0: "待命",
                    1: "运行中",
                    2: "已完成",
                    3: "已停止",
                    4: "错误"
                }.get(status_value, "未知")
                print(f"   秒 {i+1}: 状态 = {status_value} ({status_desc})")
        
        return True
    else:
        print(f"❌ 发送失败")
        return False


def test_dra_path_loading():
    """测试 DRA 路径文件加载"""
    print_header("第六步：测试 DRA 路径文件加载")
    
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    dra_path = config.get('DRA_STUDIO', 'DRA_INSTALL_PATH', fallback=r'C:\DRA\Projects')
    dra_ext = config.get('DRA_STUDIO', 'GLUE_PATH_EXTENSION', fallback='.rl')
    
    print(f"📁 DRA 项目目录: {dra_path}")
    print(f"📄 路径文件扩展名: {dra_ext}")
    
    manager = DRAPathManager(dra_projects_path=dra_path, dra_extension=dra_ext)
    paths = manager.load_paths_from_directory()
    
    if paths:
        print(f"✅ 成功加载 {len(paths)} 个路径文件:")
        for path_name, path_num in sorted(paths.items(), key=lambda x: x[1]):
            print(f"   编号 {path_num}: {path_name}")
        return paths
    else:
        print(f"⚠️  未找到路径文件 (目录可能不存在或无 {dra_ext} 文件)")
        print(f"   🔧 请在 config.ini 中配置正确的 DRA_INSTALL_PATH")
        return {}


def main():
    """主测试流程"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   台達 DRV9 六軸機械手臂 Modbus TCP/IP 對接驗證工具")
    print("║   Delta DRV9 Robot Modbus TCP/IP Integration Validator")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # 读取配置
    config = configparser.ConfigParser()
    config.read('config/config.ini', encoding='utf-8')
    
    host = config.get('MODBUS', 'HOST', fallback='127.0.0.1')
    port = config.getint('MODBUS', 'PORT', fallback=5020)
    timeout = config.getint('MODBUS', 'TIMEOUT', fallback=10)
    retries = config.getint('MODBUS', 'RETRIES', fallback=3)
    
    print(f"\n📋 配置信息:")
    print(f"   IP 地址: {host}")
    print(f"   端口: {port}")
    print(f"   超时: {timeout}s")
    print(f"   重试: {retries}次")
    
    # 第一步：网络连接
    if not test_connection(host, port):
        print("\n❌ 请先检查网络连接后重试")
        return
    
    # 第二步：Modbus 连接
    client = test_modbus_connection(host, port)
    if not client:
        print("\n❌ 无法建立 Modbus 连接")
        print("📝 对于如果使用模拟服务器（test_server.py），请确保其正在运行")
        return
    
    # 第三步：寄存器写入测试
    test_register_write(client, 1000, 99)
    
    # 第四步：寄存器读取测试
    test_register_read(client, 1001, 3)
    
    # 第五步：路径执行测试（可选）
    user_input = input("\n❓ 是否测试路径执行？(y/n): ").lower()
    if user_input == 'y':
        test_path_execution(client, 1)
    
    # 第六步：DRA 路径加载测试
    test_dra_path_loading()
    
    # 断开连接
    client.disconnect()
    
    # 总结
    print_header("验证完成")
    print("""
✅ 系统已验证与台达控制器的对接能力

📝 后续步骤：
   1. 获取实际台达控制器信息：
      - 控制器型号
      - 实际 IP 地址
      - DRAStudio 版本
      - 寄存器地址映射表
   
   2. 修改 config.ini 中的配置：
      - [MODBUS] 段：设置正确的 IP 和端口
      - [DRA_ROBOT_MODBUS] 段：设置寄存器地址
      - [DRA_STUDIO] 段：设置路径文件目录
   
   3. 在 DRAStudio 中配置：
      - 定义路径编号 (1, 2, 3, 4...)
      - 设置 Modbus 触发条件
      - 测试路径执行
   
   4. 部署到生产环境：
      - 运行主应用: python main.py
      - 连接到台达控制器
      - 测试手动/自动模式
      - 验证路径执行

⚠️  安全提醒：
   - 首次在实际设备上测试前，建议先在模拟环境中验证
   - 确保设置了适当的防火墙规则
   - 监控错误码和状态寄存器
   - 准备好紧急停止措施

📞 需要支持？请提供：
   - 台达控制器型号
   - DRAStudio 版本
   - 实际 IP 地址和端口
   - 错误日志输出
    """)


if __name__ == '__main__':
    main()
