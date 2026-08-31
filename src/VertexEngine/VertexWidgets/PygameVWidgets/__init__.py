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

    _STYLE_ATTRS = (
        "bg_color",
        "hover_color",
        "pressed_color",
        "border_color",
        "text_color",
        "border_radius",
        "border_width",
        "font_name",
        "font_size",
        "padding",
    )

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

    @classmethod
    def coerce(cls, style=None):
        """Return a Style instance, even when a style-like object is passed."""
        if style is None:
            return cls()
        if isinstance(style, cls):
            return style

        normalized = cls()
        for attr in cls._STYLE_ATTRS:
            if hasattr(style, attr):
                setattr(normalized, attr, getattr(style, attr))
        return normalized


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
        self.style = Style.coerce(style)

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
        image (pygame.Surface | str | None): Optional button image.
    """

    def __init__(self, x, y, width, height, text="", on_click=None, style=None, image=None):
        super().__init__(x, y, width, height, style)
        self.text = text
        self.on_click = on_click
        self.hovered = False
        self.pressed = False
        self.image = self._load_image(image)

        self.font = pygame.font.SysFont(
            self.style.font_name,
            self.style.font_size
        )

    @staticmethod
    def _load_image(image):
        if image is None:
            return None
        if isinstance(image, str):
            return pygame.image.load(image)
        if isinstance(image, pygame.Surface):
            return image
        return None

    def _tint_surface(self, image, tint_color, alpha=120):
        if image is None:
            return None

        tinted = image.copy()
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        overlay.fill((tint_color[0], tint_color[1], tint_color[2], alpha))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted

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

        rect = self.rect()

        if self.image:
            image = pygame.transform.smoothscale(self.image, rect.size)
            tint_color = None
            if self.pressed:
                tint_color = self.style.pressed_color
            elif self.hovered:
                tint_color = self.style.hover_color

            if tint_color is not None:
                image = self._tint_surface(image, tint_color, alpha=150)

            surface.blit(image, rect.topleft)
        else:
            color = self.style.bg_color
            if self.pressed:
                color = self.style.pressed_color
            elif self.hovered:
                color = self.style.hover_color

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
        debug=True
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

class Card(Widget):
    """A drawable container for grouping related widgets."""

    def __init__(self, x, y, width, height, style=None):
        super().__init__(x, y, width, height, style)

    def update_rect(self):
        """Update this card and all child rects in screen coordinates."""
        super().update_rect()
        for child in self.children:
            child.update_rect()

    def draw(self, surface):
        if not self.visible:
            return

        rect = self.rect()
        pygame.draw.rect(
            surface,
            self.style.bg_color,
            rect,
            border_radius=self.style.border_radius
        )
        if self.style.border_width:
            pygame.draw.rect(
                surface,
                self.style.border_color,
                rect,
                width=self.style.border_width,
                border_radius=self.style.border_radius
            )

        for child in self.children:
            child.draw(surface)


class ProgressBar(Widget):
    """Displays progress between a configurable minimum and maximum."""

    def __init__(
        self,
        x,
        y,
        width,
        height=20,
        min_value=0,
        max_value=100,
        value=0,
        on_change=None,
        style=None
    ):
        super().__init__(x, y, width, height, style)
        if max_value < min_value:
            raise ValueError("max_value must be greater than or equal to min_value")

        self.min = min_value
        self.max = max_value
        self.value = max(self.min, min(self.max, value))
        self.on_change = on_change

    def set_value(self, value):
        """Set the value, clamp it to the range, and notify on changes."""
        new_value = max(self.min, min(self.max, value))
        if new_value != self.value:
            self.value = new_value
            if self.on_change:
                self.on_change(self.value)

    def draw(self, surface):
        if not self.visible:
            return

        rect = self.rect()
        pygame.draw.rect(
            surface,
            self.style.bg_color,
            rect,
            border_radius=self.style.border_radius
        )

        progress = 0
        if self.max != self.min:
            progress = (self.value - self.min) / (self.max - self.min)
        fill_width = int(rect.width * progress)
        if fill_width:
            pygame.draw.rect(
                surface,
                self.style.hover_color,
                pygame.Rect(rect.x, rect.y, fill_width, rect.height),
                border_radius=self.style.border_radius
            )

        if self.style.border_width:
            pygame.draw.rect(
                surface,
                self.style.border_color,
                rect,
                width=self.style.border_width,
                border_radius=self.style.border_radius
            )


class Toggle(Widget):
    """A clickable two-state control."""

    def __init__(self, x, y, width=60, height=30, value=False, on_toggle=None, style=None):
        super().__init__(x, y, width, height, style)
        self.value = bool(value)
        self.on_toggle = on_toggle
        self.hovered = False
        self.pressed = False

    @property
    def is_on(self):
        return self.value

    def set_value(self, value):
        """Set the state and notify only when it changes."""
        new_value = bool(value)
        if new_value != self.value:
            self.value = new_value
            if self.on_toggle:
                self.on_toggle(self.value)

    def update(self):
        self.hovered = self.rect().collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect().collidepoint(event.pos):
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect().collidepoint(event.pos):
                self.set_value(not self.value)
            self.pressed = False

    def draw(self, surface):
        if not self.visible:
            return

        rect = self.rect()
        color = self.style.pressed_color if self.value else self.style.bg_color
        if self.hovered and not self.value:
            color = self.style.hover_color
        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=min(self.style.border_radius, rect.height // 2)
        )
        if self.style.border_width:
            pygame.draw.rect(
                surface,
                self.style.border_color,
                rect,
                width=self.style.border_width,
                border_radius=min(self.style.border_radius, rect.height // 2)
            )

        knob_radius = max(1, rect.height // 2 - self.style.padding)
        knob_x = rect.right - rect.height // 2 if self.value else rect.left + rect.height // 2
        pygame.draw.circle(surface, self.style.text_color, (knob_x, rect.centery), knob_radius)

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