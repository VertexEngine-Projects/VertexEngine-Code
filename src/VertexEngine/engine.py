from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QTimer, Qt
import pygame
from .scenes import SceneManager
from VertexEngine.InputSystem.KeyInputs import Input

pygame.init()

class GameEngine(QWidget):
    """`GameEngine()` is a class to create the window for your VertexEngine game. \n
        `width` is the resolution of your window in WIDTH. \n
        `height` is the resolution of your window in HEIGHT. \n
        The standard notation for checking resolution is `(width x height)`. \n
        Aspect ratio is the ratio of `height:width` and is crucial if you want scaling by window size. \n
        `color` is the actual color of the Background of the window. It is a tuple in `(R, G, B)`. \n
        `fps` is the amount of calculations that the engine makes every second. It's recommended to be less than your screen refresh rate. \n
        `position` is the window position on screen as a tuple `(x, y)`. `(0, 0)` is the top-left corner.
    """
    def __init__(self, width=800, height=600, color=(50, 50, 100), fps=60, position=(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.fps = fps
        self.position = position  # (x, y)

        # Qt key tracking
        self.keys_down = set()

        # pygame surface
        self.screen = pygame.Surface((self.width, self.height))

        # Scene manager
        self.scene_manager = SceneManager()

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // self.fps)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Set window size and position
        self.resize(self.width, self.height)
        self.move(*self.position)

    # ---------------------- RENDER ----------------------

    def paintEvent(self, event):
        self.screen.fill(self.color)

        self.scene_manager.draw(self.screen)

        raw = pygame.image.tobytes(self.screen, "RGBA")
        img = QImage(
            raw,
            self.width,
            self.height,
            QImage.Format.Format_RGBA8888
        )

        painter = QPainter(self)
        painter.drawImage(0, 0, img)

    def resizeEvent(self, event):
        size = event.size()
        self.width = size.width()
        self.height = size.height()
        self.screen = pygame.Surface((self.width, self.height))

    # ---------------------- UPDATE ----------------------

    def update_frame(self):
        if not self.hasFocus():
            self.keys_down.clear()

        self.scene_manager.update()
        self.update()  # triggers paintEvent

    # ---------------------- INPUT ----------------------

    def keyPressEvent(self, event):
        Input.key_down(event.key())

    def keyReleaseEvent(self, event):
        Input.key_up(event.key())
