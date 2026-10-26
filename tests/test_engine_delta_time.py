import importlib
from types import SimpleNamespace

import pytest

pytest.importorskip("PySide6")

from VertexEngine.engine import GameEngine


def test_update_frame_sets_delta_time(monkeypatch):
    frame_times = iter((10.0, 10.25))
    engine_module = importlib.import_module("VertexEngine.engine")
    monkeypatch.setattr(engine_module.time, "perf_counter", lambda: next(frame_times))

    engine = SimpleNamespace(
        _last_frame_time=next(frame_times),
        delta_time=0.0,
        hasFocus=lambda: True,
        screen=SimpleNamespace(fill=lambda color: None),
        color=(0, 0, 0),
        scene_manager=SimpleNamespace(_update=lambda: None, draw=lambda surface: None),
        _sync_qimage=lambda: None,
        update=lambda: None,
    )
    GameEngine._update_frame(engine)

    assert engine.delta_time == pytest.approx(0.25)