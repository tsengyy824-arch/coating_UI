#!/usr/bin/env python3
"""
一鍵切換 Modbus 連線模式（實機/模擬器）

用法：
  python switch_modbus_mode.py simulator
  python switch_modbus_mode.py hardware
  python switch_modbus_mode.py hardware --host 192.168.1.103 --port 502 --unit-id 2
"""

import argparse
import configparser
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="切換 Modbus 模式")
    parser.add_argument("mode", choices=["simulator", "hardware"], help="切換目標模式")
    parser.add_argument("--host", help="硬體 IP（僅 hardware 模式有意義）")
    parser.add_argument("--port", type=int, help="端口（僅 hardware 模式有意義）")
    parser.add_argument("--unit-id", type=int, help="Unit ID（僅 hardware 模式有意義）")
    return parser.parse_args()


def main():
    args = parse_args()

    config_path = Path("config/config.ini")
    if not config_path.exists():
        print(f"找不到設定檔: {config_path}")
        raise SystemExit(1)

    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")

    if "MODBUS" not in config:
        config["MODBUS"] = {}

    if args.mode == "simulator":
        config["MODBUS"]["HOST"] = "127.0.0.1"
        config["MODBUS"]["PORT"] = "5020"
        config["MODBUS"]["TIMEOUT"] = "10"
        config["MODBUS"]["RETRIES"] = "3"
        config["MODBUS"]["UNIT_ID"] = "1"
        print("已切換到模擬器模式: 127.0.0.1:5020, UNIT_ID=1")
    else:
        host = args.host or config["MODBUS"].get("HOST", "192.168.1.103")
        port = args.port or int(config["MODBUS"].get("PORT", "502"))
        unit_id = args.unit_id or int(config["MODBUS"].get("UNIT_ID", "2"))

        # 若原本是 simulator 設定，給硬體模式合理預設
        if host == "127.0.0.1":
            host = "192.168.1.103"
        if port == 5020:
            port = 502

        config["MODBUS"]["HOST"] = str(host)
        config["MODBUS"]["PORT"] = str(port)
        config["MODBUS"]["TIMEOUT"] = "10"
        config["MODBUS"]["RETRIES"] = "3"
        config["MODBUS"]["UNIT_ID"] = str(unit_id)
        print(f"已切換到實機模式: {host}:{port}, UNIT_ID={unit_id}")

    with config_path.open("w", encoding="utf-8") as f:
        config.write(f)

    print(f"設定已寫入: {config_path}")


if __name__ == "__main__":
    main()
