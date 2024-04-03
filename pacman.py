# Pac-man representation time counter
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QGuiApplication, QScreen, QPixmap
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
        # display_dimensions.setHeight(display_dimensions.height() // 10)
        # Set display height to pacman picture, 200 pixels
        display_dimensions.setHeight(200)
        self.setGeometry(display_dimensions)
        # Make the window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pacman representation time guardian')

        self.pacmanOpen = QPixmap('pacman_mouth_open.png')  # Pac-Man with mouth open
        self.pacmanClosed = QPixmap('pacman_mouth_close.png')  # Pac-Man with mouth closed

        # Create a QLabel widget for Pac-Man
        self.pacmanLabel = QLabel(self)
        self.pacmanLabel.setPixmap(self.pacmanOpen)
        self.pacmanLabel.resize(self.pacmanOpen.size())

        # Start the animation
        QTimer.singleShot(100, self.startMovingAnimation)
        self.startMouthAnimation()


    def startMovingAnimation(self):
        screenWidth = self.width()  # Get the current width of the window
        print(screenWidth)
        screenHeight = self.height()  # Get the current height of the window
        print(screenHeight)

        #  Ensure the entire 200x200 size of the Pac-Man image is accommodated
        startRect = QRect(0, screenHeight // 2 - 100, 200, 200)  # Start at the left, centered vertically
        endRect = QRect(screenWidth - 200, screenHeight // 2 - 100, 200, 200)  # End at the right, centered vertically


        self.movingAnimation = QPropertyAnimation(self.pacmanLabel, b"geometry")
        self.movingAnimation.setDuration(10000)  # Animation duration: 2 seconds
        self.movingAnimation.setStartValue(startRect)
        self.movingAnimation.setEndValue(endRect)
        self.movingAnimation.setLoopCount(-1)  # -1 for infinite loop
        self.movingAnimation.start()

    def startMouthAnimation(self):
        self.mouthTimer = QTimer(self)
        self.mouthTimer.timeout.connect(self.toggleMouth)
        self.mouthTimer.start(500)  # Adjust the interval for faster/slower mouth animation

    def toggleMouth(self):
        if self.pacmanLabel.pixmap() == self.pacmanOpen:
            self.pacmanLabel.setPixmap(self.pacmanClosed)
        else:
            self.pacmanLabel.setPixmap(self.pacmanOpen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AnimationDemo()
    demo.show()
    sys.exit(app.exec())
