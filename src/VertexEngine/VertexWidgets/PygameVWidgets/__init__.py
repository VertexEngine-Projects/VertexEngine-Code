import pygame


# =========================================================
# STYLE
# =========================================================
class Style:
    """
    Defines visual styling properties for UI widgets.

    A Style object can be shared across multiple widgets to create
    consistent themes.

    Attributes:
        bg_color (tuple[int,int,int]): Base background color.
        hover_color (tuple[int,int,int]): Hover state color.
        pressed_color (tuple[int,int,int]): Active/pressed color.
        border_color (tuple[int,int,int]): Border color.
        text_color (tuple[int,int,int]): Text color.
        border_radius (int): Rounded corner radius.
        border_width (int): Border thickness.
        font_name (str): Font family name.
        font_size (int): Font size.
        padding (int): Internal padding.
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


# =========================================================
# BASE WIDGET
# =========================================================
class Widget:
    """
    Base class for all UI widgets.

    Handles positioning, hierarchy, and stable frame caching.

    IMPORTANT:
    Rect is cached per frame to avoid input mismatch bugs.

    Attributes:
        x, y (int): Local position.
        width, height (int): Size.
        visible (bool): Render toggle.
        parent (Widget|None): Parent widget.
        children (list[Widget]): Child widgets.
        style (Style): Visual style.
        _rect (pygame.Rect): Cached screen-space rect.
    """

    def __init__(self, x, y, width, height, style=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.visible = True
        self.parent = None
        self.children = []
        self.style = style or Style()

        self._rect = pygame.Rect(x, y, width, height)

    def add_child(self, widget):
        """Adds a child widget."""
        widget.parent = self
        self.children.append(widget)

    def global_position(self):
        """Returns global screen position including parent offsets."""
        if self.parent:
            px, py = self.parent.global_position()
            return self.x + px, self.y + py
        return self.x, self.y

    def update_rect(self):
        """
        Updates cached rect (MUST be called once per frame).
        """
        gx, gy = self.global_position()
        self._rect = pygame.Rect(gx, gy, self.width, self.height)

    def rect(self):
        """Returns cached rect (frame-stable)."""
        return self._rect

    def update(self):
        """Override in subclasses."""
        for c in self.children:
            c.update()

    def draw(self, surface):
        """Override in subclasses."""
        for c in self.children:
            c.draw(surface)

    def handle_event(self, event):
        """Forwards events to children."""
        for c in self.children:
            c.handle_event(event)


# =========================================================
# BUTTON
# =========================================================
class Button(Widget):
    """
    Clickable UI button with hover + press states.

    Attributes:
        text (str): Label text.
        on_click (callable): Click callback.
        hovered (bool): Hover state.
        pressed (bool): Press state.
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
        """Updates hover state."""
        mouse = pygame.mouse.get_pos()
        self.hovered = self.rect().collidepoint(mouse)

    def handle_event(self, event):
        """Handles click input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect().collidepoint(event.pos):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect().collidepoint(event.pos):
                if self.on_click:
                    self.on_click()

            self.pressed = False

    def draw(self, surface):
        """Renders button."""
        if not self.visible:
            return

        color = self.style.bg_color
        if self.pressed:
            color = self.style.pressed_color
        elif self.hovered:
            color = self.style.hover_color

        rect = self.rect()

        pygame.draw.rect(surface, color, rect, border_radius=self.style.border_radius)

        if self.text:
            text = self.font.render(self.text, True, self.style.text_color)
            surface.blit(text, text.get_rect(center=rect.center))


# =========================================================
# SLIDER
# =========================================================
class Slider(Widget):
    """
    Horizontal numeric slider.

    Fully event-driven + rect-stable design.

    Attributes:
        min, max (float): Range.
        value (float): Current value.
        dragging (bool): Drag state.
        on_change (callable): Callback.
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

    # -----------------------------
    # VALUE MAPPING
    # -----------------------------
    def value_to_pos(self):
        rect = self.rect()
        if self.max == self.min:
            return rect.x

        t = (self.value - self.min) / (self.max - self.min)
        return rect.x + int(t * rect.width)

    def pos_to_value(self, px):
        rect = self.rect()
        if rect.width == 0:
            return self.min

        t = (px - rect.x) / rect.width
        t = max(0, min(1, t))

        return self.min + t * (self.max - self.min)

    # -----------------------------
    # EVENTS
    # -----------------------------
    def handle_event(self, event):
        rect = self.rect()
        print("SLIDER GOT:", event.type)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.value = self.pos_to_value(event.pos[0])
                if self.on_change:
                    self.on_change(self.value)

    # -----------------------------
    # DRAW
    # -----------------------------
    def draw(self, surface):
        if not self.visible:
            return

        rect = self.rect()

        # track
        pygame.draw.rect(
            surface,
            self.style.bg_color,
            rect,
            border_radius=self.style.border_radius
        )

        # fill
        fill_width = self.value_to_pos() - rect.x
        fill_width = max(0, min(fill_width, rect.width))

        pygame.draw.rect(
            surface,
            self.style.hover_color,
            pygame.Rect(rect.x, rect.y, fill_width, rect.height),
            border_radius=self.style.border_radius
        )

        # knob
        pygame.draw.circle(
            surface,
            self.style.pressed_color,
            (self.value_to_pos(), rect.centery),
            self.knob_radius
        )


# =========================================================
# UI MANAGER
# =========================================================
class UIManager:
    """
    Handles all widgets in a scene.

    IMPORTANT:
    Must call update_rect() every frame BEFORE update().
    """

    def __init__(self):
        self.widgets = []

    def add(self, widget):
        self.widgets.append(widget)

    def update(self):
        for w in self.widgets:
            w.update_rect()
            w.update()

    def draw(self, surface):
        for w in self.widgets:
            w.draw(surface)

    def handle_event(self, event):
        for w in self.widgets:
            w.handle_event(event)