# ui/settings_dialog.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from utils.config import load_config, save_config
import keyboard
import yaml

class HotkeyCaptureButton(QPushButton):
    def __init__(self, label, parent=None):
        super(HotkeyCaptureButton, self).__init__(label, parent)
        self.clicked.connect(self.capture_hotkey)

    def capture_hotkey(self):
        self.setText("Press a hotkey combination...")
        hotkey = keyboard.read_hotkey(suppress=False)
        self.setText(f"Set Hotkey: {hotkey}")
        self.parent().update_hotkey(self.objectName(), hotkey)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.config = load_config()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 400, 200)

        # Set dark theme colors
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        hotkeysLayout = QHBoxLayout()
        hotkeysLayout.setSpacing(20)

        self.startStopHotkeyButton = HotkeyCaptureButton("Set Start/Stop Hotkey")
        self.startStopHotkeyButton.setObjectName("start_stop_hotkey")
        self.startStopHotkeyButton.setStyleSheet('''
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        ''')
        hotkeysLayout.addWidget(QLabel("Start/Stop Hotkey:"))
        hotkeysLayout.addWidget(self.startStopHotkeyButton)

        self.noteHotkeyButton = HotkeyCaptureButton("Set Note Hotkey")
        self.noteHotkeyButton.setObjectName("note_hotkey")
        self.noteHotkeyButton.setStyleSheet('''
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        ''')
        hotkeysLayout.addWidget(QLabel("Note Hotkey:"))
        hotkeysLayout.addWidget(self.noteHotkeyButton)

        layout.addLayout(hotkeysLayout)

        self.clearDescriptionCheckBox = QCheckBox("Clear description after updating or creating a note", self)
        self.clearDescriptionCheckBox.setChecked(self.config['clear_description'])
        self.clearDescriptionCheckBox.setStyleSheet('''
            QCheckBox {
                color: white;
                font-size: 14px;
            }
        ''')
        layout.addWidget(self.clearDescriptionCheckBox)
        
        self.soundEffectsCheckBox = QCheckBox("Enable sound effects", self)
        self.soundEffectsCheckBox.setChecked(self.config['sound_effects'])
        self.soundEffectsCheckBox.setStyleSheet('''
            QCheckBox {
                color: white;
                font-size: 14px;
            }
        ''')
        layout.addWidget(self.soundEffectsCheckBox)

        self.saveButton = QPushButton('Save', self)
        self.saveButton.clicked.connect(self.save_settings)
        self.saveButton.setStyleSheet('''
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        ''')
        layout.addWidget(self.saveButton, alignment=Qt.AlignCenter)

    def update_hotkey(self, hotkey_name, hotkey_value):
        self.config[hotkey_name] = hotkey_value

    def save_settings(self):
        self.config['clear_description'] = self.clearDescriptionCheckBox.isChecked()
        self.config['sound_effects'] = self.soundEffectsCheckBox.isChecked()
        save_config(self.config)
        self.accept()