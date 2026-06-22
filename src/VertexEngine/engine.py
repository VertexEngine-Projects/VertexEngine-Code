from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QTimer, Qt
import pygame
from .scenes import SceneManager
from VertexEngine.InputSystem.KeyInputs import Input

pygame.init()

class GameEngine(QWidget):
    """`GameEngine()` is a class to create the window for your VertexEngine game."""
    def __init__(self, width=800, height=600, color=(50, 50, 100), fps=60, position=(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.fps = fps
        self.position = position 

        self.keys_down = set()
        
        # Optimized: Use standard RGB to avoid unneeded alpha calculations
        self.screen = pygame.Surface((self.width, self.height))
        
        # Optimized: Pre-allocate a persistent QImage that shares memory with Pygame
        self._sync_qimage()

        self.scene_manager = SceneManager()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(1000 // self.fps)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(self.width, self.height)
        self.move(*self.position)

    def _sync_qimage(self):
        """Helper to map Pygame pixel buffer directly to QImage memory."""
        # Optimized: QImage points directly to the Pygame surface memory buffer
        # This completely removes pygame.image.tobytes() CPU copying overhead
        self.img = QImage(
            self.screen.get_buffer(),
            self.width,
            self.height,
            self.screen.get_pitch(),
            QImage.Format.Format_RGB32
        )

    # ---------------------- RENDER ----------------------

    def paintEvent(self, event):
        # Optimized: Use a context manager to instantly close/flush the painter
        with QPainter(self) as painter:
            painter.drawImage(0, 0, self.img)

    def resizeEvent(self, event):
        size = event.size()
        self.width = size.width()
        self.height = size.height()
        
        # Re-allocate surfaces and re-link memory map on resize
        self.screen = pygame.Surface((self.width, self.height))
        self._sync_qimage()

    # ---------------------- UPDATE ----------------------

    def _update_frame(self):
        if not self.hasFocus():
            self.keys_down.clear()

        # Optimized: Clear and draw into the pygame surface during the update step
        self.screen.fill(self.color)
        self.scene_manager._update()
        self.scene_manager.draw(self.screen)
        
        # Schedule the visual swap
        self.update()  

    # ---------------------- INPUT ----------------------

    def keyPressEvent(self, event):
        Input._key_down(event.key())

    def keyReleaseEvent(self, event):
        Input._key_up(event.key())

    def mousePressEvent(self, event):
        # Optimized: Extracted local positions to avoid multiple property lookups
        pos = event.position()
        pygame_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": (int(pos.x()), int(pos.y())), "button": event.button()}
        )
        self.scene_manager.handle_event(pygame_event)

    def mouseReleaseEvent(self, event):
        pos = event.position()
        pygame_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {"pos": (int(pos.x()), int(pos.y())), "button": event.button()}
        )
        self.scene_manager.handle_event(pygame_event)

    def mouseMoveEvent(self, event):
        pos = event.position()
        pygame_event = pygame.event.Event(
            pygame.MOUSEMOTION,
            {
                "pos": (int(pos.x()), int(pos.y())),
                "rel": (0, 0),
                "buttons": pygame.mouse.get_pressed()
            }
        )
        self.scene_manager.handle_event(pygame_event)
