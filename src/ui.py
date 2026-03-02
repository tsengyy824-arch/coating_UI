"""
機械臂控制系統 UI
使用 PyQt5 構建 Windows UI 介面
"""

import sys
import configparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox,
    QStatusBar, QMessageBox, QLCDNumber
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from src.modbus_client import ModbusClient
from src.dra_path_manager import DRAPathManager
from src.tutorial_dialog import TutorialDialog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobotControlUI(QMainWindow):
    """機械臂控制 UI 主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini', encoding='utf-8')
        
        # 初始化 Modbus 客戶端
        self.modbus = ModbusClient(
            host=self.config.get('MODBUS', 'HOST'),
            port=self.config.getint('MODBUS', 'PORT'),
            timeout=self.config.getint('MODBUS', 'TIMEOUT'),
            retries=self.config.getint('MODBUS', 'RETRIES')
        )
        
        # 初始化 DRA 路徑管理器
        dra_path = self.config.get('DRA_STUDIO', 'DRA_INSTALL_PATH', fallback=r'C:\DRA\Projects')
        dra_ext = self.config.get('DRA_STUDIO', 'GLUE_PATH_EXTENSION', fallback='.rl')
        self.dra_manager = DRAPathManager(dra_projects_path=dra_path, dra_extension=dra_ext)
        
        # 狀態變數
        self.is_running = False
        self.is_auto_mode = False
        self.glue_valve_on = False
        
        # 初始化 UI
        self.init_ui()
        
        # 設置定時器用於讀取狀態
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(500)  # 每 500ms 更新一次
    
    def init_ui(self):
        """初始化 UI 元件"""
        self.setWindowTitle(self.config.get('UI', 'WINDOW_TITLE'))
        self.setGeometry(100, 100,
                        self.config.getint('UI', 'WINDOW_WIDTH'),
                        self.config.getint('UI', 'WINDOW_HEIGHT'))
        
        # 創建中央 Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 創建主佈局
        main_layout = QVBoxLayout()
        
        # 連接狀態區域
        connection_group = self.create_connection_group()
        main_layout.addWidget(connection_group)
        
        # 控制區域
        control_group = self.create_control_group()
        main_layout.addWidget(control_group)
        
        # 模式選擇區域
        mode_group = self.create_mode_group()
        main_layout.addWidget(mode_group)
        
        # 膠閥控制區域
        valve_group = self.create_valve_group()
        main_layout.addWidget(valve_group)
        
        # 狀態顯示區域
        status_group = self.create_status_group()
        main_layout.addWidget(status_group)
        
        central_widget.setLayout(main_layout)
        
        # 設置狀態欄
        self.statusBar().showMessage("就緒")
    
    def create_connection_group(self):
        """創建連接狀態組"""
        group = QGroupBox("Modbus 連接狀態")
        layout = QHBoxLayout()
        
        # 從配置讀取字體大小
        button_font_size = self.config.getint('UI', 'BUTTON_FONT_SIZE')
        
        status_label = QLabel("狀態:")
        status_label.setFont(QFont("Arial", button_font_size))
        
        self.connection_label = QLabel("未連接")
        self.connection_label.setFont(QFont("Arial", button_font_size, QFont.Bold))
        self.connection_label.setStyleSheet("color: red;")
        
        self.connect_button = QPushButton("連接")
        self.connect_button.clicked.connect(self.connect_modbus)
        self.connect_button.setStyleSheet(f"background-color: lightblue; padding: 15px; font-size: {button_font_size}px; min-height: 40px; min-width: 80px;")
        
        self.disconnect_button = QPushButton("斷開")
        self.disconnect_button.clicked.connect(self.disconnect_modbus)
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.setStyleSheet(f"background-color: lightcoral; padding: 15px; font-size: {button_font_size}px; min-height: 40px; min-width: 80px;")
        
        tutorial_button = QPushButton("使用步驟")
        tutorial_button.clicked.connect(self.show_tutorial)
        tutorial_button.setStyleSheet(f"background-color: #ff9900; padding: 15px; font-size: {button_font_size}px; min-height: 40px; min-width: 100px; color: white; font-weight: bold;")
        
        layout.addWidget(status_label)
        layout.addWidget(self.connection_label)
        layout.addStretch()
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(tutorial_button)
        
        group.setLayout(layout)
        return group
    
    def create_control_group(self):
        """創建控制組（開始/停止）"""
        group = QGroupBox("機械臂控制")
        layout = QHBoxLayout()
        
        # 從配置讀取字體大小
        button_font_size = self.config.getint('UI', 'CONTROL_BUTTON_FONT_SIZE')
        
        self.start_button = QPushButton("啟動 (START)")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_robot)
        self.start_button.setStyleSheet(f"background-color: lightgreen; padding: 20px; font-size: {button_font_size}px; font-weight: bold; min-height: 50px; min-width: 120px;")
        
        self.stop_button = QPushButton("停止 (STOP)")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_robot)
        self.stop_button.setStyleSheet(f"background-color: lightcoral; padding: 20px; font-size: {button_font_size}px; font-weight: bold; min-height: 50px; min-width: 120px;")
        
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        
        group.setLayout(layout)
        return group
    
    def create_mode_group(self):
        """創建模式選擇組（手動/自動 + 塗膠閥類型 + 塗膠路徑）"""
        group = QGroupBox("運行模式")
        layout = QVBoxLayout()
        
        # 從配置讀取字體大小
        button_font_size = self.config.getint('UI', 'BUTTON_FONT_SIZE')
        
        # 第一行：模式選擇
        mode_layout = QHBoxLayout()
        mode_label = QLabel("模式選擇:")
        mode_label.setFont(QFont("Arial", button_font_size))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("手動")
        self.mode_combo.addItem("自動")
        self.mode_combo.currentTextChanged.connect(self.change_mode)
        self.mode_combo.setEnabled(False)
        self.mode_combo.setStyleSheet(f"padding: 8px; font-size: {button_font_size}px;")
        
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        
        # 第二行：塗膠閥類型選擇
        valve_layout = QHBoxLayout()
        valve_label = QLabel("塗膠閥類型:")
        valve_label.setFont(QFont("Arial", button_font_size))
        
        self.valve_type_combo = QComboBox()
        self.valve_type_combo.addItem("圍壩膠塗膠", "valve_1")
        self.valve_type_combo.addItem("熱固三防滴膠", "valve_2")
        self.valve_type_combo.setEnabled(False)
        self.valve_type_combo.setStyleSheet(f"padding: 8px; font-size: {button_font_size}px;")
        self.valve_type_combo.currentTextChanged.connect(self.on_valve_type_changed)
        
        valve_layout.addWidget(valve_label)
        valve_layout.addWidget(self.valve_type_combo)
        valve_layout.addStretch()
        
        # 第三行：塗膠路徑選擇
        path_layout = QHBoxLayout()
        path_label = QLabel("塗膠路徑:")
        path_label.setFont(QFont("Arial", button_font_size))
        
        self.path_combo = QComboBox()
        self.path_combo.setEnabled(False)
        self.path_combo.setStyleSheet(f"padding: 8px; font-size: {button_font_size}px;")
        # 加載塗膠路徑選項
        self.load_glue_paths()
        # 監聽路徑選擇變化
        self.path_combo.currentTextChanged.connect(self.on_path_selected)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_combo)
        path_layout.addStretch()
        
        # 第四行：自動運行按鈕（初始隱藏）
        auto_button_layout = QHBoxLayout()
        self.auto_run_button = QPushButton("啟動自動運行塗膠")
        self.auto_run_button.setEnabled(False)
        self.auto_run_button.clicked.connect(self.start_auto_glue)
        button_font_size = self.config.getint('UI', 'BUTTON_FONT_SIZE')
        self.auto_run_button.setStyleSheet(f"background-color: lightblue; padding: 15px; font-size: {button_font_size}px; min-height: 40px; min-width: 150px; font-weight: bold;")
        self.auto_run_button.setVisible(False)  # 初始隱藏
        
        auto_button_layout.addWidget(self.auto_run_button)
        auto_button_layout.addStretch()
        
        layout.addLayout(mode_layout)
        layout.addLayout(valve_layout)
        layout.addLayout(path_layout)
        layout.addLayout(auto_button_layout)
        
        group.setLayout(layout)
        return group
    
    def create_valve_group(self):
        """創建膠閥控制組"""
        group = QGroupBox("手動IO控制")
        layout = QVBoxLayout()
        
        # 從配置讀取字體大小
        button_font_size = self.config.getint('UI', 'BUTTON_FONT_SIZE')
        
        # 第一組膠閥：塗膠（圍壩膠）
        valve_1_layout = QHBoxLayout()
        
        valve_1_label = QLabel("塗膠閥 (圍壩膠):")
        valve_1_label.setFont(QFont("Arial", button_font_size))
        
        self.valve_on_button = QPushButton("開啟 (ON)")
        self.valve_on_button.setEnabled(False)
        self.valve_on_button.clicked.connect(self.valve_on)
        self.valve_on_button.setStyleSheet(f"background-color: lightyellow; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.valve_off_button = QPushButton("關閉 (OFF)")
        self.valve_off_button.setEnabled(False)
        self.valve_off_button.clicked.connect(self.valve_off)
        self.valve_off_button.setStyleSheet(f"background-color: lightgray; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.valve_status_label = QLabel("狀態: 關閉")
        self.valve_status_label.setFont(QFont("Arial", button_font_size))
        self.valve_status_label.setStyleSheet("color: blue;")
        
        valve_1_layout.addWidget(valve_1_label)
        valve_1_layout.addWidget(self.valve_on_button)
        valve_1_layout.addWidget(self.valve_off_button)
        valve_1_layout.addStretch()
        valve_1_layout.addWidget(self.valve_status_label)
        
        # 第一組氣缸：圍壩膠伸縮汽缸
        cylinder_1_layout = QHBoxLayout()
        
        cylinder_1_label = QLabel("  └ 伸縮汽缸:")
        cylinder_1_label.setFont(QFont("Arial", button_font_size))
        
        self.cylinder_1_extend_button = QPushButton("伸出")
        self.cylinder_1_extend_button.setEnabled(False)
        self.cylinder_1_extend_button.clicked.connect(self.cylinder_1_extend)
        self.cylinder_1_extend_button.setStyleSheet(f"background-color: lightgreen; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.cylinder_1_retract_button = QPushButton("收回")
        self.cylinder_1_retract_button.setEnabled(False)
        self.cylinder_1_retract_button.clicked.connect(self.cylinder_1_retract)
        self.cylinder_1_retract_button.setStyleSheet(f"background-color: lightcoral; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.cylinder_1_status_label = QLabel("狀態: 未知")
        self.cylinder_1_status_label.setFont(QFont("Arial", button_font_size))
        self.cylinder_1_status_label.setStyleSheet("color: gray;")
        
        cylinder_1_layout.addWidget(cylinder_1_label)
        cylinder_1_layout.addWidget(self.cylinder_1_extend_button)
        cylinder_1_layout.addWidget(self.cylinder_1_retract_button)
        cylinder_1_layout.addStretch()
        cylinder_1_layout.addWidget(self.cylinder_1_status_label)
        
        # 第二組膠閥：熱固化三防滴膠閥
        valve_2_layout = QHBoxLayout()
        
        valve_2_label = QLabel("熱固化三防滴膠閥:")
        valve_2_label.setFont(QFont("Arial", button_font_size))
        
        self.valve_2_on_button = QPushButton("開啟 (ON)")
        self.valve_2_on_button.setEnabled(False)
        self.valve_2_on_button.clicked.connect(self.valve_2_on)
        self.valve_2_on_button.setStyleSheet(f"background-color: lightcyan; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.valve_2_off_button = QPushButton("關閉 (OFF)")
        self.valve_2_off_button.setEnabled(False)
        self.valve_2_off_button.clicked.connect(self.valve_2_off)
        self.valve_2_off_button.setStyleSheet(f"background-color: lightgray; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.valve_2_status_label = QLabel("狀態: 關閉")
        self.valve_2_status_label.setFont(QFont("Arial", button_font_size))
        self.valve_2_status_label.setStyleSheet("color: blue;")
        
        valve_2_layout.addWidget(valve_2_label)
        valve_2_layout.addWidget(self.valve_2_on_button)
        valve_2_layout.addWidget(self.valve_2_off_button)
        valve_2_layout.addStretch()
        valve_2_layout.addWidget(self.valve_2_status_label)
        
        # 第二組氣缸：熱固化三防膠伸縮汽缸
        cylinder_2_layout = QHBoxLayout()
        
        cylinder_2_label = QLabel("  └ 伸縮汽缸:")
        cylinder_2_label.setFont(QFont("Arial", button_font_size))
        
        self.cylinder_2_extend_button = QPushButton("伸出")
        self.cylinder_2_extend_button.setEnabled(False)
        self.cylinder_2_extend_button.clicked.connect(self.cylinder_2_extend)
        self.cylinder_2_extend_button.setStyleSheet(f"background-color: lightgreen; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.cylinder_2_retract_button = QPushButton("收回")
        self.cylinder_2_retract_button.setEnabled(False)
        self.cylinder_2_retract_button.clicked.connect(self.cylinder_2_retract)
        self.cylinder_2_retract_button.setStyleSheet(f"background-color: lightcoral; padding: 15px; font-size: {button_font_size}px; min-height: 45px; min-width: 120px;")
        
        self.cylinder_2_status_label = QLabel("狀態: 未知")
        self.cylinder_2_status_label.setFont(QFont("Arial", button_font_size))
        self.cylinder_2_status_label.setStyleSheet("color: gray;")
        
        cylinder_2_layout.addWidget(cylinder_2_label)
        cylinder_2_layout.addWidget(self.cylinder_2_extend_button)
        cylinder_2_layout.addWidget(self.cylinder_2_retract_button)
        cylinder_2_layout.addStretch()
        cylinder_2_layout.addWidget(self.cylinder_2_status_label)
        
        layout.addLayout(valve_1_layout)
        layout.addLayout(cylinder_1_layout)
        layout.addLayout(valve_2_layout)
        layout.addLayout(cylinder_2_layout)
        
        group.setLayout(layout)
        return group
    
    def create_status_group(self):
        """創建狀態顯示組"""
        group = QGroupBox("系統狀態")
        layout = QVBoxLayout()
        
        # 從配置讀取字體大小
        status_font_size = self.config.getint('UI', 'STATUS_LABEL_FONT_SIZE')
        
        # 運行狀態顯示
        run_status_layout = QHBoxLayout()
        run_status_title = QLabel("運行狀態:")
        run_status_title.setFont(QFont("Arial", status_font_size))
        run_status_layout.addWidget(run_status_title)
        self.run_status_label = QLabel("已停止")
        self.run_status_label.setFont(QFont("Arial", status_font_size, QFont.Bold))
        self.run_status_label.setStyleSheet("color: red;")
        run_status_layout.addWidget(self.run_status_label)
        run_status_layout.addStretch()
        
        # 當前模式顯示
        mode_status_layout = QHBoxLayout()
        mode_status_title = QLabel("當前模式:")
        mode_status_title.setFont(QFont("Arial", status_font_size))
        mode_status_layout.addWidget(mode_status_title)
        self.current_mode_label = QLabel("手動")
        self.current_mode_label.setFont(QFont("Arial", status_font_size, QFont.Bold))
        self.current_mode_label.setStyleSheet("color: blue;")
        mode_status_layout.addWidget(self.current_mode_label)
        mode_status_layout.addStretch()
        
        layout.addLayout(run_status_layout)
        layout.addLayout(mode_status_layout)
        
        group.setLayout(layout)
        return group
    
    def connect_modbus(self):
        """連接 Modbus 伺服器"""
        if self.modbus.connect():
            self.connection_label.setText("已連接")
            self.connection_label.setStyleSheet("color: green;")
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            # 連接後不啟用模式選擇，需要先啟動手臂
            self.mode_combo.setEnabled(False)
            self.statusBar().showMessage("已成功連接到 Modbus 伺服器 - 請先啟動手臂")
        else:
            QMessageBox.critical(self, "連接失敗", "無法連接到 Modbus 伺服器")
            self.statusBar().showMessage("連接失敗")
    
    def disconnect_modbus(self):
        """斷開 Modbus 連接"""
        self.modbus.disconnect()
        self.connection_label.setText("未連接")
        self.connection_label.setStyleSheet("color: red;")
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.mode_combo.setEnabled(False)
        self.valve_on_button.setEnabled(False)
        self.valve_off_button.setEnabled(False)
        self.valve_2_on_button.setEnabled(False)
        self.valve_2_off_button.setEnabled(False)
        self.cylinder_1_extend_button.setEnabled(False)
        self.cylinder_1_retract_button.setEnabled(False)
        self.cylinder_2_extend_button.setEnabled(False)
        self.cylinder_2_retract_button.setEnabled(False)
        self.statusBar().showMessage("已斷開 Modbus 連接")
    
    def show_tutorial(self):
        """顯示操作教導對話框"""
        tutorial = TutorialDialog(self)
        tutorial.exec_()
    
    def start_robot(self):
        """啟動機械臂"""
        if self.modbus.write_coil(0, True):  # 寫入啟動信號到線圈 0
            self.is_running = True
            self.run_status_label.setText("運行中")
            self.run_status_label.setStyleSheet("color: green;")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            # 啟動後啟用模式選擇
            self.mode_combo.setEnabled(True)
            # 根據當前模式設置其他控件狀態
            if self.is_auto_mode:
                # 自動模式：啟用塗膠閥和路徑選擇
                self.valve_type_combo.setEnabled(True)
                self.path_combo.setEnabled(True)
                if self.path_combo.currentIndex() >= 0:
                    self.auto_run_button.setEnabled(True)
                # 禁用手動IO控制
                self.valve_on_button.setEnabled(False)
                self.valve_off_button.setEnabled(False)
            else:
                # 手動模式：啟用手動IO控制
                self.valve_on_button.setEnabled(True)
                self.valve_off_button.setEnabled(True)
                self.valve_2_on_button.setEnabled(True)
                self.valve_2_off_button.setEnabled(True)
                self.cylinder_1_extend_button.setEnabled(True)
                self.cylinder_1_retract_button.setEnabled(True)
                self.cylinder_2_extend_button.setEnabled(True)
                self.cylinder_2_retract_button.setEnabled(True)
                # 禁用自動相關控制
                self.valve_type_combo.setEnabled(False)
                self.path_combo.setEnabled(False)
                self.auto_run_button.setEnabled(False)
            self.statusBar().showMessage("機械臂已啟動 - 請選擇運行模式")
        else:
            QMessageBox.warning(self, "控制失敗", "無法啟動機械臂")
    
    def stop_robot(self):
        """停止機械臂"""
        if self.modbus.write_coil(0, False):  # 寫入停止信號到線圈 0
            self.is_running = False
            self.run_status_label.setText("已停止")
            self.run_status_label.setStyleSheet("color: red;")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            # 停止後禁用模式選擇和所有相關控制項
            self.mode_combo.setEnabled(False)
            self.valve_type_combo.setEnabled(False)
            self.path_combo.setEnabled(False)
            self.auto_run_button.setEnabled(False)
            self.valve_on_button.setEnabled(False)
            self.valve_off_button.setEnabled(False)
            self.valve_2_on_button.setEnabled(False)
            self.valve_2_off_button.setEnabled(False)
            self.cylinder_1_extend_button.setEnabled(False)
            self.cylinder_1_retract_button.setEnabled(False)
            self.cylinder_2_extend_button.setEnabled(False)
            self.cylinder_2_retract_button.setEnabled(False)
            self.statusBar().showMessage("機械臂已停止 - 請重新啟動手臂")
        else:
            QMessageBox.warning(self, "控制失敗", "無法停止機械臂")
    
    def change_mode(self, mode):
        """改變運行模式"""
        if mode == "自動":
            self.is_auto_mode = True
            # 寫入自動模式信號到線圈 1
            self.modbus.write_coil(1, True)
            self.current_mode_label.setText("自動")
            self.current_mode_label.setStyleSheet("color: green;")
            self.statusBar().showMessage("切換到自動模式")
            # 啟用塗膠閥類型選擇
            self.valve_type_combo.setEnabled(True)
            # 強制觸發信號以啟用路徑選擇（即使已經在索引0）
            current_index = self.valve_type_combo.currentIndex()
            if current_index >= 0:
                # 如果已經有選項，手動調用 on_valve_type_changed() 來啟用路徑
                self.on_valve_type_changed()
            else:
                # 如果沒有選項，設置為第一個
                self.valve_type_combo.setCurrentIndex(0)
            # 顯示自動運行按鈕
            self.auto_run_button.setVisible(True)
            self.auto_run_button.setEnabled(False)  # 先禁用，直到選擇了路徑
            # 禁用手動IO控制按鈕（自動模式不允許手動塗膠）
            self.valve_on_button.setEnabled(False)
            self.valve_off_button.setEnabled(False)
            self.valve_2_on_button.setEnabled(False)
            self.valve_2_off_button.setEnabled(False)
            self.cylinder_1_extend_button.setEnabled(False)
            self.cylinder_1_retract_button.setEnabled(False)
            self.cylinder_2_extend_button.setEnabled(False)
            self.cylinder_2_retract_button.setEnabled(False)
        else:
            self.is_auto_mode = False
            # 寫入手動模式信號到線圈 1
            self.modbus.write_coil(1, False)
            self.current_mode_label.setText("手動")
            self.current_mode_label.setStyleSheet("color: blue;")
            self.statusBar().showMessage("切換到手動模式")
            # 禁用塗膠閥類型選擇
            self.valve_type_combo.setEnabled(False)
            self.path_combo.setEnabled(False)
            # 隱藏自動運行按鈕
            self.auto_run_button.setVisible(False)
            self.auto_run_button.setEnabled(False)
            # 啟用手動IO控制按鈕（手動模式允許手動塗膠）
            self.valve_on_button.setEnabled(True)
            self.valve_off_button.setEnabled(True)
            self.valve_2_on_button.setEnabled(True)
            self.valve_2_off_button.setEnabled(True)
            self.cylinder_1_extend_button.setEnabled(True)
            self.cylinder_1_retract_button.setEnabled(True)
            self.cylinder_2_extend_button.setEnabled(True)
            self.cylinder_2_retract_button.setEnabled(True)
    
    def on_valve_type_changed(self):
        """塗膠閥類型改變時觸發"""
        if not self.is_auto_mode:
            return
        
        selected_valve = self.valve_type_combo.currentText()
        logger.info(f"選擇的塗膠閥類型: {selected_valve}")
        
        # 檢查路徑下拉菜單是否有選項
        if self.path_combo.count() == 0:
            logger.warning("路徑下拉菜單中沒有選項，重新加載路徑")
            self.load_glue_paths()
        
        # 啟用路徑選擇
        self.path_combo.setEnabled(True)
        
        # 如果路徑下拉菜單為空選擇狀態，自動選擇第一個選項
        if self.path_combo.currentIndex() == -1 and self.path_combo.count() > 0:
            self.path_combo.setCurrentIndex(0)
            logger.info(f"自動選擇第一個路徑: {self.path_combo.currentText()}")
        
        # 如果有選擇了路徑，啟用自動運行按鈕
        if self.path_combo.currentIndex() >= 0:
            self.auto_run_button.setEnabled(True)
        
        self.statusBar().showMessage(f"已選擇: {selected_valve} - 已加載塗膠路徑，請選擇路徑")
    
    def on_path_selected(self):
        """路徑選擇改變時觸發"""
        if not self.is_auto_mode:
            return
        
        selected_path = self.path_combo.currentText()
        if selected_path:
            logger.info(f"已選擇路徑: {selected_path}")
            # 當同時選了閥類型和路徑時，啟用自動運行按鈕
            if self.valve_type_combo.currentText():
                self.auto_run_button.setEnabled(True)
                self.statusBar().showMessage(f"已準備好執行: [{self.valve_type_combo.currentText()}] {selected_path}")
    
    def load_glue_paths(self):
        """加載塗膠路徑列表 (從 DRA studio 程式讀取)"""
        try:
            # 使用 DRA 管理器加載路徑
            paths = self.dra_manager.get_available_paths()
            
            glue_paths = []
            if paths:
                # 格式：路徑名 (編號)
                for path_name, path_num in paths:
                    glue_paths.append(f"{path_name} ({path_num})")
                logger.info(f"成功加載 {len(glue_paths)} 個塗膠路徑: {glue_paths}")
            else:
                # 如果沒找到實際文件，使用預設範例
                logger.warning("未找到 DRA 路徑文件，使用預設路徑")
                glue_paths = [
                    "路徑 1 - 標準方形 (1)",
                    "路徑 2 - 圓形封邊 (2)",
                    "路徑 3 - 複雜軌跡 (3)",
                    "路徑 4 - 快速模式 (4)"
                ]
            
            self.path_combo.clear()
            self.path_combo.addItems(glue_paths)
            self.path_combo.setCurrentIndex(0)  # 預設選擇第一個選項
            logger.info(f"路徑下拉菜單已加載 {len(glue_paths)} 個選項")
            
        except Exception as e:
            logger.error(f"加載塗膠路徑時出錯: {e}")
            # 加載失敗時至少提供預設選項
            glue_paths = [
                "路徑 1 - 標準方形 (1)",
                "路徑 2 - 圓形封邊 (2)",
                "路徑 3 - 複雜軌跡 (3)",
                "路徑 4 - 快速模式 (4)"
            ]
            self.path_combo.clear()
            self.path_combo.addItems(glue_paths)
            self.path_combo.setCurrentIndex(0)  # 預設選擇第一個選項
            logger.warning(f"使用備用預設路徑: {glue_paths}")
    
    def start_auto_glue(self):
        """啟動自動運行塗膠"""
        if not self.is_auto_mode:
            QMessageBox.warning(self, "模式錯誤", "請先切換到自動模式")
            return
        
        # 檢查塗膠閥類型是否已選擇
        selected_valve = self.valve_type_combo.currentText()
        if not selected_valve or selected_valve == "":
            QMessageBox.warning(self, "塗膠閥未選擇", "請先選擇塗膠閥類型")
            return
        
        selected_path = self.path_combo.currentText()
        if not selected_path or selected_path == "":
            QMessageBox.warning(self, "路徑未選擇", "請先選擇塗膠路徑")
            return
        
        # 提取路徑編號 (格式: "路徑名 (編號)")
        path_number = self.extract_path_number(selected_path)
        if path_number <= 0:
            QMessageBox.warning(self, "路徑無效", "無法識別路徑編號")
            return
        
        # 根據選擇的塗膠閥類型寫入寄存器
        valve_type_data = self.valve_type_combo.currentData()  # 取得 "valve_1" 或 "valve_2"
        
        if valve_type_data == "valve_1":
            VALVE_REGISTER = self.config.getint('DRA_ROBOT_MODBUS', 'VALVE_TYPE_1_REGISTER', fallback=2000)
        else:  # valve_2
            VALVE_REGISTER = self.config.getint('DRA_ROBOT_MODBUS', 'VALVE_TYPE_2_REGISTER', fallback=2001)
        
        # 先寫入閥類型寄存器 (寫入 1 表示啟用該閥)
        if not self.modbus.write_register(VALVE_REGISTER, 1):
            QMessageBox.critical(self, "寫入失敗", "無法寫入塗膠閥寄存器")
            return
        
        # 寫入路徑執行寄存器觸發執行
        PATH_EXECUTE_REGISTER = self.config.getint('DRA_ROBOT_MODBUS', 'PATH_EXECUTE_REGISTER', fallback=1000)
        
        if self.modbus.write_register(PATH_EXECUTE_REGISTER, path_number):
            self.run_status_label.setText("自動塗膠運行中")
            self.run_status_label.setStyleSheet("color: darkgreen; font-weight: bold;")
            logger.info(f"已啟動自動塗膠: 閥類型={selected_valve} (寄存器: {VALVE_REGISTER}), 路徑={selected_path} (編號: {path_number})")
            self.statusBar().showMessage(f"自動塗膠運行中: [{selected_valve}] {selected_path}")
            # 設定定時器在2秒後重新啟用自動運行按鈕
            QTimer.singleShot(2000, self.re_enable_auto_run_button)
        else:
            QMessageBox.critical(self, "啟動失敗", "無法啟動自動塗膠")
            self.auto_run_button.setEnabled(True)
    
    def extract_path_number(self, path_text):
        """從路徑文本中提取編號
        
        Args:
            path_text (str): 路徑文本，格式為 "路徑名 (編號)"
            
        Returns:
            int: 路徑編號
        """
        import re
        match = re.search(r'\((\d+)\)', path_text)
        if match:
            return int(match.group(1))
        return 0
    
    def re_enable_auto_run_button(self):
        """在塗膠完成後 2 秒重新啟用自動運行按鈕"""
        if self.is_auto_mode:
            self.auto_run_button.setEnabled(True)
            self.run_status_label.setText("自動塗膠完成")
            self.run_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.statusBar().showMessage("自動塗膠已完成 - 可以開始新的運行")
    
    def valve_on(self):
        """打開膠閥（塗膠）"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'VALVE_ON_COIL'),
            True
        ):
            self.glue_valve_on = True
            self.valve_status_label.setText("狀態: 塗膠 (ON)")
            self.valve_status_label.setStyleSheet("color: green;")
            self.statusBar().showMessage("膠閥已打開 - 塗膠中")
        else:
            QMessageBox.warning(self, "控制失敗", "無法打開膠閥")
    
    def valve_off(self):
        """關閉膠閥（停膠）"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'VALVE_OFF_COIL'),
            True
        ):
            self.glue_valve_on = False
            self.valve_status_label.setText("狀態: 停膠 (OFF)")
            self.valve_status_label.setStyleSheet("color: red;")
            self.statusBar().showMessage("膠閥已關閉 - 停止塗膠")
        else:
            QMessageBox.warning(self, "控制失敗", "無法關閉膠閥")
    
    def valve_2_on(self):
        """打開熱固化三防滴膠閥"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'VALVE_2_ON_COIL'),
            True
        ):
            self.valve_2_status_label.setText("狀態: 開啟 (ON)")
            self.valve_2_status_label.setStyleSheet("color: green;")
            self.statusBar().showMessage("熱固化三防滴膠閥已開啟")
        else:
            QMessageBox.warning(self, "控制失敗", "無法打開熱固化三防滴膠閥")
    
    def valve_2_off(self):
        """關閉熱固化三防滴膠閥"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'VALVE_2_OFF_COIL'),
            True
        ):
            self.valve_2_status_label.setText("狀態: 關閉 (OFF)")
            self.valve_2_status_label.setStyleSheet("color: red;")
            self.statusBar().showMessage("熱固化三防滴膠閥已關閉")
        else:
            QMessageBox.warning(self, "控制失敗", "無法關閉熱固化三防滴膠閥")
    
    def cylinder_1_extend(self):
        """圍壩膠氣缸伸出"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'CYLINDER_1_EXTEND_COIL'),
            True
        ):
            self.cylinder_1_status_label.setText("狀態: 伸出")
            self.cylinder_1_status_label.setStyleSheet("color: green;")
            self.statusBar().showMessage("圍壩膠氣缸已伸出")
        else:
            QMessageBox.warning(self, "控制失敗", "無法伸出圍壩膠氣缸")
    
    def cylinder_1_retract(self):
        """圍壩膠氣缸收回"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'CYLINDER_1_RETRACT_COIL'),
            True
        ):
            self.cylinder_1_status_label.setText("狀態: 收回")
            self.cylinder_1_status_label.setStyleSheet("color: red;")
            self.statusBar().showMessage("圍壩膠氣缸已收回")
        else:
            QMessageBox.warning(self, "控制失敗", "無法收回圍壩膠氣缸")
    
    def cylinder_2_extend(self):
        """熱固化三防膠氣缸伸出"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'CYLINDER_2_EXTEND_COIL'),
            True
        ):
            self.cylinder_2_status_label.setText("狀態: 伸出")
            self.cylinder_2_status_label.setStyleSheet("color: green;")
            self.statusBar().showMessage("熱固化三防膠氣缸已伸出")
        else:
            QMessageBox.warning(self, "控制失敗", "無法伸出熱固化三防膠氣缸")
    
    def cylinder_2_retract(self):
        """熱固化三防膠氣缸收回"""
        if self.modbus.write_coil(
            self.config.getint('IO_CONTROL', 'CYLINDER_2_RETRACT_COIL'),
            True
        ):
            self.cylinder_2_status_label.setText("狀態: 收回")
            self.cylinder_2_status_label.setStyleSheet("color: red;")
            self.statusBar().showMessage("熱固化三防膠氣缸已收回")
        else:
            QMessageBox.warning(self, "控制失敗", "無法收回熱固化三防膠氣缸")
    
    def update_status(self):
        """定時更新系統狀態"""
        if self.modbus.is_connected:
            # 可以在這裡添加讀取狀態的邏輯
            pass
    
    def closeEvent(self, event):
        """視窗關閉事件"""
        self.status_timer.stop()
        if self.modbus.is_connected:
            self.modbus.disconnect()
        event.accept()


def main():
    """主程序入口"""
    app = QApplication(sys.argv)
    window = RobotControlUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
