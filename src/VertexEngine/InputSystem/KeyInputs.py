from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

KEY_MAP = {
    # Arrows
    "left": Qt.Key.Key_Left,
    "right": Qt.Key.Key_Right,
    "up": Qt.Key.Key_Up,
    "down": Qt.Key.Key_Down,

    # Actions
    "space": Qt.Key.Key_Space,
    "enter": Qt.Key.Key_Return,
    "escape": Qt.Key.Key_Escape,
    "tab": Qt.Key.Key_Tab,
    "shift": Qt.Key.Key_Shift,
    "ctrl": Qt.Key.Key_Control,
    "alt": Qt.Key.Key_Alt,
}

# Letters
for c in "abcdefghijklmnopqrstuvwxyz":
    KEY_MAP[c] = getattr(Qt.Key, f"Key_{c.upper()}")

# Numbers
for n in "0123456789":
    KEY_MAP[n] = getattr(Qt.Key, f"Key_{n}")

# Function keys
for i in range(1, 13):
    KEY_MAP[f"f{i}"] = getattr(Qt.Key, f"Key_F{i}")

# Basic punctuation keys
punctuation_map = {
    "`": "Backquote",
    "-": "Minus",
    "=": "Equal",
    "[": "BracketLeft",
    "]": "BracketRight",
    "\\": "Backslash",
    ";": "Semicolon",
    "'": "Apostrophe",
    ",": "Comma",
    ".": "Period",
    "/": "Slash",
    # Shifted versions
    "!": "Exclam",
    "@": "At",
    "#": "NumberSign",
    "$": "Dollar",
    "%": "Percent",
    "^": "AsciiCircum",
    "&": "Ampersand",
    "*": "Asterisk",
    "(": "ParenLeft",
    ")": "ParenRight",
    "_": "Underscore",
    "+": "Plus",
    "{": "BraceLeft",
    "}": "BraceRight",
    "|": "Bar",
    ":": "Colon",
    '"': "QuoteDbl",
    "<": "Less",
    ">": "Greater",
    "?": "Question"
}

for key, qt_name in punctuation_map.items():
    try:
        KEY_MAP[key] = getattr(Qt.Key, f"Key_{qt_name}")
    except AttributeError:
        # Some symbols might not exist in PyQt6's Qt.Key
        pass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

KEY_MAP = {
    # Arrows
    "left": Qt.Key.Key_Left,
    "right": Qt.Key.Key_Right,
    "up": Qt.Key.Key_Up,
    "down": Qt.Key.Key_Down,

    # Actions
    "space": Qt.Key.Key_Space,
    "enter": Qt.Key.Key_Return,
    "escape": Qt.Key.Key_Escape,
    "tab": Qt.Key.Key_Tab,
    "shift": Qt.Key.Key_Shift,
    "ctrl": Qt.Key.Key_Control,
    "alt": Qt.Key.Key_Alt,
}

# Letters
for c in "abcdefghijklmnopqrstuvwxyz":
    KEY_MAP[c] = getattr(Qt.Key, f"Key_{c.upper()}")

# Numbers
for n in "0123456789":
    KEY_MAP[n] = getattr(Qt.Key, f"Key_{n}")

# Function keys
for i in range(1, 13):
    KEY_MAP[f"f{i}"] = getattr(Qt.Key, f"Key_F{i}")

# Basic punctuation keys
punctuation_map = {
    "`": "Backquote",
    "-": "Minus",
    "=": "Equal",
    "[": "BracketLeft",
    "]": "BracketRight",
    "\\": "Backslash",
    ";": "Semicolon",
    "'": "Apostrophe",
    ",": "Comma",
    ".": "Period",
    "/": "Slash",
    # Shifted versions
    "!": "Exclam",
    "@": "At",
    "#": "NumberSign",
    "$": "Dollar",
    "%": "Percent",
    "^": "AsciiCircum",
    "&": "Ampersand",
    "*": "Asterisk",
    "(": "ParenLeft",
    ")": "ParenRight",
    "_": "Underscore",
    "+": "Plus",
    "{": "BraceLeft",
    "}": "BraceRight",
    "|": "Bar",
    ":": "Colon",
    '"': "QuoteDbl",
    "<": "Less",
    ">": "Greater",
    "?": "Question"
}

for key, qt_name in punctuation_map.items():
    try:
        KEY_MAP[key] = getattr(Qt.Key, f"Key_{qt_name}")
    except AttributeError:
        # Some symbols might not exist in PyQt6's Qt.Key
        pass

class Input:
    _pressed = set()
    _just_pressed = set()
    _just_released = set()

    _bindings = {}  # action_name -> set of qt_keys

    @classmethod
    def input_update(cls):
        cls._just_pressed.clear()
        cls._just_released.clear()

    @classmethod
    def bind(cls, action, key):
        """Bind an action name to a key."""
        qt_key = KEY_MAP.get(key, key)
        cls._bindings.setdefault(action, set()).add(qt_key)

    @classmethod
    def unbind(cls, action, key=None):
        """Remove a key from an action, or remove the action entirely."""
        if action not in cls._bindings:
            return

        if key is None:
            del cls._bindings[action]
        else:
            qt_key = KEY_MAP.get(key, key)
            cls._bindings[action].discard(qt_key)

    @classmethod
    def _key_down(cls, key):
        qt_key = KEY_MAP.get(key, key)
        if qt_key not in cls._pressed:
            cls._just_pressed.add(qt_key)
        cls._pressed.add(qt_key)

    @classmethod
    def _key_up(cls, key):
        qt_key = KEY_MAP.get(key, key)
        if qt_key in cls._pressed:
            cls._just_released.add(qt_key)
        cls._pressed.discard(qt_key)

    # === Direct Key API ===
    @classmethod
    def is_pressed(cls, key):
        return KEY_MAP[key] in cls._pressed

    @classmethod
    def is_just_pressed(cls, key):
        return KEY_MAP[key] in cls._just_pressed

    @classmethod
    def is_released(cls, key):
        return KEY_MAP[key] in cls._just_released

    # === Action API ===
    @classmethod
    def is_action_pressed(cls, action):
        return any(k in cls._pressed for k in cls._bindings.get(action, []))

    @classmethod
    def is_action_just_pressed(cls, action):
        return any(k in cls._just_pressed for k in cls._bindings.get(action, []))

    @classmethod
    def is_action_released(cls, action):
        return any(k in cls._just_released for k in cls._bindings.get(action, []))

    class VShortcut(QShortcut):
        def __init__(self, key, parent, callback):
            super().__init__(QKeySequence(key), parent)
            self.activated.connect(callback)
            