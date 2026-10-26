import pygame

from VertexEngine import AssetManager


def test_load_spritesheet_splits_frames(monkeypatch):
    sheet = pygame.Surface((20, 10), pygame.SRCALPHA)
    monkeypatch.setattr(pygame.image, "load", lambda path: sheet)
    manager = AssetManager()

    frames = manager.load_spritesheet("player", "player.png", (10, 10))

    assert len(frames) == 2
    assert [frame.get_size() for frame in frames] == [(10, 10), (10, 10)]
    assert manager.get_sprite("player", 1).get_size() == (10, 10)