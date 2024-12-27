"""
EdgeRunner Visualization Library
"""
from .theme import COLORS, COLOR_SEQUENCE, STYLE, setup_rajdhani_fonts

# Ensure font is set up on import
setup_rajdhani_fonts()

__all__ = ['COLORS', 'COLOR_SEQUENCE', 'STYLE'] 