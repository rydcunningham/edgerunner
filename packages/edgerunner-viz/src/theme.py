"""
EdgeRunner visualization theme module.
Defines a seaborn-compatible theme with cyberpunk aesthetics.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# Add Rajdhani font
FONT_DIR = Path(__file__).parent / 'fonts'
RAJDHANI_MEDIUM = str(FONT_DIR / 'Rajdhani-Medium.ttf')
RAJDHANI_SEMIBOLD = str(FONT_DIR / 'Rajdhani-SemiBold.ttf')

# Add fonts to matplotlib
for font_path in [RAJDHANI_MEDIUM, RAJDHANI_SEMIBOLD]:
    if Path(font_path).exists():
        fm.fontManager.addfont(font_path)

# Color palette
COLORS = {
    'arasaka_red': '#F75049',
    'arctic': '#FFFFFF',
    'shadow': '#424242',
    'slate': '#979797',
    'electric_blue': '#5EF6FF',
    'background': '#000000'
}

# Typography scale (relative to figure width)
TEXT_SCALE = {
    'title': 1.9,        # Main title
    'subtitle': 1.0,     # Subtitle
    'axis_label': 1.5,   # Axis labels
    'tick_label': 1.5,   # Tick labels
    'data_label': 1.3,   # Data point labels
    'credit': 1.2,       # Credit text
}

# Standard positions
TEXT_POSITIONS = {
    'title_x': 0.12,     # Left alignment position
    'title_y': 0.91,     # Title y-position
    'subtitle_y': 0.87,  # Subtitle y-position (closer to title)
    'credit_y': 0.03,    # Credit text y-position
}

def set_theme():
    """Set the EdgeRunner theme for all subsequent plots."""
    # Create the style dictionary
    style = {
        # Figure
        'figure.facecolor': COLORS['background'],
        'axes.facecolor': COLORS['background'],
        
        # Grid
        'grid.color': COLORS['shadow'],
        'grid.linestyle': '-',
        'grid.linewidth': 0.5,
        'grid.alpha': 1.0,
        
        # Text
        'text.color': COLORS['arasaka_red'],
        'font.family': ['Rajdhani'],
        'font.size': 14,
        
        # Axes
        'axes.grid': True,
        'axes.grid.axis': 'both',  # Show both x and y grid
        'axes.edgecolor': COLORS['arasaka_red'],
        'axes.labelcolor': COLORS['arasaka_red'],
        'axes.titlecolor': COLORS['arasaka_red'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.axisbelow': True,  # Grid lines below data
        
        # Background fill
        'axes.facecolor': f"{COLORS['arasaka_red']}1c",  # 11% opacity in hex
        
        # Ticks
        'xtick.color': COLORS['arasaka_red'],
        'ytick.color': COLORS['arasaka_red'],
        
        # Font weights
        'font.weight': 'medium',
        'axes.titleweight': 'semibold',
        'axes.labelweight': 'medium',
    }
    
    # Set style and context
    sns.set_theme(style=style, context='notebook')
    
    # Set default color palette
    sns.set_palette([
        COLORS['arasaka_red'],
        COLORS['electric_blue'],
        COLORS['arctic'],
        COLORS['slate'],
        COLORS['shadow']
    ])
    
    # Set default figure size
    plt.rcParams['figure.figsize'] = (12, 6)
    
    # Additional matplotlib settings
    plt.rcParams['font.family'] = 'Rajdhani'
    plt.rcParams['font.weight'] = 'medium'
    plt.rcParams['axes.titleweight'] = 'semibold'
    plt.rcParams['axes.labelweight'] = 'medium'

    # Add legend settings here with rcParams
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.facecolor'] = COLORS['background']
    plt.rcParams['legend.edgecolor'] = COLORS['slate']
    plt.rcParams['legend.labelcolor'] = 'linecolor'

def color(name):
    """Get a color from the palette by name."""
    return COLORS[name]

def text_size(name):
    """Get a standardized text size relative to figure width."""
    return TEXT_SCALE[name]

def text_pos(name):
    """Get a standardized text position."""
    return TEXT_POSITIONS[name]

def palette():
    """Get the full color palette as a list."""
    return list(COLORS.values()) 