"""
Modbus TCP/IP 通訊模組
用於與機械臂 IPC 進行 Modbus 通訊
"""

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging
import time
import sys
import os

# 添加專案根目錄到路徑以導入 deltaDRV 配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from deltaDRV_modbus_address_table import (
        ServoControl, SERVO_VALUES, JogFunction, GoFunction,
        RobotStatus, ErrorCode, SpeedControl, JointDegreePosition,
        CartesianPosition, JointVelocity, MOTION_COMMANDS
    )
    USING_DELTARV_TABLE = True
except ImportError:
    USING_DELTARV_TABLE = False
    # 如果找不到表，使用預設值
    class ServoControl:
        J1_J6_SERVO = 0x0010
    class SERVO_VALUES:
        J1_J6_ON = 0x0001
        J1_J6_OFF = 0x0002

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModbusClient:
    """Modbus TCP/IP 客戶端"""
    
    def __init__(self, host, port, timeout=10, retries=3, unit_id=2):
        """
        初始化 Modbus 客戶端
        
        Args:
            host (str): IPC IP 地址
            port (int): Modbus 端口（默認 502）
            timeout (int): 連接超時時間
            retries (int): 重試次數
            unit_id (int): Modbus Slave/Device ID（Delta DRV 常用 2）
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.unit_id = unit_id
        self.client = None
        self.is_connected = False
        self.last_error = ""
    
    def connect(self):
        """連接到 Modbus 伺服器"""
        try:
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )
            result = self.client.connect()
            if result:
                self.is_connected = True
                self.last_error = ""
                logger.info(f"成功連接到 Modbus 伺服器 {self.host}:{self.port} (unit_id={self.unit_id})")
                return True
            else:
                self.last_error = f"無法連接到 Modbus 伺服器 {self.host}:{self.port}"
                logger.error(f"無法連接到 Modbus 伺服器 {self.host}:{self.port}")
                return False
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"連接 Modbus 伺服器時出錯: {e}")
            return False
    
    def disconnect(self):
        """斷開連接"""
        if self.client:
            self.client.close()
            self.is_connected = False
            self.last_error = ""
            logger.info("已斷開 Modbus 連接")
    
    def read_coil(self, address, count=1):
        """
        讀取線圈（數字輸出）
        
        Args:
            address (int): 線圈地址
            count (int): 讀取數量
            
        Returns:
            list: 線圈狀態列表
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                return None
            
            result = self.client.read_coils(address=address, count=count, device_id=self.unit_id)
            if isinstance(result, ModbusException):
                logger.error(f"讀取線圈時出錯: {result}")
                return None
            return result.bits if hasattr(result, 'bits') else None
        except Exception as e:
            logger.error(f"讀取線圈時出現異常: {e}")
            return None
    
    def write_coil(self, address, value):
        """
        寫入線圈（數字輸出）
        
        Args:
            address (int): 線圈地址
            value (bool): 線圈值 (True/False)
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                return False
            
            result = self.client.write_coil(address=address, value=value, device_id=self.unit_id)
            if isinstance(result, ModbusException):
                logger.error(f"寫入線圈時出錯: {result}")
                return False
            logger.info(f"已寫入線圈 {address}: {value}")
            return True
        except Exception as e:
            logger.error(f"寫入線圈時出現異常: {e}")
            return False
    
    def write_do(self, register_address, bit_value):
        """
        寫入 DO (數位輸出) - 使用16位元寄存器的位元控制
        
        Args:
            register_address (int): 寄存器地址 (0-6)
            bit_value (int): 16位元值 (如 0x0001, 0x0100, 0x0000)
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                self.last_error = "未連接到 Modbus 伺服器"
                logger.warning("未連接到 Modbus 伺服器")
                return False
            
            # 先記錄寫入信息
            logger.info(f"準備寫入 DO 寄存器 {register_address} (0x{register_address:04X}): 0x{bit_value:04X} (二進制: {bin(bit_value)})")
            
            result = self.client.write_register(address=register_address, value=bit_value, device_id=self.unit_id)
            
            if result is None:
                self.last_error = f"寫入返回 None: {register_address}"
                logger.error(f"寫入 DO 寄存器返回 None: {register_address}")
                return False
                
            if isinstance(result, ModbusException):
                self.last_error = str(result)
                logger.error(f"寫入 DO 寄存器時出錯: {result}")
                return False
            self.last_error = ""
            logger.info(f"成功寫入 DO 寄存器 {register_address}: 0x{bit_value:04X}")
            return True
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"寫入 DO 寄存器時出現異常: {e}")
            return False
    
    def read_register(self, address, count=1):
        """
        讀取寄存器（類比輸入）
        
        Args:
            address (int): 寄存器地址
            count (int): 讀取數量
            
        Returns:
            list: 寄存器值列表
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                return None
            
            logger.info(f"準備讀取寄存器 {address} (0x{address:04X}), 數量: {count}")
            result = self.client.read_holding_registers(address=address, count=count, device_id=self.unit_id)
            
            # 檢查是否有錯誤
            if result is None:
                logger.warning(f"讀取寄存器返回 None: {address}")
                return None
                
            if isinstance(result, ModbusException):
                logger.error(f"讀取寄存器時出錯: {result}")
                return None
            
            # 提取寄存器值
            registers = result.registers if hasattr(result, 'registers') else None
            if registers:
                logger.info(f"成功讀取寄存器 {address}: {registers}")
            else:
                logger.warning(f"讀取成功但寄存器值為空: {address}")
            return registers
        except Exception as e:
            logger.error(f"讀取寄存器時出現異常: {e}")
            self.last_error = str(e)
            return None
    
    def write_register(self, address, value):
        """
        寫入寄存器（類比輸出）
        
        Args:
            address (int): 寄存器地址
            value (int): 寄存器值
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                self.last_error = "未連接到 Modbus 伺服器"
                return False
            
            logger.info(f"準備寫入寄存器 {address}: {value}")
            result = self.client.write_register(address=address, value=value, device_id=self.unit_id)
            
            if result is None:
                logger.error(f"寫入寄存器返回 None: {address}")
                self.last_error = f"寫入失敗 (None): {address}"
                return False
                
            if isinstance(result, ModbusException):
                logger.error(f"寫入寄存器時出錯: {result}")
                self.last_error = str(result)
                return False
            
            logger.info(f"已成功寫入寄存器 {address}: {value}")
            self.last_error = ""
            return True
        except Exception as e:
            logger.error(f"寫入寄存器時出現異常: {e}")
            self.last_error = str(e)
            return False
    
    def read_multiple_registers(self, start_address, count=10):
        """
        批量讀取多個連續寄存器 (用於監控狀態組)
        
        Args:
            start_address (int): 起始寄存器地址
            count (int): 要讀取的寄存器數量
            
        Returns:
            list: 寄存器值列表或 None
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                return None
            
            result = self.client.read_holding_registers(address=start_address, count=count, device_id=self.unit_id)
            
            if result is None:
                logger.warning(f"批量讀取寄存器返回 None: {start_address}")
                return None
                
            if isinstance(result, ModbusException):
                logger.error(f"批量讀取寄存器時出錯: {result}")
                return None
            
            registers = result.registers if hasattr(result, 'registers') else None
            if registers:
                logger.debug(f"批量讀取寄存器 {start_address}-{start_address+count-1}: {registers}")
            return registers
            
        except Exception as e:
            logger.error(f"批量讀取寄存器時出現異常: {e}")
            return None
    
    def write_multiple_registers(self, start_address, values):
        """
        批量寫入多個連續寄存器
        
        Args:
            start_address (int): 起始寄存器地址
            values (list): 要寫入的值列表
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                logger.warning("未連接到 Modbus 伺服器")
                return False
            
            result = self.client.write_registers(address=start_address, values=values, device_id=self.unit_id)
            
            if result is None:
                logger.error(f"批量寫入寄存器返回 None: {start_address}")
                return False
                
            if isinstance(result, ModbusException):
                logger.error(f"批量寫入寄存器時出錯: {result}")
                return False
            
            logger.info(f"已批量寫入寄存器 {start_address}: {values}")
            return True
            
        except Exception as e:
            logger.error(f"批量寫入寄存器時出現異常: {e}")
            return False

    def servo_on(self):
        """
        啟動機械臂伺服（全軸 Servo ON）
        基於經過測試的 Delta DRV 控制邏輯
        使用硬體對應表中的正確寄存器地址
        
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                self.last_error = "未連接到 Modbus 伺服器"
                logger.warning("未連接到 Modbus 伺服器 - 無法執行 Servo ON")
                return False
            
            # 使用 Delta DRV 硬體對應表中的寄存器和值
            servo_register = ServoControl.J1_J6_SERVO
            servo_on_value = SERVO_VALUES.J1_J6_ON
            
            logger.info(f"執行 Servo ON: 寄存器 0x{servo_register:04X} (D{servo_register}), 值: 0x{servo_on_value:04X} ({servo_on_value})")
            result = self.write_do(servo_register, servo_on_value)
            
            # 延遲 100ms 確保指令被正確執行（基於提供的測試代碼）
            time.sleep(0.1)
            
            if result:
                self.last_error = ""
                logger.info("✅ Servo ON 命令執行成功")
                return True
            else:
                logger.error(f"❌ Servo ON 命令執行失敗: {self.last_error}")
                return False
                
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ Servo ON 命令執行異常: {e}")
            return False

    def servo_off(self):
        """
        停止機械臂伺服（全軸 Servo OFF）
        基於經過測試的 Delta DRV 控制邏輯
        使用硬體對應表中的正確寄存器地址
        
        Returns:
            bool: 是否成功
        """
        try:
            if not self.is_connected:
                self.last_error = "未連接到 Modbus 伺服器"
                logger.warning("未連接到 Modbus 伺服器 - 無法執行 Servo OFF")
                return False
            
            # 使用 Delta DRV 硬體對應表中的寄存器和值
            servo_register = ServoControl.J1_J6_SERVO
            servo_off_value = SERVO_VALUES.J1_J6_OFF
            
            logger.info(f"執行 Servo OFF: 寄存器 0x{servo_register:04X} (D{servo_register}), 值: 0x{servo_off_value:04X} ({servo_off_value})")
            result = self.write_do(servo_register, servo_off_value)
            
            # 延遲 100ms 確保指令被正確執行（基於提供的測試代碼）
            time.sleep(0.1)
            
            if result:
                self.last_error = ""
                logger.info("✅ Servo OFF 命令執行成功")
                return True
            else:
                logger.error(f"❌ Servo OFF 命令執行失敗: {self.last_error}")
                return False
                
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"❌ Servo OFF 命令執行異常: {e}")
            return False

