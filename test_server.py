#!/usr/bin/env python3
"""
Quick test for Modbus server startup
"""
import sys
import logging
from pymodbus.datastore import ModbusSimulatorContext, ModbusServerContext
from pymodbus.server import StartTcpServer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Setting up simulator context...")
        simulator = ModbusSimulatorContext(config={}, custom_actions=None)
        logger.info("Simulator context created successfully")
        
        logger.info("Setting up server context...")
        context = ModbusServerContext(devices={0x00: simulator}, single=False)
        logger.info("Server context created successfully")
        
        logger.info("Starting Modbus TCP server on 127.0.0.1:5020...")
        StartTcpServer(context=context, address=("127.0.0.1", 5020))
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
