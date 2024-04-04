# Pac-man representation time counter
import sys
import time
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QGuiApplication, QScreen, QPixmap
from PySide6.QtCore import QPropertyAnimation, QTimer, QRect, Qt

class PacmanWindow(QWidget):
    def __init__(self, counter_minutes : float = 5):
        super().__init__()
        self._minutes = counter_minutes
        # Set pacman to show up in the end of the time
        if self._minutes > 15:
            self._animation_duration = 10
        elif self._minutes > 5:
            self._animation_duration = 5
        else:
            self._animation_duration = self._minutes
        time.sleep((self._minutes-self._animation_duration) * 60)
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
        """Loads the pacman pictures, creates a QLabel to show the pacman. The animation is started and some internal states are saved.
        """        
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
        """Starts the pacman's moving animation. The pacman will move from the left to the right of the screen.
        """        
        #  Ensure the entire size of the Pac-Man image is accommodated
        startRect = QRect(0, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # Start at the left, centered vertically
        endRect = QRect(self._screen_width, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # End at the right, centered vertically


        self.movingAnimation = QPropertyAnimation(self.pacmanLabel, b"geometry")
        self.movingAnimation.setDuration(self._animation_duration * 60 *1000) # Set pacman animation duration
        self.movingAnimation.setStartValue(startRect)
        self.movingAnimation.setEndValue(endRect)
        self.movingAnimation.setLoopCount(1)  # -1 for infinite loop
        self.movingAnimation.start()

    def startMouthAnimation(self):
        """Starts the pacman's mouth animation. The mouth will open and close every 500 ms.
        """        
        self.mouthTimer = QTimer(self)
        self.mouthTimer.timeout.connect(self.toggleMouth)
        self.mouthTimer.start(500)  # Adjust the interval for faster/slower mouth animation

    def toggleMouth(self):
        """Toggles the pic of pacman: open or closed mouth. State is saved in the attribute self._mouth_open.
        """
        if self._mouth_open:
            self.pacmanLabel.setPixmap(self.pacmanClosed)
        else:
            self.pacmanLabel.setPixmap(self.pacmanOpen)
        self._mouth_open = not self._mouth_open 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        try:
            minutes_to_go = float(sys.argv[1])
        except ValueError:
            print("The argument must be a number")
            sys.exit(1)
    else:
        minutes_to_go = 6
    print("Counter measuring time in minutes: ", minutes_to_go)
    pacman_window = PacmanWindow(counter_minutes=minutes_to_go)
    pacman_window.show()
    sys.exit(app.exec())
