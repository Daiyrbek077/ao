from __future__ import annotations

from pathlib import Path

PRIMARY = "#3F51B5"
SECONDARY = "#2196F3"
SUCCESS = "#4CAF50"
ERROR = "#F44336"
BACKGROUND = "#F5F7FB"
CARD = "#FFFFFF"

SOUNDS_DIR = Path.cwd() / "sounds"
CONFIG_DIR = Path.home() / ".akyl_ordo"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

PLAYER_CONFIG = CONFIG_DIR / "player.json"
MAKER_CONFIG = CONFIG_DIR / "maker.json"
