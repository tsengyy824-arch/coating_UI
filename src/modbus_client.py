"""
Modbus TCP/IP 通訊模組
用於與機械臂 IPC 進行 Modbus 通訊
"""

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModbusClient:
    """Modbus TCP/IP 客戶端"""
    
    def __init__(self, host, port, timeout=10, retries=3):
        """
        初始化 Modbus 客戶端
        
        Args:
            host (str): IPC IP 地址
            port (int): Modbus 端口（默認 502）
            timeout (int): 連接超時時間
            retries (int): 重試次數
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.client = None
        self.is_connected = False
    
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
                logger.info(f"成功連接到 Modbus 伺服器 {self.host}:{self.port}")
                return True
            else:
                logger.error(f"無法連接到 Modbus 伺服器 {self.host}:{self.port}")
                return False
        except Exception as e:
            logger.error(f"連接 Modbus 伺服器時出錯: {e}")
            return False
    
    def disconnect(self):
        """斷開連接"""
        if self.client:
            self.client.close()
            self.is_connected = False
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
            
            result = self.client.read_coils(address, count=count, device_id=1)
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
            
            result = self.client.write_coil(address, value, device_id=1)
            if isinstance(result, ModbusException):
                logger.error(f"寫入線圈時出錯: {result}")
                return False
            logger.info(f"已寫入線圈 {address}: {value}")
            return True
        except Exception as e:
            logger.error(f"寫入線圈時出現異常: {e}")
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
            
            result = self.client.read_holding_registers(address, count=count, device_id=1)
            if isinstance(result, ModbusException):
                logger.error(f"讀取寄存器時出錯: {result}")
                return None
            return result.registers if hasattr(result, 'registers') else None
        except Exception as e:
            logger.error(f"讀取寄存器時出現異常: {e}")
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
                return False
            
            result = self.client.write_register(address, value, device_id=1)
            if isinstance(result, ModbusException):
                logger.error(f"寫入寄存器時出錯: {result}")
                return False
            logger.info(f"已寫入寄存器 {address}: {value}")
            return True
        except Exception as e:
            logger.error(f"寫入寄存器時出現異常: {e}")
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
            
            result = self.client.read_holding_registers(start_address, count=count, device_id=1)
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
            
            result = self.client.write_registers(start_address, values, device_id=1)
            if isinstance(result, ModbusException):
                logger.error(f"批量寫入寄存器時出錯: {result}")
                return False
            
            logger.info(f"已批量寫入寄存器 {start_address}: {values}")
            return True
            
        except Exception as e:
            logger.error(f"批量寫入寄存器時出現異常: {e}")
            return False
