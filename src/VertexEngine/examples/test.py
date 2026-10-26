from VertexEngine.InputSystem.Events import ButtonEvents
from VertexEngine import VertexUI
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
import random
Buttons = ButtonEvents()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Button Demo')
window.resize(300, 200)

layout = QVBoxLayout()

label = VertexUI.Text('Click a Button', font_size=32, font_weight=QFont.Weight.Bold)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

btn_hello = VertexUI.FancyButton("Hello")
btn_random = VertexUI.FancyButton("Random")
btn_clear = VertexUI.FancyButton("Clear")

layout.addWidget(label)
layout.addWidget(btn_hello)
layout.addWidget(btn_random)
layout.addWidget(btn_clear)

# ---------------- Actions ----------------
def say_hello():
    label.setText("Hello 👋")

def random_text():
    messages = [
        "VertexEngine 🔥",
        "Buttons clicked 😄",
        "PySide6 is clean ✨",
        "Event system FTW 🎮",
        "Random works 🎲"
    ]
    label.setText(random.choice(messages))

def clear_text():
    label.setText("Click a button")

# ---------------- Bind Events ----------------
Buttons.on_click(btn_hello, say_hello)
Buttons.on_click(btn_random, random_text)
Buttons.on_click(btn_clear, clear_text)

window.setLayout(layout)

window.show()
sys.exit(app.exec())
