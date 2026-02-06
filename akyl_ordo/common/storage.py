from __future__ import annotations

import json
from pathlib import Path

from .models import GameData


def ensure_game_structure(root: Path, title: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    content_dir = root / "content"
    (content_dir / "images").mkdir(parents=True, exist_ok=True)
    (content_dir / "videos").mkdir(parents=True, exist_ok=True)
    (content_dir / "audio").mkdir(parents=True, exist_ok=True)
    game = GameData(title=title)
    write_game(root / "main.json", game)
    return root


def write_game(path: Path, game: GameData) -> None:
    path.write_text(json.dumps(game.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def load_game(path: Path) -> GameData:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return GameData.from_dict(payload)
