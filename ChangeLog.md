#this belongs in root /ChangeLog.md - Version: 1

## July 2026 — Native QToolBar ribbon rebuild + 4-Pane View

**model_workshop.py, apps/methods/dff_viewport.py:**
- Replaced the old DockableToolbar-based panels (_create_transform_icon_panel,
  _create_transform_text_panel, _create_preview_controls, plus their
  reflow/grid helpers) with a native QMainWindow + QToolBar system -
  Selection, Snap Targets, Edit Geometry, Navigation, Render ribbons.
  RibbonManagerDialog added: two-pane dialog to reassign actions between
  toolbars, create/delete toolbars, save/load named presets, drag to
  reorder, plus an icon-size slider (was only reachable via toolbar
  right-click before).
- Removed ~1,240 lines of dead code left over from the rebuild - every
  removed action already had a live equivalent in the new ribbons,
  confirmed via zero call sites before deletion.
- Added the 3ds Max style 4-Pane View: Top/Front/Side/Perspective quad
  viewport via a QStackedWidget central widget, per-pane view
  reassignment by right-click, splitter-resizable, selection state shared
  live across all panes and the main view (clicking a vertex in one pane
  highlights it everywhere), flip/rotate/render-style toolbar actions
  applied to every visible pane instead of just whichever one happens to
  be hidden. DFFViewport gained set_view_lock() for locked rotation +
  orthographic projection on the Top/Front/Side panes; the Perspective
  pane stays free-rotate.
- Icon-scale persistence bug fixed: the Ribbon Manager's icon-size slider
  wrote to model_workshop.json but nothing ever read it back on the next
  launch, so icon size silently reset to 20px every time regardless of
  what was saved.
- Ribbon layout save/restore made version-aware: a _RIBBON_LAYOUT_VERSION
  class constant is now passed into QMainWindow.saveState()/
  restoreState(), so a stale save from an older ribbon structure is
  cleanly rejected instead of Qt silently failing to restore anything.
  restoreState()'s return value is checked/logged, and all 5 ribbons are
  force-shown after every restore attempt regardless of outcome - there's
  no user-facing way to have intentionally hidden one, so any hidden
  result is corrected rather than respected.
- A black-window/QOpenGLWidget context-creation failure was chased
  through several rounds of code rollback (all the way back to before
  this rebuild) before journalctl confirmed it was a GPU/PCIe hardware
  fault on the affected machine (BadTLP bus errors + NVIDIA GSP firmware
  load failure), unrelated to any of the above - resolved by a reboot,
  no code change needed. Ribbon rebuild + 4-Pane View were fully restored
  afterward once cleared of blame.
