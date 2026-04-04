# Model Workshop

GTA RenderWare DFF model viewer and editor.

Companion tool to [IMG Factory 1.6](https://github.com/X-Seti/Img-Factory-1.6),
[Col Workshop](https://github.com/X-Seti/Col-Workshop), and
[TXD Workshop](https://github.com/X-Seti/Txd-Workshop).

## Features (Build 1)
- Open and parse GTA III / VC / SA PC DFF files
- Wireframe 3D preview with orbit/zoom controls
- Geometry list (multi-mesh DFF supported)
- Frame/bone hierarchy display
- Material list with texture names and colors
- Mesh info panel (vertex/triangle counts, normals, UV layers)
- Standalone mode (frameless window) and docked mode (IMG Factory tab)

## Planned
- Solid/shaded rendering
- OBJ export
- DFF re-save / round-trip editing
- Texture preview integration with TXD Workshop
- Collision mesh overlay (from COL Workshop)

## Architecture
Mirrors COL Workshop (`col_workshop.py`) exactly:
- `QWidget` base for docking support
- `SVGIconFactory` for all icons (no emoji, no bitmaps)
- `AppSettings` for shared theme
- `ModelWorkshopDialog` alias for IMG Factory integration

## Dependencies
- PyQt6
- Python 3.10+
- GTA DFF files (GTA III / VC / SA PC format)

## Running standalone
```bash
cd Model-Workshop
python3 -m apps.components.Model_Workshop.model_workshop
```
