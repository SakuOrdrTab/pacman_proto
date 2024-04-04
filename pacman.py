# Pac-man representation time counter
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QGuiApplication, QScreen, QPixmap
from PySide6.QtCore import QPropertyAnimation, QTimer, QRect, Qt

class PacmanWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set the window to be always on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        # Set the window size to the screen size
        display_dimensions = QScreen.availableGeometry(QGuiApplication.primaryScreen())
        print(display_dimensions)
        # Set the height of the window to 1/16 of the screen height
        display_dimensions.setHeight(display_dimensions.height() // 16)
        self.setGeometry(display_dimensions)
        # Make the window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUI()
        # Save also the pacman size for more readable code
        self._pacman_size = self.pacmanOpen.height()

    def initUI(self):
        self.setWindowTitle('Pacman representation time guardian')

        # Load pacman pictures
        self.pacmanOpen = QPixmap('pacman_mouth_open.png').scaled(self.height(), self.height())  # Pac-Man with mouth open
        self.pacmanClosed = QPixmap('pacman_mouth_close.png').scaled(self.height(), self.height()) # Pac-Man with mouth closed

        # Save the state of the pacman's mouth
        self._mouth_open = True

        # Create a QLabel widget for Pac-Man
        self.pacmanLabel = QLabel(self)
        self.pacmanLabel.setPixmap(self.pacmanOpen)
        self.pacmanLabel.resize(self.pacmanOpen.size())

        # Start the animation
        QTimer.singleShot(100, self.startMovingAnimation)
        self.startMouthAnimation()
        # Save the window size as variables
        self._screen_width = self.width()  # Get the current width of the window
        print(self._screen_width)
        self._screen_height = self.height()  # Get the current height of the window
        print(self._screen_height)


    def startMovingAnimation(self):
        #  Ensure the entire size of the Pac-Man image is accommodated
        startRect = QRect(0, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # Start at the left, centered vertically
        endRect = QRect(self._screen_width, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # End at the right, centered vertically


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
        # Use the attribute to check the mouth state
        if self._mouth_open:
            self.pacmanLabel.setPixmap(self.pacmanClosed)
        else:
            self.pacmanLabel.setPixmap(self.pacmanOpen)
        self._mouth_open = not self._mouth_open  # Toggle the state

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pacman_window = PacmanWindow()
    pacman_window.show()
    sys.exit(app.exec())
