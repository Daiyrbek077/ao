# Akyl Ordo (Акыл Ордо)

Offline quiz system with two desktop apps:

- **Maker**: create game packages.
- **Player**: host/play games in class.

## Requirements

- Python 3.11+
- PySide6

## Structure

```
Akyl Ordo/
  akyl_ordo/
    common/
    maker/
    player/
```

## Running

```bash
python -m akyl_ordo.maker.app
```

```bash
python -m akyl_ordo.player.app
```

## Game Package

The Maker generates:

```
<Game Title>/
 ├── main.json
 └── content/
     ├── images/
     ├── videos/
     └── audio/
```

Sounds for Player should live in a `sounds/` folder in the working directory:

```
/sounds/
 ├── bg_music.mp3
 ├── click.wav
 ├── correct.wav
 ├── wrong.wav
 └── bonus.wav
```
