from VertexEngine import GameEngine, Scene, VertexScreen
from VertexEngine.VertexWidgets.PygameVWidgets import *
from VertexEngine.Vertex import App
class Main(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.ui = UIManager()
        self.engine = engine
        self.style1 = Style((255, 255, 255), (0, 255, 0), (0, 100, 0), text_color=(0, 0, 0), font_size=24)
        self.slider = Slider(300, 200, 200, 20)
        self.button1 = Button(300, 300, 100, 50, text="Button 1", on_click=lambda: self.switch())
        self.slider.style = self.style1
        self.ui.add(self.slider)
        self.ui.add(self.button1)
        self.ui.update()

    def draw(self, surface):
        self.ui.draw(surface)
        font = VertexScreen.Font(None, 36)
        header = VertexScreen.Font(None, 48)
        header.draw(surface, "Pygame Widgets Test", (25, 25), (255, 255, 255))
        font.draw(surface, "Slider Test", (300, 150), (255, 255, 255))
        font.draw(surface, f"Value: {self.slider.value:.2f}", (300, 250), (255, 255, 255))
        font.draw(surface, "Button Test", (300, 375), (255, 255, 255))

    def update(self):
        self.ui.update()

    def handle_event(self, event):
        self.ui.handle_event(event)

    def switch(self):
        self.engine.scene_manager.set_scene(Side(self.engine))

class Side(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine = engine
        self.ui = UIManager()
        self.style2 = Style((255, 255, 255), (255, 0, 0), (100, 0, 0), text_color=(0, 0, 0), font_size=24)
        self.button2 = Button(300, 300, 100, 50, text="Back", on_click=lambda: self.switch_back())
        self.button2.style = self.style2
        self.ui.add(self.button2)
        self.ui.update()

    def draw(self, surface):
        self.ui.draw(surface)
        font = VertexScreen.Font(None, 36)
        header = VertexScreen.Font(None, 48)
        header.draw(surface, "Side Scene", (25, 25), (255, 255, 255))
        font.draw(surface, "This is the side scene.", (300, 150), (255, 255, 255))

    def update(self):
        self.ui.update()

    def handle_event(self, event):
        self.ui.handle_event(event)

    def switch_back(self):
        self.engine.scene_manager.set_scene(Main(self.engine))
if __name__ == "__main__":
    app = App()
    engine = GameEngine(color=(0, 0, 0))
    engine.setWindowTitle("Pygame Widgets Test")
    engine.show()

    scene = Main(engine)
    engine.scene_manager.set_scene(scene)
    app.exec()