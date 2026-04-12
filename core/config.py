from __future__ import annotations
import json
import threading
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent / "data" / "config.json"

_lock   = threading.Lock()   # guards all reads and writes
_cache: dict = {}            # in-memory cache so we don't hit disk every frame


def _load() -> dict:
    """Load config from disk into cache. Called lazily on first access."""
    global _cache
    with _CONFIG_PATH.open("r", encoding="utf-8") as f:
        _cache = json.load(f)
    return _cache


def _ensure_loaded() -> dict:
    """Return cache, loading from disk if not yet loaded."""
    if not _cache:
        _load()
    return _cache


def get(*keys: str, default=None):
    """
    Read a nested value from config by key path.
    e.g. get("config", "window_manager") → config["config"]["window_manager"]
    Returns default if any key in the path is missing.
    """
    with _lock:
        node = _ensure_loaded()
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node


def save(data: dict) -> None:
    """Overwrite the entire config file with new data and update the cache."""
    global _cache
    with _lock:
        _CONFIG_PATH.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        _cache = data


def reload() -> None:
    """Force a fresh load from disk — called by GUI after writing changes."""
    with _lock:
        _load()


def resolve_gesture_action(gesture_name: str) -> str | None:
    """
    Look up which action id is mapped to a gesture.
    Checks 'custom' map first, falls back to 'default'.
    Returns None if the gesture isn't mapped in either.
    """
    with _lock:
        cfg = _ensure_loaded()
    mapping = cfg.get("gesture_map", {})
    custom  = mapping.get("custom", {})
    default = mapping.get("default", {})
    return custom.get(gesture_name) or default.get(gesture_name)