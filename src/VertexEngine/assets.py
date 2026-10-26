import pygame
from PySide6.QtGui import QImage
import typing_extensions as typing

@typing.deprecated('This is not a public API, use AssetManager pls :D')
class QtRenderer:
    def create_texture(self, image_asset):
        surf = image_asset.surface
        width, height = surf.get_size()

        # Ensure predictable format
        surf = surf.convert_alpha() if surf.get_alpha() else surf.convert()

        # pygame → raw RGBA
        pixel_data = pygame.image.tostring(surf, "RGBA", False)

        # Create REAL QImage (no OpenGL required)
        qimage = QImage(
            pixel_data,
            width,
            height,
            QImage.Format.Format_RGBA8888
        )

        # IMPORTANT: deep copy so data survives after function returns
        qimage = qimage.copy()

        return Texture(qimage)

@typing.deprecated('This is not a public API, use AssetManager pls :D')
class Texture:
    def __init__(self, qimage: QImage):
        self.image = qimage
        self.width = qimage.width()
        self.height = qimage.height()

    def __repr__(self):
        return f"<Texture {self.width}x{self.height} (QImage)>"

@typing.deprecated('This is not a public API, use AssetManager pls :D')
class ImageAsset:
    def __init__(self, surface):
        self.surface = surface  # pygame.Surface

class AssetManager:
    """The `AssetManager` is a class to draw and load images and assets of any kind."""
    def __init__(self):
        self.images = {}
        self.spritesheets = {}
        self._scaled_cache = {}  # cache for scaled versions

    def load_image(self, name: str, path: str):
        """Load an image with `path` and `name`, `name` can be thought as a variable that represents `path`.
        It can be acessed by any other `AssetManager` function.
        """
        if name in self.images:
            return self.images[name]

        try:
            surface = pygame.image.load(path)
            self.images[name] = surface
            self._scaled_cache = {
                key: value for key, value in self._scaled_cache.items()
                if key[0] != name
            }
            return surface

        except FileNotFoundError:
            print(f"[Warning] Image '{path}' not found!")
            return None

    def get_image(self, name: str):
        return self.images.get(name)

    def draw(self, target_surface, name, pos=(0, 0), size=None):
        """
        Draw image.
        size = (width, height) to rescale.
        If size is None, original size is used.
        target_surface is the surface to draw the actual image
        pos is where to draw it in coordinates
        name is the identity of the image. make sure it's loaded in by `load_image`
        """
        img = self.images.get(name)

        if img is None:
            print(f"[Warning] Image '{name}' not loaded!")
            return

        # If no scaling requested → draw normally
        if size is None:
            target_surface.blit(img, pos)
            return

        # Use cache key
        size = tuple(size)
        cache_key = (name, size)

        # Check if scaled version exists
        if cache_key not in self._scaled_cache:
            scaled_img = pygame.transform.smoothscale(img, size)
            self._scaled_cache[cache_key] = scaled_img
        else:
            scaled_img = self._scaled_cache[cache_key]

        target_surface.blit(scaled_img, pos)

    def load_spritesheet(self, name: str, path: str, frame_size):
        """Load a spritesheet and split it into equally sized frames.

        ``frame_size`` is ``(width, height)``. Incomplete frames at the
        right or bottom edges are ignored.
        """
        if name in self.spritesheets:
            return self.spritesheets[name]

        frame_width, frame_height = (int(value) for value in frame_size)
        if frame_width <= 0 or frame_height <= 0:
            raise ValueError("frame_size values must be greater than zero")

        try:
            sheet = pygame.image.load(path)
        except FileNotFoundError:
            print(f"[Warning] Spritesheet '{path}' not found!")
            return None

        sheet_width, sheet_height = sheet.get_size()
        frames = [
            sheet.subsurface((x, y, frame_width, frame_height)).copy()
            for y in range(0, sheet_height - frame_height + 1, frame_height)
            for x in range(0, sheet_width - frame_width + 1, frame_width)
        ]
        self.spritesheets[name] = frames
        return frames

    def get_sprite(self, name: str, index: int):
        """Return one frame from a loaded spritesheet."""
        spritesheet = self.spritesheets.get(name)
        if spritesheet is None:
            print(f"[Warning] Spritesheet '{name}' not loaded!")
            return None
        return spritesheet[index]

    def draw_sprite(self, target_surface, name: str, index: int,
                    pos=(0, 0), size=None):
        """Draw one frame from a loaded spritesheet."""
        sprite = self.get_sprite(name, index)
        if sprite is None:
            return

        if size is not None:
            sprite = pygame.transform.smoothscale(sprite, tuple(size))
        target_surface.blit(sprite, pos)
