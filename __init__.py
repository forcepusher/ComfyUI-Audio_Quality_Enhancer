"""
ComfyUI Audio Quality Enhancer - Initialization
Loads Audio Enhancer, Audio Effects, and Audio Fade nodes.
"""

try:
    from .audio_enhancer import NODE_CLASS_MAPPINGS as _enhancer_cls
    from .audio_enhancer import NODE_DISPLAY_NAME_MAPPINGS as _enhancer_disp
    from .audio_effects import NODE_CLASS_MAPPINGS as _effects_cls
    from .audio_effects import NODE_DISPLAY_NAME_MAPPINGS as _effects_disp
    from .audio_fade import NODE_CLASS_MAPPINGS as _fade_cls
    from .audio_fade import NODE_DISPLAY_NAME_MAPPINGS as _fade_disp

    NODE_CLASS_MAPPINGS = {**_enhancer_cls, **_effects_cls, **_fade_cls}
    NODE_DISPLAY_NAME_MAPPINGS = {**_enhancer_disp, **_effects_disp, **_fade_disp}

    print("ComfyUI Audio Quality Enhancer: Successfully loaded nodes")
    print(f"Available nodes: {list(NODE_CLASS_MAPPINGS.keys())}")

except Exception as e:
    print(f"ComfyUI Audio Quality Enhancer: Error loading nodes: {e}")
    import traceback
    traceback.print_exc()

    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
