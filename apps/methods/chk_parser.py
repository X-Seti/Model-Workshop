#!/usr/bin/env python3
#this belongs in apps/methods/chk_parser.py - Version: 3
# X-Seti - Apr 2026 - IMG Factory 1.6
# GTA III PS2 CHK splash texture parser
"""
Parses GTA III Liberty City Stories PS2 SPLASH/*.CHK texture files.

Format ('xet' — 'tex' reversed):
  Header (28 bytes):
    +00  u32  magic = 0x00746578  ('xet\\0')
    +04  u32  reserved = 0
    +08  u32  file_size
    +12  u32  data_size  (= file_size - 28)
    +16  u32  data_size  (duplicate)
    +20  u32  sub_type   (usually 7)
    +24  u32  reserved2  = 0
  Sub-header (60 bytes): metadata — skipped for now
  Pixel data (W × H bytes, 8bpp linear, Y-major)
  CLUT (1024 bytes): 256 × RGBA32 entries
    Alpha stored as PS2-style 0x00–0x80 (0x80 = fully opaque = 255)

All textures use 512-wide rows.  Height is derived from file size:
    pixel_bytes = file_size - 28 (main hdr) - 60 (sub hdr) - 1024 (CLUT)
    height      = pixel_bytes // 512
"""

import struct
import os
from typing import Optional, Dict, Any, List
from apps.methods.xtx_reader import parse_stories_textures, write_stories_textures

## Methods list -
# detect_chk
# chk_to_rgba
# load_chk
# parse_chk
# write_chk

CHK_MAGIC = 0x00746578   # 'xet\0' LE — 'tex\0' in big-endian
CHK_MAIN_HEADER  = 28
CHK_SUB_HEADER   = 60
CHK_CLUT_SIZE    = 1024
CHK_WIDTH        = 512   # All GTA3 PS2 splash textures are 512px wide


def detect_chk_old(data: bytes) -> bool:
    """Return True if data begins with a CHK ('xet') header."""
    if len(data) < 12:
        return False
    magic = struct.unpack_from('<I', data, 0)[0]
    return magic == CHK_MAGIC

def detect_chk(data: bytes) -> bool: #vers 2
    """True if data begins with the 'xet' ident."""
    return len(data) >= 4 and struct.unpack_from('<I', data, 0)[0] == CHK_MAGIC

def parse_chk(data: bytes, name: str = '') -> Optional[Dict[str, Any]]:
    """
    Parse a GTA III PS2 CHK splash texture from raw bytes.

    Returns a texture dict with keys:
        name, width, height, depth, format,
        pixel_data (raw 8bpp indices), clut (256×RGBA bytes),
        rgba_data (decoded RGBA32 bytes)
    or None on failure.
    """
    if not detect_chk(data):
        return None

    try:
        magic, _res0, file_sz, data_sz, _dup, sub_type, _res1 = \
            struct.unpack_from('<7I', data, 0)

        if file_sz != len(data):
            # Accept minor mismatch — some tools write the wrong size
            pass

        px_offset = CHK_MAIN_HEADER + CHK_SUB_HEADER
        px_bytes  = file_sz - CHK_MAIN_HEADER - CHK_SUB_HEADER - CHK_CLUT_SIZE

        if px_bytes <= 0 or px_offset + px_bytes + CHK_CLUT_SIZE > len(data):
            return None

        W = CHK_WIDTH
        H = px_bytes // W
        if H <= 0:
            return None

        pixel_data = data[px_offset : px_offset + W * H]
        clut_raw   = data[len(data) - CHK_CLUT_SIZE:]

        # Decode PS2 CLUT: alpha 0x80 = fully opaque = 255
        clut_rgba = bytearray(CHK_CLUT_SIZE)
        for i in range(256):
            r, g, b, a_ps2 = clut_raw[i*4 : i*4+4]
            clut_rgba[i*4 : i*4+4] = (r, g, b, min(255, a_ps2 * 2))
        clut_rgba = bytes(clut_rgba)

        # Decode pixel data → RGBA32
        rgba = bytearray(W * H * 4)
        for i in range(W * H):
            idx  = pixel_data[i]
            base = i * 4
            rgba[base : base+4] = clut_rgba[idx*4 : idx*4+4]

        return {
            'name':        name or os.path.splitext(os.path.basename(''))[0] or 'splash',
            'width':       W,
            'height':      H,
            'depth':       8,
            'format':      'PAL8',
            'has_alpha':   True,
            'mipmaps':     1,
            'sub_type':    sub_type,
            'pixel_data':  bytes(pixel_data),   # raw 8bpp indices
            'clut':        clut_rgba,            # 256 RGBA entries (decoded)
            'rgba_data':   bytes(rgba),          # decoded RGBA32 for display
            'mipmap_levels': [],
            'raster_format_flags': 0,
            'platform_id': 0,
        }

    except Exception as e:
        print(f"[CHKParser] Error parsing CHK: {e}")
        return None

def parse_chk_old(data: bytes, name: str = '') -> Dict[str, Any]: #vers 2
    """Parse CHK bytes; first texture fields plus 'textures' list."""
    if not detect_chk(data):
        raise ValueError("Not a CHK file ('xet' ident missing)")
    texs = parse_stories_textures(data)
    t = texs[0]
    return {
        'name': name or t['name'],
        'texture_name': t['name'],
        'width': t['width'], 'height': t['height'],
        'depth': t['depth'], 'format': t['format'],
        'has_alpha': t['has_alpha'],
        'mipmaps': 1,
        'platform': t['platform'],
        'pixel_data': t['indices'],
        'clut': t['palette'],
        'palette': t['palette'],
        'rgba_data': t['rgba_data'],
        'mipmap_levels': [],
        'raster_format_flags': 0,
        'platform_id': 0,
        'textures': texs,
    }


def load_chk(path: str) -> Optional[Dict[str, Any]]: #vers 2
    """Load CHK file; None and printed error on failure."""
    try:
        with open(path, 'rb') as f:
            data = f.read()
        return parse_chk(data, os.path.splitext(os.path.basename(path))[0])
    except (OSError, ValueError, struct.error) as e:
        print(f"[CHKParser] Failed to load {path}: {e}")
        return None

def load_chk_old(path: str) -> Optional[Dict[str, Any]]:
    """Load a CHK file from disk. Returns texture dict or None."""
    try:
        with open(path, 'rb') as f:
            data = f.read()
        name = os.path.splitext(os.path.basename(path))[0]
        return parse_chk(data, name)
    except Exception as e:
        print(f"[CHKParser] Failed to load {path}: {e}")
        return None

def chk_to_rgba(tex: Dict) -> Optional[bytes]: #vers 2
    """RGBA bytes from a parsed CHK texture dict."""
    return tex.get('rgba_data') if tex else None

def write_chk(original_bytes: bytes, rgba) -> bytes: #vers 1
    """Return CHK bytes with new RGBA; header and size unchanged."""
    if not detect_chk(original_bytes):
        raise ValueError("Not a CHK file ('xet' ident missing)")
    return write_stories_textures(original_bytes, rgba)

__all__ = ['chk_to_rgba', 'detect_chk', 'load_chk', 'parse_chk', 'write_chk']
