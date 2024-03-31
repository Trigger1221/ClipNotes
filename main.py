# main.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash_pixmap = QPixmap('ui/splash_screen.png')  # Replace with your splash image path
    splash_screen = SplashScreen(splash_pixmap)
    splash_screen.show()

    main_window = MainWindow()

    splash_screen.showMessage("Loading...")
    splash_screen.finish(main_window)

    main_window.show()
    sys.exit(app.exec_())