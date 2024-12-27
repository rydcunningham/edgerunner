"""
EdgeRunner visualization theme module.
Defines a seaborn-compatible theme with cyberpunk aesthetics.
"""
import seaborn as sns
import matplotlib.pyplot as plt

# Color palette
COLORS = {
    'cyberpunk_red': '#F75049',
    'arctic': '#FFFFFF',
    'shadow': '#424242',
    'slate': '#979797',
    'cyberpunk_cyan': '#5EF6FF',
    'background': '#000000'
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
        'grid.alpha': 0.3,
        
        # Text
        'text.color': COLORS['cyberpunk_red'],
        'font.family': ['sans-serif'],
        'font.size': 12,
        
        # Axes
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.edgecolor': COLORS['cyberpunk_red'],
        'axes.labelcolor': COLORS['cyberpunk_red'],
        'axes.titlecolor': COLORS['cyberpunk_red'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        
        # Ticks
        'xtick.color': COLORS['cyberpunk_red'],
        'ytick.color': COLORS['cyberpunk_red'],
        
        # Legend
        'legend.frameon': False,
        'legend.labelcolor': COLORS['cyberpunk_red'],
    }
    
    # Set style and context
    sns.set_theme(style=style, context='notebook')
    
    # Set default color palette
    sns.set_palette([
        COLORS['cyberpunk_red'],
        COLORS['cyberpunk_cyan'],
        COLORS['arctic'],
        COLORS['slate'],
        COLORS['shadow']
    ])
    
    # Set default figure size
    plt.rcParams['figure.figsize'] = (12, 6)
    
    # Additional matplotlib settings
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'

def color(name):
    """Get a color from the palette by name."""
    return COLORS[name]

def palette():
    """Get the full color palette as a list."""
    return list(COLORS.values()) 