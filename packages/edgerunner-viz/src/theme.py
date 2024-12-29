"""
EdgeRunner visualization theme module.
Defines a seaborn-compatible theme system with multiple presets.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

# Font setup
FONT_DIR = Path(__file__).parent / 'fonts'
RAJDHANI_MEDIUM = str(FONT_DIR / 'Rajdhani-Medium.ttf')
RAJDHANI_SEMIBOLD = str(FONT_DIR / 'Rajdhani-SemiBold.ttf')

# Add fonts to matplotlib
for font_path in [RAJDHANI_MEDIUM, RAJDHANI_SEMIBOLD]:
    if Path(font_path).exists():
        fm.fontManager.addfont(font_path)

# Theme directory
THEME_DIR = Path(__file__).parent / 'themes'

def load_theme(name: str = 'ARASAKA') -> Dict[str, Any]:
    """Load a theme from a YAML file."""
    theme_file = THEME_DIR / f"{name.lower()}_theme.yaml"
    
    try:
        with open(theme_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise ValueError(f"Theme '{name}' not found")

class Theme:
    """Dynamic theme object with easy access to theme properties."""
    def __init__(self, theme_config: Dict[str, Any]):
        self._config = theme_config
    
    def __getattr__(self, name):
        """Dynamically access nested theme properties."""
        if name in self._config:
            value = self._config[name]
            return Theme(value) if isinstance(value, dict) else value
        
        for key, value in self._config.items():
            if isinstance(value, dict) and name in value:
                return value[name]
        
        raise AttributeError(f"No attribute '{name}' in theme")
    
    def color(self, name: Optional[str] = None):
        """Get a color from the theme palette."""
        colors = self._config.get('colors', {})
        return colors if name is None else colors.get(name, colors.get('primary', '#000000'))
    
    def text_size(self, name: str):
        """Get a standardized text size."""
        return self._config.get('text_scale', {}).get(name, 1.0)
    
    def text_pos(self, name: str):
        """Get a standardized text position."""
        return self._config.get('text_positions', {}).get(name, 0.0)

def set_theme(name: str = 'ARASAKA') -> Theme:
    """Set the theme for subsequent plots and return a Theme object."""
    theme_config = load_theme(name)
    _apply_theme(theme_config)
    return Theme(theme_config)

def _apply_theme(theme: Dict[str, Any]):
    """Apply the theme configuration to matplotlib and seaborn."""
    colors = theme['colors']
    
    style = {
        'figure.facecolor': colors['background'],
        'axes.facecolor': colors['background'],
        'grid.color': colors['grid'],
        'text.color': colors['text'],
        'font.family': ['Rajdhani'],
        'axes.edgecolor': colors['primary'],
        'axes.labelcolor': colors['primary'],
        'axes.titlecolor': colors['primary'],
        'xtick.color': colors['primary'],
        'ytick.color': colors['primary'],
        'axes.grid': True,
        'axes.spines.top': False,
        'axes.spines.right': False,
    }
    
    sns.set_theme(style=style, context='notebook')
    sns.set_palette(list(colors.values()))
    
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'font.family': 'Rajdhani',
        'legend.frameon': True,
        'legend.facecolor': colors['background'],
        'legend.edgecolor': colors['grid'],
    })

# Utility functions for direct color, text size, and palette access
def color(name: Optional[str] = None, theme: str = 'ARASAKA'):
    """Get a color from the theme palette."""
    return load_theme(theme)['colors'].get(name) if name else load_theme(theme)['colors']

def text_size(name: str, theme: str = 'ARASAKA'):
    """Get a standardized text size."""
    return load_theme(theme)['text_scale'][name]

def text_pos(name: str, theme: str = 'ARASAKA'):
    """Get a standardized text position."""
    return load_theme(theme)['text_positions'][name]

def palette(theme: str = 'ARASAKA'):
    """Get the full color palette."""
    return load_theme(theme)['colors'] 