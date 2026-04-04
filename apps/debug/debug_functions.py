# Stub debug module — replaces apps.debug from IMG Factory
# Model-Workshop does not require IMG Factory's debugger.

class _NullDebugger:
    """Silent no-op debugger stub."""
    def __getattr__(self, name):
        return lambda *a, **kw: None
    def __call__(self, *a, **kw):
        return None

img_debugger = _NullDebugger()
