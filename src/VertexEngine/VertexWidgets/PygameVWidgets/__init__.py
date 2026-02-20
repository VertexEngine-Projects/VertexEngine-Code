import pygame

class Style:
    """
    Defines visual styling for widgets.

    Attributes
    ----------
    bg_color : tuple
        Background color.
    hover_color : tuple
        Color when mouse is hovering.
    active_color : tuple
        Color when pressed/active.
    border_color : tuple
        Border color.
    text_color : tuple
        Text color.
    border_width : int
        Width of border.
    padding : int
        Inner padding.
    font_size : int
        Font size.
    """
    def __init__(
        self,
        bg_color=(200, 200, 200),
        hover_color=(230, 230, 230),
        active_color=(180, 180, 180),
        border_color=(50, 50, 50),
        text_color=(0, 0, 0),
        border_width=2,
        padding=6,
        font_size=24,
    ):
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.border_color = border_color
        self.text_color = text_color
        self.border_width = border_width
        self.padding = padding
        self.font_size = font_size

class Widget:
    """
    Base class for all UI widgets.

    Parameters
    ----------
    x : int
        X position.
    y : int
        Y position.
    width : int
        Width of widget.
    height : int
        Height of widget.
    style : Style, optional
        Visual style configuration.
    visible : bool
        Whether widget is visible.
    enabled : bool
        Whether widget is interactive.
    """

    def __init__(self, x, y, width, height, style=None, visible=True, enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.style = style or Style()
        self.visible = visible
        self.enabled = enabled

        self.hovered = False
        self.active = False

    def update(self):
        """Update widget logic."""
        pass

    def draw(self, surface):
        """Draw widget."""
        pass

    def handle_event(self, event):
        """Handle pygame event."""
        pass

    def contains(self, pos):
        """Check if position is inside widget."""
        return self.rect.collidepoint(pos)
    
class Button(Widget):
    """
    Clickable button widget.

    Parameters
    ----------
    text : str
        Button label.
    x, y : int
        Position.
    width, height : int
        Size.
    callback : callable, optional
        Function to call on click.
    style : Style, optional
        Visual style.
    toggle : bool
        Whether button acts as toggle.
    """

    def __init__(
        self,
        text,
        x,
        y,
        width=200,
        height=60,
        callback=None,
        style=None,
        toggle=False,
    ):
        super().__init__(x, y, width, height, style)
        self.text = text
        self.callback = callback
        self.toggle = toggle
        self.toggled = False

        self.font = pygame.font.SysFont(None, self.style.font_size)

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.contains(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.active = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.active and self.hovered:
                if self.toggle:
                    self.toggled = not self.toggled
                if self.callback:
                    self.callback()
            self.active = False

    def draw(self, surface):
        if not self.visible:
            return

        color = self.style.bg_color

        if self.hovered:
            color = self.style.hover_color
        if self.active or self.toggled:
            color = self.style.active_color

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.style.border_color, self.rect, self.style.border_width)

        text_surface = self.font.render(self.text, True, self.style.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Slider(Widget):
    """
    Horizontal slider widget.

    Parameters
    ----------
    x, y : int
        Position.
    width : int
        Slider width.
    min_val : float
        Minimum value.
    max_val : float
        Maximum value.
    start_val : float
        Initial value.
    on_change : callable, optional
        Callback when value changes.
    """

    def __init__(
        self,
        x,
        y,
        width=300,
        min_val=0,
        max_val=100,
        start_val=None,
        style=None,
        on_change=None,
    ):
        super().__init__(x, y, width, 20, style)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val if start_val is not None else (min_val + max_val) / 2
        self.on_change = on_change

        self.dragging = False
        self.knob_radius = 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.contains(event.pos):
            self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            rel_x = max(0, min(self.rect.width, rel_x))
            ratio = rel_x / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

            if self.on_change:
                self.on_change(self.value)

    def draw(self, surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, self.style.bg_color, self.rect)

        knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        pygame.draw.circle(surface, self.style.active_color, (int(knob_x), self.rect.centery), self.knob_radius)

class UIManager:
    """
    Manages all widgets.

    Methods
    -------
    add(widget)
        Add widget.
    remove(widget)
        Remove widget.
    handle_event(event)
        Dispatch event.
    update()
        Update all widgets.
    draw(surface)
        Draw all widgets.
    """

    def __init__(self):
        self.widgets = []

    def add(self, widget):
        self.widgets.append(widget)

    def remove(self, widget):
        self.widgets.remove(widget)

    def handle_event(self, event):
        for w in self.widgets:
            w.handle_event(event)

    def update(self):
        for w in self.widgets:
            w.update()

    def draw(self, surface):
        for w in self.widgets:
            w.draw(surface)
