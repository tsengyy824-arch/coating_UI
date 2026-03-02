"""
機械臂控制系統 - 教導模式對話框
提供分步驟的操作指導
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTextEdit, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class TutorialDialog(QDialog):
    """教導模式對話框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.init_ui()
        self.show_step(0)
    
    def init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("機械臂控制系統 - 操作教導")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        layout = QVBoxLayout()
        
        # 標題
        title_label = QLabel("操作步驟教導")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; padding: 10px;")
        layout.addWidget(title_label)
        
        # 步驟說明區域（可滾動）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        self.step_title = QLabel()
        step_title_font = QFont("Arial", 14, QFont.Bold)
        self.step_title.setFont(step_title_font)
        self.step_title.setStyleSheet("color: #0066cc; padding: 10px; background-color: white; border-radius: 5px;")
        self.content_layout.addWidget(self.step_title)
        
        self.step_content = QTextEdit()
        self.step_content.setReadOnly(True)
        self.step_content.setFont(QFont("Arial", 11))
        self.step_content.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                min-height: 200px;
            }
        """)
        self.content_layout.addWidget(self.step_content)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("上一步")
        self.prev_button.clicked.connect(self.previous_step)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover { background-color: #606060; }
            QPushButton:pressed { background-color: #505050; }
        """)
        
        self.step_label = QLabel()
        self.step_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("color: #333;")
        
        self.next_button = QPushButton("下一步")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover { background-color: #0052a3; }
            QPushButton:pressed { background-color: #004080; }
        """)
        
        close_button = QPushButton("關閉")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover { background-color: #555; }
            QPushButton:pressed { background-color: #444; }
        """)
        
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch()
        button_layout.addWidget(self.step_label)
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_steps(self):
        """定義所有教導步驟"""
        return [
            {
                'title': '步驟 1: 連接到 Modbus 伺服器',
                'content': '''
【準備工作】
✓ 確保機械臂 IPC 已開機
✓ 確保網路連接正常

【操作步驟】
1. 在主視窗中找到「Modbus 連接狀態」區域
2. 點擊「連接」按鈕
3. 等待連接完成，狀態會顯示「已連接」

【預期結果】
✓ 連接狀態標籤變為綠色「已連接」
✓ 「斷開」按鈕變可用
✓ 「啟動手臂」按鈕變可用

【提示】
如果連接失敗，請檢查：
• IPC 地址是否正確（預設 127.0.0.1:5020）
• 網路連接是否正常
• IPC 的 Modbus 服務是否已啟動
                '''
            },
            {
                'title': '步驟 2: 啟動機械臂',
                'content': '''
【前置條件】
✓ 必須已連接到 Modbus（參考步驟 1）

【操作步驟】
1. 在「機械臂控制」區域，點擊「啟動 (START)」按鈕
2. 等待機械臂啟動完成

【預期結果】
✓ 「運行狀態」變為綠色「運行中」
✓ 「停止 (STOP)」按鈕變可用
✓ 「模式選擇」下拉菜單變可用

【重要提醒】
⚠ 啟動前請確保機械臂及其周圍區域安全
⚠ 機械臂啟動時可能會有運動，請保持安全距離
                '''
            },
            {
                'title': '步驟 3: 選擇運行模式',
                'content': '''
【前置條件】
✓ 機械臂必須已啟動（參考步驟 2）

【操作步驟】
在「運行模式」區域中選擇：
  • 【手動】- 手動控制膠閥開關
  • 【自動】- 自動執行預設的塗膠路徑

【選項 A：手動模式】
1. 選擇「手動」模式
2. 轉到步驟 4A（手動塗膠）

【選項 B：自動模式】
1. 選擇「自動」模式
2. 轉到步驟 4B（自動塗膠）

【提示】
✓ 可隨時切換不同模式
✓ 切換模式時系統會自動調整可用控件
                '''
            },
            {
                'title': '步驟 4A: 手動塗膠（I/O 控制）',
                'content': '''
【前置條件】
✓ 模式已設為「手動」（參考步驟 3）

【操作步驟】
在「螺桿膠閥控制 (IO 控制)」區域：

1. 點擊「塗膠 (ON)」按鈕
   → 膠閥開啟，膠液開始流出
   → 狀態會更新為「塗膠中」

2. 根據需要調整時間，監控膠液流量

3. 點擊「停膠 (OFF)」按鈕
   → 膠閥關閉，膠液停止流出
   → 狀態會更新為「停膠」

【重複操作】
✓ 可根據需要多次開關膠閥
✓ 每次操作系統會記錄膠液控制信號

【安全提示】
⚠ 若膠閥無法關閉，應立即停止手臂（參考停止步驟）
⚠ 長時間持續塗膠可能造成膠液浪費
                '''
            },
            {
                'title': '步驟 4B: 自動塗膠流程',
                'content': '''
【前置條件】
✓ 模式已設為「自動」（參考步驟 3）

【第 1 小步：選擇塗膠膠種】
1. 在「塗膠閥類型」下拉菜單中選擇：
   • 圍壩膠塗膠
   • 熱固三防滴膠
2. 確認選擇後，「塗膠路徑」菜單會自動啟用

【第 2 小步：選擇塗膠路徑】
1. 在「塗膠路徑」下拉菜單中選擇預設路徑：
   • 路徑 1 - 標準方形
   • 路徑 2 - 圓形封邊
   • 路徑 3 - 複雜軌跡
   • 路徑 4 - 快速模式
2. 確認選擇後，「啟動自動運行塗膠」按鈕會啟用

【第 3 小步：啟動自動塗膠】
1. 點擊「啟動自動運行塗膠」按鈕
2. 系統會自動執行以下操作：
   • 設置選定的膠種
   • 按照選定路徑控制機械臂
   • 根據路徑自動開關膠閥
3. 等待自動塗膠完成
4. 完成後按鈕會重新啟用，可進行下一次操作

【提示】
✓ 路徑數據自線上Modbus寄存器讀取
✓ 確保DRA Studio路徑文件已正確配置
✓ 首次使用建議在測試環境進行
                '''
            },
            {
                'title': '步驟 5: 停止機械臂',
                'content': '''
【何時需要停止】
✓ 完成所有塗膠操作後
✓ 需要切換模式或更換膠種時
✓ 出現異常情況需要緊急停止

【操作步驟】
1. 在「機械臂控制」區域，點擊「停止 (STOP)」按鈕
2. 系統會停止所有控制信號

【停止後的狀態】
✓ 「運行狀態」變為紅色「已停止」
✓ 膠閥自動關閉
✓ 所有模式和選擇控件都會禁用
✓ 「啟動手臂」按鈕重新啟用

【重新啟動】
• 若要繼續操作，點擊「啟動手臂」按鈕重新開始
• 需要重新選擇模式和參數

【安全提示】
⚠ 停止後機械臂可能需要幾秒鐘才能完全停止
⚠ 停止後不要立即重新啟動，等待 2-3 秒
                '''
            },
            {
                'title': '步驟 6: 斷開連接',
                'content': '''
【何時需要斷開】
✓ 完成所有操作後
✓ 關閉應用程式前
✓ 需要切換不同的 IPC 連接

【操作步驟】
1. 確保機械臂已停止（參考步驟 5）
2. 在「Modbus 連接狀態」區域，點擊「斷開」按鈕
3. 等待連接斷開

【斷開後的狀態】
✓ 連接狀態標籤變為紅色「未連接」
✓ 「連接」按鈕重新啟用
✓ 所有控制相關功能都會禁用

【重新連接】
• 若要再次使用，點擊「連接」按鈕重新開始

【提示】
✓ 系統會自動保存最後的配置
✓ 下次連接時可恢復之前的設定
                '''
            },
            {
                'title': '常見問題排除',
                'content': '''
【連接問題】
Q: 無法連接到 IPC？
A: 
  1. 檢查 IPC 地址和埠是否正確
  2. 檢查網路連接是否正常
  3. 檢查 IPC 的 Modbus 服務是否已啟動
  4. 檢查防火牆設定

【啟動問題】
Q: 啟動後機械臂沒有反應？
A:
  1. 檢查 Modbus 連接是否真的已建立
  2. 確認機械臂控制器是否接收到信號
  3. 重新連接並重試

【自動塗膠問題】
Q: 自動運行按鈕無法點擊？
A:
  1. 確認已連接到 Modbus
  2. 確認機械臂已啟動
  3. 確認已選擇膠種
  4. 確認已選擇塗膠路徑
  5. 確認模式設為「自動」

【膠閥控制問題】
Q: I/O 按鈕在手動模式無法點擊？
A:
  1. 確認已連接到 Modbus
  2. 確認機械臂已啟動
  3. 確認模式設為「手動」
  4. 檢查膠閥硬體連接

【性能問題】
Q: 系統響應緩慢？
A:
  1. 檢查網路連接質量
  2. 檢查 IPC 是否過忙
  3. 嘗試重新連接
  4. 重啟應用程式

【需要更多幫助】
• 查看狀態欄的錯誤訊息
• 檢查應用日誌輸出
• 聯絡技術支援
                '''
            }
        ]
    
    def show_step(self, step_index):
        """顯示指定步驟"""
        steps = self.get_steps()
        
        if step_index < 0 or step_index >= len(steps):
            return
        
        self.current_step = step_index
        step = steps[step_index]
        
        self.step_title.setText(step['title'])
        self.step_content.setText(step['content'])
        self.step_label.setText(f"步驟 {step_index + 1} / {len(steps)}")
        
        # 更新按鈕狀態
        self.prev_button.setEnabled(step_index > 0)
        self.next_button.setEnabled(step_index < len(steps) - 1)
        
        # 更新按鈕文字
        if step_index == len(steps) - 1:
            self.next_button.setText("完成")
        else:
            self.next_button.setText("下一步")
    
    def next_step(self):
        """下一步"""
        steps = self.get_steps()
        if self.current_step < len(steps) - 1:
            self.show_step(self.current_step + 1)
        else:
            self.accept()
    
    def previous_step(self):
        """上一步"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
