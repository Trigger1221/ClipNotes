# ui/splash_screen.py
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setEnabled(False)

        # Set dark theme colors
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(dark_palette)

    def showMessage(self, message, alignment=Qt.AlignBottom | Qt.AlignHCenter, color=Qt.white):
        super().showMessage(message, alignment, color)