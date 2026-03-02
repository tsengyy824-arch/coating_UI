# 機械臂控制系統 (Robot Arm Control System)

## 項目描述

這是一個基於 Python 的 Windows UI 應用程序，用於控制達7公斤六軸機械臂搭配 IPC 通過 Modbus TCP/IP 進行通訊。

### 主要功能

1. **機械臂控制**
   - 啟動/停止按鈕
   - 手動/自動模式切換

2. **膠閥控制**
   - 塗膠 (ON) - 打開螺桿膠閥
   - 停膠 (OFF) - 關閉螺桿膠閥
   - IO 控制實現

3. **Modbus TCP/IP 通訊**
   - 連接/斷開 IPC
   - 線圈和寄存器讀寫
   - 錯誤處理和重試機制

## 項目結構

```
robot-arm-control/
├── main.py                 # 主程序入口
├── requirements.txt        # 項目依賴
├── README.md              # 項目說明
├── config/
│   └── config.ini         # 配置文件
└── src/
    ├── ui.py              # PyQt5 UI 界面
    └── modbus_client.py   # Modbus TCP/IP 客戶端
```

## 安裝依賴

```bash
pip install -r requirements.txt
```

### 依賴包列表

- **PyQt5** (>=5.15.0) - Windows UI 框架
- **pymodbus** (>=3.0.0) - Modbus TCP/IP 通訊
- **python-dotenv** (>=0.19.0) - 環境變數管理

## 配置

編輯 `config/config.ini` 文件進行配置：

```ini
[MODBUS]
HOST=192.168.1.100          # IPC IP 地址
PORT=502                    # Modbus 端口
TIMEOUT=10                  # 連接超時時間
RETRIES=3                   # 重試次數

[ROBOT_ARM]
MAX_SPEED=100               # 最大速度
MIN_SPEED=1                 # 最小速度
ACCELERATION=50             # 加速度

[IO_CONTROL]
VALVE_ON_COIL=0             # 打開膠閥的線圈地址
VALVE_OFF_COIL=1            # 關閉膠閥的線圈地址
GLUE_STATE_INPUT=0          # 膠閥狀態輸入地址

[UI]
WINDOW_WIDTH=800            # 窗口寬度
WINDOW_HEIGHT=600           # 窗口高度
WINDOW_TITLE=Robot Arm Control System
```

## 使用方法

### 啟動應用程序

```bash
python main.py
```

### 操作流程

1. **連接 IPC**
   - 點擊 "連接" 按鈕連接到 Modbus 伺服器（自動讀取 config.ini 中的配置）

2. **選擇運行模式**
   - 從下拉菜單選擇 "手動" 或 "自動" 模式

3. **控制機械臂**
   - 點擊 "啟動 (START)" 按鈕開始運行
   - 點擊 "停止 (STOP)" 按鈕停止運行

4. **膠閥控制**
   - 點擊 "塗膠 (ON)" 打開膠閥進行塗膠
   - 點擊 "停膠 (OFF)" 關閉膠閥停止塗膠

5. **斷開連接**
   - 點擊 "斷開" 按鈕斷開 Modbus 連接

## Modbus 通訊規格

### 線圈 (Coils) - 數字輸出

| 地址 | 功能 | 描述 |
|------|------|------|
| 0 | 啟動/停止 | True=啟動, False=停止 |
| 1 | 模式選擇 | True=自動, False=手動 |
| 100 | 塗膠控制 | True=打開, False=關閉 |
| 101 | 停膠控制 | True=打開, False=關閉 |

### 寄存器 (Registers) - 類比輸出

| 地址 | 功能 | 範圍 |
|------|------|------|
| 0 | 速度設置 | 1-100 |
| 1 | 加速度 | 0-255 |

## 故障排除

### 連接失敗
- 檢查 IPC IP 地址是否正確
- 確認网络連接正常
- 驗證 Modbus 端口（默認 502）

### 通訊超時
- 增加 config.ini 中的 TIMEOUT 值
- 檢查網絡延遲
- 驗證 IPC Modbus 伺服器是否正常運行

### UI 無法顯示
- 確保 PyQt5 已正確安裝
- 在 Windows 上運行此應用程序

## 開發日誌

- 2026年2月26日: 初始項目創建
  - 實現基本 UI 框架
  - 集成 Modbus TCP/IP 通訊
  - 添加機械臂和膠閥控制功能

## 許可證

MIT License

## 聯繫方式

如有問題或建議，請聯絡開發者。
