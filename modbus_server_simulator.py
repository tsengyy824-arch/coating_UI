"""
Modbus TCP/IP 服务器模拟器
用於測試機械臂控制系統的本地模拟服务器
兼容 pymodbus 3.x
"""

from pymodbus.datastore import ModbusSimulatorContext, ModbusServerContext
from pymodbus.server import StartTcpServer
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_modbus_server():
    """設置 Modbus TCP/IP 服務器"""
    # 配置
    config = {}
    
    # 使用模擬器上下文 (自動初始化所有暫存器)
    simulator = ModbusSimulatorContext(config=config, custom_actions=None)
    
    # 建立伺服器上下文
    context = ModbusServerContext(devices={0x00: simulator}, single=False)
    
    return context


def run_server():
    """運行 Modbus TCP/IP 服務器"""
    logger.info("=" * 50)
    logger.info("機械臂 Modbus TCP/IP 模擬伺服器啟動")
    logger.info("=" * 50)
    logger.info("服務器地址: 127.0.0.1")
    logger.info("服務器端口: 5020")
    logger.info("從機 ID: 1")
    logger.info("")
    logger.info("模擬功能說明:")
    logger.info("- 線圈 (Coils):        地址 0-99 (預設: OFF)")
    logger.info("- 離散輸入:            地址 0-99 (預設: OFF)")
    logger.info("- 保持暫存器:          地址 0-99 (預設: 0)")
    logger.info("- 輸入暫存器:          地址 0-99 (預設: 0)")
    logger.info("")
    logger.info("主程式配置:")
    logger.info("1. 打開 config/config.ini")
    logger.info("2. 將 HOST 改為: 127.0.0.1 或 localhost")
    logger.info("3. 將 PORT 保持為: 502")
    logger.info("4. 保存後運行主程式: python main.py")
    logger.info("")
    logger.info("按 Ctrl+C 停止伺服器")
    logger.info("=" * 50)
    
    # 設置服務器
    context = setup_modbus_server()
    
    # 啟動服務器 (同步版本)
    try:
        StartTcpServer(
            context=context,
            address=("127.0.0.1", 5020),
        )
    except Exception as e:
        logger.error(f"伺服器啟動失敗: {e}")
        if "Permission denied" in str(e) or "Access is denied" in str(e):
            logger.error("錯誤: 無法綁定端口 502")
            logger.error("解決方案:")
            logger.error("  方式1: 以管理員身份運行此程式")
            logger.error("  方式2: 修改 config/config.ini 中的 PORT 為其他端口 (如 5020)")
            logger.error("  方式3: 修改本程式中的端口號")


def main():
    """主程式入口"""
    try:
        # 運行同步伺服器
        run_server()
    except KeyboardInterrupt:
        logger.info("\n伺服器已停止")
    except Exception as e:
        logger.error(f"伺服器出錯: {e}")


if __name__ == '__main__':
    main()
