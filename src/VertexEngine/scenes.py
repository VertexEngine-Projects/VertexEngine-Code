# scenes/scene.py
from .Vertex import VWidget

class Scene(VWidget):
    """
    Base class for all scenes. Inherit from this and implement on_enter, on_exit, update, and draw.
    Scenes are managed by the SceneManager and can be switched dynamically.
    Each scene receives a reference to the engine, allowing access to shared resources.
    
    Example usage:

    ``` python
    class MainMenuScene(Scene):
        def on_enter(self):
            print("Entered Main Menu")

        def update(self):
            # Handle menu logic
            pass

        def draw(self, surface):
            # Draw menu items
            pass
            
    # In your engine setup:
    engine.scene_manager.set_scene(MainMenuScene(engine)) # Switch to the main menu scene, you can also use a variable to store the scene instance and reuse it later.
    ```
    """
    def __init__(self, engine):
        super().__init__(engine)  # parent = engine widget
        self.engine = engine

        # Optional: scenes can receive focus
        self.setFocusPolicy(engine.focusPolicy())

    def on_enter(self):
        """Called when the scene becomes active"""
        self.setFocus()

    def on_exit(self):
        """Called when the scene is removed"""
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# scenes/scene_manager.py
class SceneManager:
    def __init__(self):
        self.current_scene = None

    def set_scene(self, scene):
        if self.current_scene:
            self.current_scene.on_exit()
            self.current_scene.hide()

        self.current_scene = scene
        self.current_scene.show()
        self.current_scene.on_enter()

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, surface):
        if self.current_scene:
            self.current_scene.draw(surface)

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)