from __future__ import annotations
import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Optional

from core.cooldown import Cooldown
from core.config  import resolve_gesture_action
from actions.base import BaseAction

# ── Action registry ────────────────────────────────────────────────────────
_action_registry: dict[str, BaseAction] = {}
_registry_loaded = False

# Subdirectories under actions/
_ACTION_PKGS = ["actions.app", "actions.linux", "actions.mac", "actions.media",
                "actions.util", "actions.win"]


def _build_action_registry() -> None:
    global _registry_loaded
    base_path = Path(__file__).parent.parent / "actions"

    for pkg_name in _ACTION_PKGS:
        # Convert "actions.media" → path actions/media
        subdir = base_path / pkg_name.split(".", 1)[1]
        if not subdir.exists():
            continue

        for _finder, mod_name, _ispkg in pkgutil.iter_modules([str(subdir)]):
            full_name = f"{pkg_name}.{mod_name}"
            try:
                mod = importlib.import_module(full_name)
            except Exception as exc:
                print(f"[Router] Failed to import {full_name}: {exc}")
                continue

            # Find all concrete BaseAction subclasses in this module
            for _name, obj in inspect.getmembers(mod, inspect.isclass):
                if (
                    issubclass(obj, BaseAction)
                    and obj is not BaseAction
                    and hasattr(obj, "id")
                    and obj.__module__ == full_name  # only classes defined in this module
                ):
                    try:
                        instance = obj()
                        _action_registry[instance.id] = instance
                    except Exception as exc:
                        print(f"[Router] Failed to instantiate {obj}: {exc}")

    _registry_loaded = True
    print(f"[Router] Registered {len(_action_registry)} actions:")
    for action_id in sorted(_action_registry):
        a = _action_registry[action_id]
        print(f"  • {action_id:20s} — {a.name}")


def _get_action(action_id: str) -> Optional[BaseAction]:
    if not _registry_loaded:
        _build_action_registry()
    return _action_registry.get(action_id)


# ── Gesture module loader ──────────────────────────────────────────────────

def _load_gesture_modules() -> list:
    base    = Path(__file__).parent.parent / "gestures"
    subdirs = ["static", "motion"]
    raw: list[tuple[str, object]] = []

    for sub in subdirs:
        pkg_path = base / sub
        if not pkg_path.exists():
            continue
        pkg_name = f"gestures.{sub}"
        for _finder, mod_name, _ispkg in pkgutil.iter_modules([str(pkg_path)]):
            full_name = f"{pkg_name}.{mod_name}"
            try:
                mod = importlib.import_module(full_name)
            except Exception as exc:
                print(f"[Router] Failed to import {full_name}: {exc}")
                continue
            if not all(hasattr(mod, attr) for attr in ("GESTURE_NAME", "matches")):
                print(f"[Router] Skipping {full_name} — missing GESTURE_NAME or matches()")
                continue
            raw.append((mod.GESTURE_NAME, mod))

    # _2 (double-hand) before _1 (single-hand); alphabetical within each tier
    raw.sort(key=lambda item: (0 if item[0].endswith("_2") else 1, item[0]))

    modules = [mod for _, mod in raw]
    print(f"[Router] Loaded {len(modules)} gesture modules:")
    for mod in modules:
        print(f"  • {mod.GESTURE_NAME}")
    return modules


# ── GestureRouter ──────────────────────────────────────────────────────────

class GestureRouter:
    def __init__(self, cooldown: Cooldown) -> None:
        self._cooldown = cooldown
        self._modules  = _load_gesture_modules()
        _build_action_registry()  # eager load so first gesture fires instantly

    def route(self, result) -> Optional[str]:
        if result is None:
            return None

        for mod in self._modules:
            try:
                if not mod.matches(result):
                    continue

                name = mod.GESTURE_NAME

                if not self._cooldown.can_trigger(name):
                    continue

                action_id = resolve_gesture_action(name)
                if action_id is None:
                    print(f"[Router] No action mapped for '{name}' — skipping")
                    continue

                action = _get_action(action_id)
                if action is None:
                    print(f"[Router] Action '{action_id}' not found in registry — skipping")
                    continue

                action.execute()
                self._cooldown.record(name)
                return name

            except Exception as exc:
                print(f"[Router] Error routing {mod.GESTURE_NAME}: {exc}")

        return None