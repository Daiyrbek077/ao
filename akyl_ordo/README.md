# Акыл Ордо (Akyл Ordo)

Offline educational quiz system with two desktop apps built in **Python 3.11+** using **PySide6**.

- **Akyл Ordo Maker**: create quiz games and export them as folder packages.
- **Akyл Ordo Player**: host and play games in class.

## Project layout

```
akyl_ordo/
├── akyl_ordo/
│   ├── common/
│   ├── maker/
│   └── player/
└── README.md
```

## Requirements

- Python 3.11+
- PySide6

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install PySide6
```

## Running

### Maker

```bash
python -m akyl_ordo.maker.main
```

### Player

```bash
python -m akyl_ordo.player.main
```

## Game package structure

```
<Game Title>/
├── main.json
└── content/
    ├── images/
    ├── videos/
    └── audio/
```

Sound files are loaded from a `/sounds/` folder at the working directory:

```
/sounds/
├── bg_music.mp3
├── click.wav
├── correct.wav
├── wrong.wav
├── bonus.wav
└── bonus_gold.wav
```

## Notes

- Both apps are offline and use JSON for storage.
- Media selected in Maker is copied into the game package `content/` subfolders.
- Player supports the three bonus types and manual score adjustments.
