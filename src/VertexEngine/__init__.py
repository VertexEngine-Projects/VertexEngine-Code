# VertexEngine/__init__.py
# Copyright (C) 2025
# This library/SDK is free. You can redistribute it.
# Tyrel Gomez (email as annbasilan)
# annbasilan0828@gmail.com
"""VertexEngine is an SDK for Application Development. It's also supported by many others.

Supported OSes 
--------------
- RainOS 
- Windows 
- MacOS, 
- OS X 
- BeOS 
- FreeBSD 
- IRIX  
- and Linux

It is written on top of the excellent Pygame library which is ran on the even more excellent SDL library which runs on every Desktop OS with SDL."""
import pygame
from .engine import GameEngine
from .scenes import Scene, SceneManager
from .assets import AssetManager
from .audio import AudioManager
from pygame.base import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from pygame import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel, QWidget
from PyQt6.QtGui import QFont, QCursor, QFontMetrics
from PyQt6.QtCore import Qt
from typing_extensions import deprecated as dep
from VertexEngine.Vertex import VBox
class VertexScreen():
    """Draw on VertexEngine's Screen."""
    def __init__(self):
        pass
    class Draw():
        "The Draw class to draw on VertexEngine"
        def __init__(self):
            pass
        def rect(self, surface, color, rect=None):
            """Draw a Rectangle of a solid color."""
            pygame.draw.rect(surface, color, rect)
        def polygon(self, surface, color, points, width):
            "Draw a polygon by marking points on the screen to make an n-gon"
            pygame.draw.polygon(surface, color, points, width)
        def circle(self, circle_surface, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_right, draw_bottom_left):
            """Draw a Circle with radius, color, etc."""
            pygame.draw.circle(circle_surface, color, center, radius, width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
        def ellipse(self, surface, color, rect, width):
            """Draw an elipse with surface, color, rect and width""" 
            pygame.draw.ellipse(surface, color, rect, width)
        def arc(self, surface, color, rect, start_angle, stop_angle, width):
            "Draw an arc with a lot of values"
            pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width)
        def line(self, surface, color, start_pos, end_pos, width):
            """Draw a line"""
            pygame.draw.line(surface, color, start_pos, end_pos, width)
        def lines(self, surface, color, closed, points, width):
            '''Draw a pair of lines'''
            pygame.draw.lines(surface, color, closed, points, width)
        def aaline(
            self,
            surface,
            color,
            start_pos,
            end_pos,
            blend,
        ):
            '''Draw an aaline'''
            pygame.draw.aaline(surface, color, start_pos, end_pos, blend)
        def aalines(
            self,
            surface,
            color,
            closed,
            points,
            blend
        ):
            '''Draw a set of aalines'''
            pygame.draw.aalines(surface, color, closed, points, blend)
    class Font():
        """VertexEngine's offical Font Engine"""
        def __init__(self, path=None, size=24, antialias=True):
            self.font = pygame.font.Font(path, size)
            self.size = size
            self.antialias = antialias
        
        def draw(
                self,
                surface,
                text,
                pos,
                color=(255, 255, 255),
                align="topleft",
                center=False,
                shadow=False,
                shadow_color=(0, 0, 0),
                shadow_offset=(2, 2),
                outline=False,
                outline_color=(0, 0, 0),
                outline_thickness=1
            ):      
                text_surf = self.font.render(text, self.antialias, color)
                rect = text_surf.get_rect()

                if center:
                    rect.center = pos
                else:
                    setattr(rect, align, pos)

                # 🔲 Outline
                if outline:
                    for dx in range(-outline_thickness, outline_thickness + 1):
                        for dy in range(-outline_thickness, outline_thickness + 1):
                            if dx == 0 and dy == 0:
                                continue
                            outline_surf = self.font.render(text, self.antialias, outline_color)
                            surface.blit(outline_surf, rect.move(dx, dy))

                # 🌑 Shadow
                if shadow:
                    shadow_surf = self.font.render(text, self.antialias, shadow_color)
                    shadow_rect = rect.move(shadow_offset)
                    surface.blit(shadow_surf, shadow_rect)

                surface.blit(text_surf, rect)

        @dep("Unlike internal APIs, this one is fully deprecated, NEVER USE THIS. EVER :)")
        def draw_text(
            surface,
            text,
            font,
            color,
            pos,
            align="topleft",
            shadow=False,
            shadow_color=(0, 0, 0),
            shadow_offset=(2, 2)
        ):
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect()

            setattr(text_rect, align, pos)

            if shadow:
                shadow_surf = font.render(text, True, shadow_color)
                shadow_rect = shadow_surf.get_rect()
                setattr(shadow_rect, align, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
                surface.blit(shadow_surf, shadow_rect)

            surface.blit(text_surf, text_rect)
class Rect():
    '''Define a rect to pass into VertexScreen.Draw.rect()'''
    def __init__(self, left, top, width, height):
        pygame.Rect(left, top, width, height)

class VertexUI():
    # QPushButton *button = new QPushButton(tr("Ro&ck && Roll"), this)
    def __init__(self):
        pass

    class AutoFontLabel(QLabel):
        def __init__(self, text="", parent=None):
            super().__init__(text, parent)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def resizeEvent(self, event):
            self.adjustFont()
            super().resizeEvent(event)

        def adjustFont(self):
            if not self.text():
                return
            # Start with a large font and shrink until it fits
            font = self.font()
            font_size = self.height()  # start big
            font.setPointSize(font_size)
            metrics = QFontMetrics(font)

            while metrics.width(self.text()) > self.width() and font_size > 1:
                font_size -= 1
                font.setPointSize(font_size)
                metrics = QFontMetrics(font)
            self.setFont(font)

    class FancyButton(QPushButton):
        def __init__(
            self,
            text="Button",
            x=0,
            y=0,
            width=120,
            height=40,
            bg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            border_radius=10,
            border_color="#388E3C",
            border_width=2,
            font_name="Arial",
            font_size=12,
            font_weight=QFont.Weight.Bold,
            parent=None
        ):
            class FancyButton(QPushButton):
                """
                A customizable Button with enhanced styling and hover effects, 
                allowing easy position placement within a parent widget.

                Features:
                - Customizable background, hover, and text colors.
                - Adjustable border radius, color, and width.
                - Custom font settings (name, size, weight).
                - Hover effect with automatic style change.
                - Positioning via (x, y) coordinates relative to parent widget.
                - Cursor changes to a pointing hand on hover.

                Parameters:
                -----------
                text : str, optional
                    The text displayed on the button. Default is "Button".

                width : int, optional
                    The minimum width of the button in pixels. Default is 120.

                height : int, optional
                    The minimum height of the button in pixels. Default is 40.

                x : int, optional
                    The horizontal position of the button relative to its parent widget's top-left corner.
                    Default is 0 (top-left).

                y : int, optional
                    The vertical position of the button relative to its parent widget's top-left corner.
                    Default is 0 (top-left).

                bg_color : str, optional
                    Background color of the button in normal state (CSS color format). Default is "#4CAF50".

                hover_color : str, optional
                    Background color of the button when hovered over. Default is "#45A049".

                text_color : str, optional
                    Color of the button text. Default is "white".

                border_radius : int, optional
                    Radius of the button corners in pixels. Default is 10.

                border_color : str, optional
                    Color of the button border. Default is "#388E3C".

                border_width : int, optional
                    Width of the button border in pixels. Default is 2.

                font_name : str, optional
                    Name of the font used for the button text. Default is "Arial".

                font_size : int, optional
                    Size of the font used for the button text. Default is 12.

                font_weight : QFont.Weight, optional
                    Weight of the font (e.g., QFont.Weight.Bold). Default is QFont.Weight.Bold.

                parent : QWidget, optional
                    The parent widget in which the button will be placed. Default is None.

                Example Usage:
                --------------
                btn = FancyButton(
                    text="Click Me",
                    width=150,
                    height=50,
                    x=50,
                    y=100,
                    bg_color="#2196F3",
                    hover_color="#1976D2",
                    text_color="white",
                    border_radius=15,
                    border_color="#0D47A1",
                    border_width=3,
                    font_name="Verdana",
                    font_size=14,
                    font_weight=QFont.Weight.Bold,
                    parent=self
                )
                """
            super().__init__(text, parent)

            # Store params
            self.bg_color = bg_color
            self.hover_color = hover_color
            self.text_color = text_color
            self.border_radius = border_radius
            self.border_color = border_color
            self.border_width = border_width
            self.setFont(QFont(font_name, font_size, font_weight))
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.setMinimumSize(width, height)
            self.move(x, y)
            # Apply default style
            self.setStyleSheet(self.default_style())

        def enterEvent(self, event):
            self.setStyleSheet(self.hover_style())
            super().enterEvent(event)

        def leaveEvent(self, event):
            self.setStyleSheet(self.default_style())
            super().leaveEvent(event)

        def default_style(self):
            return f"""
                QPushButton {{
                    background-color: {self.bg_color};
                    color: {self.text_color};
                    border-radius: {self.border_radius}px;
                    border: {self.border_width}px solid {self.border_color};
                }}
            """

        def hover_style(self):
            return f"""
                QPushButton {{
                    background-color: {self.hover_color};
                    color: {self.text_color};
                    border-radius: {self.border_radius}px;
                    border: {self.border_width}px solid {self.border_color};
                }}
            """

    class Text(QLabel):
        """
        A customizable QLabel with enhanced styling, positioning, and text control.

        Features:
        - Custom font settings (name, size, weight).
        - Adjustable text and background color.
        - Padding and border-radius for a styled label.
        - Supports alignment and positioning within a parent widget.
        - Methods to update text and text color dynamically.

        Parameters:
        -----------
        text : str, optional
            The text displayed by the label. Default is "Text".

        font_name : str, optional
            Name of the font used for the text. Default is "Arial".

        font_size : int, optional
            Size of the font in points. Default is 14.

        x : int, optional
            Horizontal position of the label relative to the parent widget's top-left corner. Default is 0.

        y : int, optional
            Vertical position of the label relative to the parent widget's top-left corner. Default is 0.

        font_weight : QFont.Weight, optional
            Weight of the font (e.g., QFont.Weight.Normal or QFont.Weight.Bold). Default is QFont.Weight.Normal.

        text_color : str, optional
            Color of the text (CSS format). Default is "#FFFFFF".

        bg_color : str or None, optional
            Background color of the label (CSS format). If None, background is transparent. Default is None.

        padding : int, optional
            Padding inside the label in pixels. Default is 8.

        border_radius : int, optional
            Radius of the label's corners in pixels. Default is 8.

        alignment : Qt.AlignmentFlag, optional
            Text alignment inside the label. Default is Qt.AlignmentFlag.AlignCenter.

        parent : QWidget, optional
            Parent widget in which the label will be placed. Default is None.

        Example Usage:
        --------------
        lbl = Text(
            text="Hello World",
            font_name="Verdana",
            font_size=16,
            x=50,
            y=100,
            font_weight=QFont.Weight.Bold,
            text_color="#FFDD00",
            bg_color="#333333",
            padding=10,
            border_radius=12,
            alignment=Qt.AlignmentFlag.AlignLeft,
            parent=self
        )

        lbl.set_text("New Text")
        lbl.set_color("#00FF00")
        """

        def __init__(
            self,
            text="Text",    
            font_name="Arial",
            font_size=14,
            x=0,
            y=0,
            font_weight=QFont.Weight.Normal,
            text_color="#FFFFFF",
            bg_color=None,
            padding=8,
            border_radius=8,
            alignment=Qt.AlignmentFlag.AlignCenter,
            parent=None
        ):
            super().__init__(text, parent)

            self.setFont(QFont(font_name, font_size, font_weight))
            self.setAlignment(alignment)
            self.move(x, y)

            bg = "transparent" if bg_color is None else bg_color

            self.setStyleSheet(f"""
                QLabel {{
                    color: {text_color};
                    background-color: {bg};
                    padding: {padding}px;
                    border-radius: {border_radius}px;
                }}
            """)

        def set_text(self, text):
            self.setText(text)

        def set_color(self, color):
            self.setStyleSheet(self.styleSheet() + f"color: {color};")

    class Card(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.layout = VBox()
            self.setLayout(self.layout)
            self.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                background-color: #f9f9f9;
            }
            """)

        def addWidget(self, widget):
            self.layout.addWidget(widget)

    class InputField(QLineEdit):
        def __init__(
            self,
            placeholder="Enter text...",
            width=240,
            height=36,
            font_name="Arial",
            font_size=12,
            text_color="#FFFFFF",
            bg_color="#1E1E1E",
            border_color="#555555",
            focus_color="#00E5FF",
            border_radius=8,
            padding=8,
            parent=None
        ):
            super().__init__(parent)

            self.setPlaceholderText(placeholder)
            self.setFont(QFont(font_name, font_size))
            self.setMinimumSize(width, height)

            self.text_color = text_color
            self.bg_color = bg_color
            self.border_color = border_color
            self.focus_color = focus_color
            self.border_radius = border_radius
            self.padding = padding

            self.apply_style(focused=False)

        def apply_style(self, focused=False):
            border = self.focus_color if focused else self.border_color

            self.setStyleSheet(f"""
                QLineEdit {{
                    color: {self.text_color};
                    background-color: {self.bg_color};
                    border: 2px solid {border};
                    border-radius: {self.border_radius}px;
                    padding: {self.padding}px;
                }}
                QLineEdit::placeholder {{
                    color: #888888;
                }}
            """)

        def focusInEvent(self, event):
            self.apply_style(focused=True)
            super().focusInEvent(event)

        def focusOutEvent(self, event):
            self.apply_style(focused=False)
            super().focusOutEvent(event)

        def get_value(self):
            return self.text()

        def set_value(self, value):
            self.setText(value)
