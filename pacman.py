# Pac-man representation time counter
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QGuiApplication, QScreen
from PySide6.QtCore import QPropertyAnimation, QTimer, QRect, Qt

class AnimationDemo(QWidget):
    def __init__(self):
        super().__init__()
        # Set the window to be always on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        # Set the window size to the screen size
        display_dimensions = QScreen.availableGeometry(QGuiApplication.primaryScreen())
        print(display_dimensions)
        # Set the height of the window to 1/20 of the screen height
        display_dimensions.setHeight(display_dimensions.height() // 20)
        self.setGeometry(display_dimensions)
        # Make the window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pacman representation time guardian')

        # Create a QLabel widget
        self.label = QLabel('Move Me!', self)
        self.label.setStyleSheet("background-color: yellow; border: 1px solid black;")

        # Delay the start of the animation
        QTimer.singleShot(100, self.startAnimation)  # Delay in milliseconds


    def startAnimation(self):
        screenWidth = self.width()  # Get the current width of the window
        print(screenWidth)
        screenHeight = self.height()  # Get the current height of the window
        print(screenHeight)

        # Adjust start and end values based on screen size
        startRect = QRect(0, screenHeight // 2, 100, 30)  # Start at the left, centered vertically
        endRect = QRect(screenWidth - 100, screenHeight // 2, 100, 30)  # End at the right, centered vertically

        self.animation = QPropertyAnimation(self.label, b"geometry")
        self.animation.setDuration(2000)  # Animation duration: 2 seconds
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(endRect)
        self.animation.setLoopCount(-1)  # -1 for infinite loop
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AnimationDemo()
    demo.show()
    sys.exit(app.exec())
