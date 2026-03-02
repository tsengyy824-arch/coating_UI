<style>
h1, h2, h3, h4, h5, h6 { 
  font-size: 22px; 
  font-family: '微軟正黑體', 'Microsoft JhengHei', sans-serif;
  font-weight: bold;
}

p, li, td, th, span, blockquote, code {
  font-size: 16px;
  font-family: '微軟正黑體', 'Microsoft JhengHei', sans-serif;
}

table {
  font-size: 16px;
  font-family: '微軟正黑體', 'Microsoft JhengHei', sans-serif;
}

body {
  font-family: '微軟正黑體', 'Microsoft JhengHei', sans-serif;
}
</style>

# 新增功能說明 - 塗膠路徑選擇與自動運行模式

## 功能概述

在「運行模式」區域新增了以下功能：

### 1. **塗膠路徑下拉選單**
   - 位置：運行模式區域
   - 功能：顯示所有可用的塗膠路徑程式
   - 來源：可從 DRA Studio 專案目錄自動讀取

### 2. **模式選擇（手動/自動）**
   - **手動模式**：隱藏「啟動自動運行塗膠」按鈕
   - **自動模式**：顯示「啟動自動運行塗膠」按鈕

### 3. **啟動自動運行塗膠按鈕**
   - 位置：運行模式區域（僅在自動模式顯示）
   - 功能：在選定塗膠路徑後，點擊啟動自動塗膠程式
   - 前置條件：
     - 已連接到 Modbus 伺服器
     - 已選擇塗膠路徑
     - 模式已切換到「自動」

## 配置說明

### 修改 `config/config.ini` 中的 DRA Studio 設置：

```ini
[DRA_STUDIO]
# DRA Studio 安裝路徑 (放置 .dra 路徑程式的目錄)
DRA_INSTALL_PATH=C:\DRA\Projects

# 塗膠路徑程式副檔名
GLUE_PATH_EXTENSION=.dra

# 自動塗膠控制線圈地址 (Modbus 寫入位置)
AUTO_GLUE_COIL=2
```

## 操作步驟

### 方案 A：手動模式操作
1. 點擊「連接」按鈕連線到 IPC
2. 選擇「模式選擇」為「手動」
3. 使用「啟動/停止」按鈕控制機械臂
4. 使用「塗膠/停膠」按鈕控制膠閥

### 方案 B：自動模式操作
1. 點擊「連接」按鈕連線到 IPC
2. 選擇「模式選擇」為「自動」
   - 此時「啟動自動運行塗膠」按鈕會自動顯示
3. 從「塗膠路徑」下拉選單選擇要執行的路徑程式
4. 點擊「啟動自動運行塗膠」按鈕
5. 機械臂將按照選定的路徑程式自動執行塗膠

## Modbus 信號對應

|gitgit clone https://github.com/tsengyy824-arch/coating_UI.git|
| 自動塗膠 | 2 | True | 線圈 2 寫入 True 啟動自動塗膠 |

## DRA Studio 路徑程式集成

### 若要實際讀取 DRA Studio 路徑程式：

1. **確保 DRA Studio 已安裝**
2. **在 DRA Studio 中建立塗膠路徑程式** (.dra 文件)
3. **將路徑程式放在指定目錄**
   - 預設：`C:\DRA\Projects`
   - 可在 `config.ini` 修改 `DRA_INSTALL_PATH`
4. **應用啟動時會自動
   - 掃描該目錄
   - 讀取所有 .dra 文件
   - 顯示在塗膠路徑下拉選單中

### 如果目錄不存在或無文件
- 系統將使用預設的範例路徑選項
- 可繼續進行測試

## 故障排除

### 塗膠路徑下拉選單為空
- 檢查 `DRA_INSTALL_PATH` 配置是否正確
- 確認該目錄是否存在
- 檢查 .dra 文件副檔名是否正確
- 查看應用日誌 (console 輸出)

### 自動運行按鈕無法點擊
- 確認已連接到 Modbus 伺服器
- 確認模式已切換到「自動」
- 確認已從下拉選單選擇路徑

### 無法啟動自動塗膠
- 檢查 Modbus 連接是否正常
- 確認 IPC 端是否配置了線圈 2 監聽
- 查看狀態欄的錯誤訊息

## 技術細節

### 新增 UI 元素
- `self.path_combo`: 塗膠路徑下拉選單
- `self.auto_run_button`: 自動運行塗膠按鈕

### 新增方法
- `load_glue_paths()`: 讀取塗膠路徑程式
- `start_auto_glue()`: 啟動自動塗膠

### 修改方法
- `change_mode()`: 添加自動按鈕顯示/隱藏邏輯

