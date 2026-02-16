import pygame
from PyQt6.QtGui import QImage
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
        self._scaled_cache = {}  # cache for scaled versions

    def load_image(self, name: str, path: str):
        """Load an image with `path` and `name`, `name` can be thought as a variable that represents `path`.
        It can be acessed by any other `AssetManager` function.
        """
        if name in self.images:
            return self.images[name]

        try:
            surface = pygame.image.load(path).convert_alpha()
            self.images[name] = surface
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

        if not img:
            print(f"[Warning] Image '{name}' not loaded!")
            return

        # If no scaling requested → draw normally
        if size is None:
            target_surface.blit(img, pos)
            return

        # Use cache key
        cache_key = (name, size)

        # Check if scaled version exists
        if cache_key not in self._scaled_cache:
            scaled_img = pygame.transform.smoothscale(img, size)
            self._scaled_cache[cache_key] = scaled_img
        else:
            scaled_img = self._scaled_cache[cache_key]

        target_surface.blit(scaled_img, pos)
