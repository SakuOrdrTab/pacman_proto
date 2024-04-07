''' Pac-man representation time counter '''

# Version: 1.0
# Todo:
# - replace sys.argv with argparse, add --brutal, --duration, --help
# - add pacman pics smoothen animation
# - Set aspect ratio for pacman face

import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtGui import QGuiApplication, QScreen, QPixmap
from PySide6.QtCore import QPropertyAnimation, QTimer, QRect, Qt

class PacmanWindow(QWidget):
    def __init__(self, counter_minutes : float = 5):
        super().__init__()
        self._minutes = counter_minutes
        print("Counter measuring time in minutes: ", self._minutes)
        # Set pacman to show up in the end of the time
        if self._minutes > 15:
            self._animation_duration = 10
        elif self._minutes > 5:
            self._animation_duration = 5
        else:
            self._animation_duration = self._minutes if self._minutes > 0 else 0.01 # ensure non negative time

        animation_start_delay_ms = (self._minutes - self._animation_duration) * 60 * 1000
        
        # Window setup
        self.setup_window()

        # Delay starting the animations
        QTimer.singleShot(animation_start_delay_ms, self.start_animations)

    def setup_window(self):
        """Set up the window and load UI components immediately."""
        # Set the window to be always on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        # Set the window size to the screen size
        display_dimensions = QScreen.availableGeometry(QGuiApplication.primaryScreen())
        # Set the height of the window to 1/16 of the screen height
        display_dimensions.setHeight(display_dimensions.height() // 16)
        self.setGeometry(display_dimensions)
        # Make the window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Set window flags and geometry
        self.setWindowTitle('Pacman representation time guardian')

        # Load pacman pictures and set up QLabel for Pac-Man...
        self.load_pacman_pictures()

        # Save the window size as variables
        self._screen_width = self.width()  # Get the current width of the window
        print(self._screen_width)
        self._screen_height = self.height()  # Get the current height of the window
        print(self._screen_height)

        self.init_pills(self._animation_duration)
        print(f"Animation duration: {self._animation_duration}")

    def load_pacman_pictures(self):
        """Loads the pacman pictures and prepares the QLabel."""
        # Load pacman pictures...
        self.pacmanOpen = QPixmap('pacman_mouth_open.png').scaled(self.height(), self.height())
        self.pacmanClosed = QPixmap('pacman_mouth_close.png').scaled(self.height(), self.height())
        # Load end animation image, don't resize yet
        self.pacman_face = QPixmap('pacman_face.png')

        # Save also the pacman size for more readable code
        self._pacman_size = self.pacmanOpen.height()
        # Save the state of the pacman's mouth
        self._mouth_open = True

        # Create a QLabel widget for Pac-Man
        self.pacmanLabel = QLabel(self)
        self.pacmanLabel.setPixmap(self.pacmanOpen)
        self.pacmanLabel.resize(self.pacmanOpen.size())

        # Initially hide the Pac-Man QLabel
        self.pacmanLabel.hide()

    def init_pills(self, pill_count):
        """Initializes the pills to be eaten by pacman in QLabels in correct spots in the screen.

        Args:
            pill_count (float): initially from self._animation_duration (float) converted to int
        """        
        self.pill_labels = []
        pill_spacing = self._screen_width / pill_count
        for i in range(int(pill_count)):
            pill_label = QLabel(self)
            pill_label.setPixmap(QPixmap('pill.png').scaledToWidth(self.height()))  # Pill's height is the same as the window's height
            x_position = i * pill_spacing
            pill_label.move(x_position, 0)  
            pill_label.hide()  # Initially hide the pills until the animation starts
            self.pill_labels.append((pill_label, x_position))

    
    def start_animations(self):
        """Starts the moving and mouth animations for Pac-Man."""
        # Show the pills at the start of the animation
        for pill_label, _ in self.pill_labels:
            pill_label.show()
        
        self.pacmanLabel.show()
        self.start_moving_animation()
        self.start_mouth_animation()

        # Start a timer to check for pill consumption
        self.check_pill_timer = QTimer(self)
        self.check_pill_timer.timeout.connect(self.check_pill_consumption)
        self.check_pill_timer.start(100)  # Check every 100 milliseconds

    def check_pill_consumption(self):
        """Checks the position of pacman and hides the pill QLabel if it has been "eaten"
        """        
        pacman_right_edge = self.pacmanLabel.x() + self.pacmanLabel.width()
        # Iterate through pills to see if Pac-Man has "eaten" them
        for pill_label, x_position in self.pill_labels[:]:  # Copy the list to avoid modification issues
            if pacman_right_edge >= x_position:
                pill_label.hide()  # Hide the pill
                self.pill_labels.remove((pill_label, x_position))  # Remove the pill from tracking list

    def start_moving_animation(self):
        """Starts the pacman's moving animation. The pacman will move from the left to the right of the screen.
        """        
        #  Ensure the entire size of the Pac-Man image is accommodated
        startRect = QRect(0, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # Start at the left, centered vertically
        endRect = QRect(self._screen_width, self._screen_height // 2 - self._pacman_size // 2, self._pacman_size, self._pacman_size)  # End at the right, centered vertically

        # Create the animation object
        self.moving_animation = QPropertyAnimation(self.pacmanLabel, b"geometry")
        self.moving_animation.setDuration(self._animation_duration * 60 *1000) # Set pacman animation duration
        self.moving_animation.setStartValue(startRect)
        self.moving_animation.setEndValue(endRect)
        self.moving_animation.setLoopCount(1)  # -1 for infinite loop
        # Connect the finished signal to the end_of_time method
        self.moving_animation.finished.connect(self.end_of_time)

        self.moving_animation.start()

    def start_mouth_animation(self):
        """Starts the pacman's mouth animation. The mouth will open and close every 500 ms.
        """        
        self.mouthTimer = QTimer(self)
        self.mouthTimer.timeout.connect(self.toggle_mouth)
        self.mouthTimer.start(500)  # Adjust the interval for faster/slower mouth animation

    def toggle_mouth(self):
        """Toggles the pic of pacman: open or closed mouth. State is saved in the attribute self._mouth_open.
        """
        if self._mouth_open:
            self.pacmanLabel.setPixmap(self.pacmanClosed)
        else:
            self.pacmanLabel.setPixmap(self.pacmanOpen)
        self._mouth_open = not self._mouth_open 

    def end_of_time(self):
        """Pacman engulfs the screen."""
        def end_alert():
            # Helper function to show the final alert message
            end_widget = QMessageBox(self)
            end_widget.setWindowTitle("!")
            end_widget.setIcon(QMessageBox.Critical)
            end_widget.setText("Time is up!")
            end_widget.addButton(QMessageBox.Ok)
            end_widget.exec()
            sys.exit(0)
        self.check_pill_timer.stop()  # Stop checking for pill consumption

        self.pacmanLabel.hide()  # Hide the old pacman widget
        
        # Maximize the window to ensure it covers the full screen
        self.showMaximized()

        # Create widget for end animation
        self.end_label = QLabel(self)
        self.end_label.setAlignment(Qt.AlignCenter)  # Ensure the pixmap stays centered
        self.end_label.setScaledContents(True)  # Enable scaling of the pixmap with the label
        
        # Set the pixmap without scaling it here; let the label handle scaling
        self.end_label.setPixmap(self.pacman_face)
        self.end_label.resize(self._pacman_size, self._pacman_size)
        self.end_label.show()

        # Start position centered within the visible window
        centerX = self.width() / 2 - self._pacman_size / 2
        centerY = self.height() / 2 - self._pacman_size / 2
        startRect = QRect(centerX, centerY, self._pacman_size, self._pacman_size)

        # End at full window size
        endRect = QRect(0, 0, self.width(), self.height())

        self.endAnimation = QPropertyAnimation(self.end_label, b"geometry")
        self.endAnimation.setDuration(1000)  # Duration 1 seconds
        self.endAnimation.setStartValue(startRect)
        self.endAnimation.setEndValue(endRect)
        self.endAnimation.setLoopCount(1)
        self.endAnimation.start()

        print("Time is up!")

        # Show the alert 0.5 seconds after the animation ends
        QTimer.singleShot(1500, end_alert)  

class TimeWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Time")
        self.layout = QVBoxLayout()
        
        self.info_label = QLabel("No counter time was provided in command line arguments.\nPlease provide a time in minutes:")
        self.layout.addWidget(self.info_label)
        
        self.time_input = QLineEdit()
        self.layout.addWidget(self.time_input)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        
        self.setLayout(self.layout)

    def get_time(self):
        return self.time_input.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    if len(sys.argv) > 1:
        try:
            minutes_to_go = float(sys.argv[1])
        except ValueError:
            print("The argument must be a number")
            sys.exit(1)
    else:
        timeWindow = TimeWindow()
        if timeWindow.exec() == QDialog.Accepted:
            try:
                minutes_to_go = float(timeWindow.get_time())
            except ValueError:
                print("The argument must be a number")
                sys.exit(1)
        else:
            sys.exit(0)  # Exit if user cancels
    
    pacman_window = PacmanWindow(counter_minutes=minutes_to_go)
    pacman_window.show()
    sys.exit(app.exec())