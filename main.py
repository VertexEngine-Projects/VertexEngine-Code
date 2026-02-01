from VertexEngine.engine import GameEngine
from VertexEngine import VertexScreen
from VertexEngine.scenes import Scene
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication


class Main(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.width = engine.width
        self.height = engine.height

    def update(self):
        pass

    def draw(self, surface):
        VertexScreen.Draw.rect(
            VertexScreen.Draw,
            surface,
            (0, 255, 0),
            (-570, 350, 5000, 500),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = GameEngine(fps=60, width=1920, height=1080)
    engine.setWindowTitle("Template")
    engine.show()

    main_scene = Main(engine)
    engine.scene_manager.set_scene(main_scene)

    app.exec()
