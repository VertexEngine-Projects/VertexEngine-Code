from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import pyqtSignal
import sys

# -----------------------------
# Custom OptionButtonWidget
# -----------------------------
class OptionButtonWidget(QWidget):
    """Widget for Option buttons. Options by default is A, B and C.
    Usage:
    .. code-block :: python
        options_widget = OptionButtonWidget(["Option A", "Option B", "Option C"]) \n
        layout.addWidget(options_widget) \n
        def on_option_clicked(option): \n
            print(f"You clicked: {option}") \n

        options_widget.optionClicked.connect(on_option_clicked)
    """
    # Signal emits the clicked option text
    optionClicked = pyqtSignal(str)

    def __init__(self, options=None):
        super().__init__()
        options = options or ["A", "B", "C"]  # default options

        # Layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Create buttons
        self.buttons = []
        for opt in options:
            btn = QPushButton(opt)
            btn.setCheckable(True)  # allows toggle behavior
            btn.clicked.connect(lambda checked, o=opt: self._on_clicked(o))
            layout.addWidget(btn)
            self.buttons.append(btn)

    def _on_clicked(self, option):
        # Uncheck all other buttons
        for btn in self.buttons:
            if btn.text() != option:
                btn.setChecked(False)
        # Emit signal
        self.optionClicked.emit(option)

    # Optional: get currently selected option
    def selected_option(self):
        for btn in self.buttons:
            if btn.isChecked():
                return btn.text()
        return None

# -----------------------------
# Demo usage
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Option Button Demo")
    layout = QHBoxLayout()
    window.setLayout(layout)

    # Create option button widget
    options_widget = OptionButtonWidget(["Option A", "Option B", "Option C"])
    layout.addWidget(options_widget)

    # Connect the clicked signal
    def on_option_clicked(option):
        print(f"You clicked: {option}")

    options_widget.optionClicked.connect(on_option_clicked)

    window.show()
    sys.exit(app.exec())
