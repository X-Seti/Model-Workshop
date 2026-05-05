# X-Seti - May 2026 - apps/methods/dff_parser.py
# Shim: re-exports DFFParser, load_dff, detect_dff from the canonical location.
# model_workshop.py imports from apps.methods.dff_parser -- this bridges the gap.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../components/Model_Editor/depends'))
from dff_parser import DFFParser, load_dff, detect_dff, read_chunk
from dff_classes import (
    DFFModel, Geometry, Frame, Atomic, Material, Triangle,
    Vector3, RGBA, TexCoord, BoundingSphere, RWChunkType
)
