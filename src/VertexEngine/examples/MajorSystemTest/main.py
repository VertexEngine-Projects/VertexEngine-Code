from VertexEngine import GameEngine, AssetManager, Scene, AudioManager, VertexScreen
from VertexEngine.Vertex import App
from VertexEngine.VertexWidgets.PygameVWidgets import Button, UIManager
from VertexEngine.InputSystem.KeyInputs import Input
from pathlib import Path

# 1. Get the directory where this script file lives
script_dir = Path(__file__).resolve().parent

class Player():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 5

    def update(self, input):
        if input.is_pressed("w"):
            self.y -= self.speed
        if input.is_pressed("s"):
            self.y += self.speed
        if input.is_pressed("a"):
            self.x -= self.speed
        if input.is_pressed("d"):
            self.x += self.speed
        if input.is_pressed("up"):
            self.h -= 1
        if input.is_pressed("down"):
            self.h += 1
        if input.is_pressed("left"):
            self.w -= 1
        if input.is_pressed("right"):
            self.w += 1
        if input.is_pressed("r"):
            self.h = 50
            self.w = 50

class Main(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.ui = UIManager()
        self.engine = engine
        self.drawer = VertexScreen.Draw()
        self.player = Player(400, 300, 50, 50)
        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.target_audio = str(script_dir / "universfield-ui-button-click-147358.mp3")
        self.target_image = str(script_dir / "Wangi.png")
        self.asset_manager.load_image("logo", self.target_image)
        self.audio_manager.load_sound("click", self.target_audio)
        self.button = Button(300, 370, 200, 50, "Click Me", lambda: self.click())
        self.switch = Button(300, 450, 200, 50, "Switch Scene", lambda: self.engine.scene_manager.set_scene(Side(self.engine)))
        self.ui.add(self.button)
        self.ui.add(self.switch)

    def update(self):
        # Update game logic here
        self.ui.update()
        self.player.update(Input())
    def draw(self, surface):
        self.drawer.rect(surface, (255, 0, 0), (self.player.x, self.player.y, self.player.w, self.player.h))
        self.asset_manager.draw(surface, "logo", (-100, 0), (1000, 500))
        self.ui.draw(surface)
    def handle_event(self, event):
        self.ui.handle_event(event)

    def click(self):
        self.audio_manager.play_sound("click")
        print("Button clicked!")

class Side(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.ui = UIManager()
        self.engine = engine
        self.asset_manager = AssetManager()
        self.screen1 = VertexScreen()
        self.target_image = str(script_dir / "Wangi.png")
        self.asset_manager.load_image("logo", self.target_image)
        self.switch = Button(300, 450, 200, 50, "Switch Scene", lambda: self.engine.scene_manager.set_scene(Main(self.engine)))
        self.ui.add(self.switch)

    def update(self):
        # Update game logic here
        self.ui.update()

    def draw(self, surface):
        self.ui.draw(surface)
        font = self.screen1.Font(None, 50)
        font2 = self.screen1.Font(None, 25)
        font.draw(surface, "This is the second scene!", (200, 200), (255, 255, 255))
        font2.draw(surface, "Press the button to go back. AERIS IS UGLY!!!!!!!!!!!!!!!", (175, 300), (255, 255, 255))

    def handle_event(self, event):
        self.ui.handle_event(event)

if __name__ == "__main__":
    app = App()
    engine = GameEngine(color=(0, 0, 0))
    engine.scene_manager.set_scene(Main(engine))
    engine.setWindowTitle("Vertex Engine Example")
    engine.show()

    app.run()