import pygame

class Widget:
    """
    Base class for all UI widgets.

    Provides core functionality such as positioning, visibility,
    parenting hierarchy, styling, and basic lifecycle methods.

    All UI elements should inherit from this class.

    Attributes:
        x (int): Local x position.
        y (int): Local y position.
        width (int): Widget width.
        height (int): Widget height.
        visible (bool): Whether widget is rendered.
        children (list[Widget]): Child widgets.
        parent (Widget | None): Parent widget.
        style (Style): Styling object.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.visible = True
        self.children = []
        self.parent = None

    def add_child(self, widget):
        widget.parent = self
        self.children.append(widget)

    def global_position(self):
        if self.parent:
            px, py = self.parent.global_position()
            return self.x + px, self.y + py
        return self.x, self.y

    def rect(self):
        gx, gy = self.global_position()
        return pygame.Rect(gx, gy, self.width, self.height)

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def handle_event(self, event):
        for child in self.children:
            child.handle_event(event)

class Button(Widget):
    """
    Clickable button widget.

    Supports hover, pressed states, and click callbacks.
    Uses Style for rendering appearance.

    Attributes:
        text (str): Button label.
        on_click (Callable | None): Callback when clicked.
        hovered (bool): Mouse hover state.
        pressed (bool): Mouse pressed state.
        font (pygame.Font): Text font.
    """

    def __init__(self, x, y, width, height, text="", on_click=None, style=None):
        super().__init__(x, y, width, height, style)

        self.text = text
        self.on_click = on_click

        self.hovered = False
        self.pressed = False

        self.font = pygame.font.SysFont(
            self.style.font_name,
            self.style.font_size
        )

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect().collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.hovered and self.on_click:
                self.on_click()
            self.pressed = False

    def draw(self, surface):
        if not self.visible:
            return

        color = self.style.bg_color
        if self.pressed:
            color = self.style.pressed_color
        elif self.hovered:
            color = self.style.hover_color

        rect = self.rect()

        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=self.style.border_radius
        )

        if self.style.border_width > 0:
            pygame.draw.rect(
                surface,
                self.style.border_color,
                rect,
                width=self.style.border_width,
                border_radius=self.style.border_radius
            )

        if self.text:
            text_surf = self.font.render(
                self.text,
                True,
                self.style.text_color
            )
            surface.blit(text_surf, text_surf.get_rect(center=rect.center))

class Slider(Widget):
    """
    Horizontal slider widget for selecting numeric values.

    Allows dragging a knob along a track to adjust a value
    between a minimum and maximum range.

    Attributes:
        min (float): Minimum value.
        max (float): Maximum value.
        value (float): Current value.
        on_change (Callable | None): Callback when value changes.
        dragging (bool): Whether slider is being dragged.
        knob_radius (int): Knob size.
    """

    def __init__(
        self,
        x,
        y,
        width,
        height=20,
        min_value=0,
        max_value=100,
        start_value=50,
        on_change=None,
        style=None,
    ):
        super().__init__(x, y, width, height, style)

        self.min = min_value
        self.max = max_value
        self.value = start_value
        self.on_change = on_change

        self.dragging = False
        self.knob_radius = height // 2 + 4

    def value_to_pos(self):
        """
        Converts current value to screen position.

        Returns:
            int: X coordinate of knob.
        """
        t = (self.value - self.min) / (self.max - self.min)
        return self.rect().x + int(t * self.width)

    def pos_to_value(self, px):
        """
        Converts mouse position to slider value.

        Args:
            px (int): Mouse x coordinate.

        Returns:
            float: Computed value.
        """
        t = (px - self.rect().x) / self.width
        t = max(0, min(1, t))
        return self.min + t * (self.max - self.min)

    def update(self):
        """Updates value while dragging."""
        if self.dragging:
            mx, _ = pygame.mouse.get_pos()
            self.value = self.pos_to_value(mx)

            if self.on_change:
                self.on_change(self.value)

    def handle_event(self, event):
        """Handles mouse dragging events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect().collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def draw(self, surface):
        """Renders slider track, fill, and knob."""
        if not self.visible:
            return

        rect = self.rect()

        pygame.draw.rect(surface, self.style.bg_color, rect, border_radius=self.style.border_radius)

        fill_rect = rect.copy()
        fill_rect.width = self.value_to_pos() - rect.x

        pygame.draw.rect(surface, self.style.hover_color, fill_rect, border_radius=self.style.border_radius)

        knob_x = self.value_to_pos()
        knob_y = rect.centery

        pygame.draw.circle(surface, self.style.pressed_color, (knob_x, knob_y), self.knob_radius)

class UIManager:
    """
    Manages all UI widgets.

    Responsible for updating, drawing, and forwarding
    input events to widgets.

    Attributes:
        widgets (list[Widget]): Registered widgets.
    """

    def __init__(self):
        self.widgets = []

    def add(self, widget):
        """
        Adds a widget to the manager.

        Args:
            widget (Widget): Widget to register.
        """
        self.widgets.append(widget)

    def update(self):
        """Updates all widgets."""
        for w in self.widgets:
            w.update()

    def draw(self, surface):
        """
        Draws all widgets.

        Args:
            surface (pygame.Surface): Target surface.
        """
        for w in self.widgets:
            w.draw(surface)

    def handle_event(self, event):
        """
        Forwards events to widgets.

        Args:
            event (pygame.Event): Input event.
        """
        for w in self.widgets:
            w.handle_event(event)

class Style:
    """
    Defines visual styling properties for UI widgets.

    A Style object can be shared across multiple widgets to create
    consistent themes. Widgets read styling values such as colors,
    font settings, borders, and padding from this class.

    Attributes:
        bg_color (tuple[int, int, int]): Background color.
        hover_color (tuple[int, int, int]): Color when widget is hovered.
        pressed_color (tuple[int, int, int]): Color when widget is pressed/active.
        border_color (tuple[int, int, int]): Border color.
        text_color (tuple[int, int, int]): Text color.
        border_radius (int): Corner roundness.
        border_width (int): Border thickness.
        font_name (str): Font family name.
        font_size (int): Font size.
        padding (int): Internal spacing.
    """
    def __init__(
        self,
        bg_color=(70, 70, 90),
        hover_color=(90, 90, 120),
        pressed_color=(120, 120, 160),
        border_color=(30, 30, 40),
        text_color=(255, 255, 255),
        border_radius=8,
        border_width=0,
        font_name="Arial",
        font_size=20,
        padding=4,
    ):
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_color = border_color
        self.text_color = text_color

        self.border_radius = border_radius
        self.border_width = border_width

        self.font_name = font_name
        self.font_size = font_size

        self.padding = padding
