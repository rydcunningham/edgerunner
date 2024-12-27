"""
EdgeRunner visualization theme module.
Defines color palettes and styling constants used across the library.
"""
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os
from pathlib import Path
import logging
import matplotlib.colors as mcolors

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Color palette
COLORS = {
    'cyberpunk_red': '#F75049',
    'arctic': '#FFFFFF',
    'shadow': '#1a1a1a',  # Darker shadow for subtle grid
    'slate': '#979797',
    'cyberpunk_cyan': '#5EF6FF',
    'background': '#000000'  # True black background
}

# Create semi-transparent versions
COLORS['cyberpunk_red_30'] = mcolors.to_rgba(COLORS['cyberpunk_red'], alpha=0.3)
COLORS['shadow_30'] = mcolors.to_rgba(COLORS['shadow'], alpha=0.3)

# Default color sequence for plots
COLOR_SEQUENCE = [
    COLORS['cyberpunk_red'],
    COLORS['cyberpunk_cyan'],
    COLORS['arctic'],
    COLORS['slate'],
    COLORS['shadow']
]

def validate_font_file(file_path):
    """Validate that the font file exists and has content."""
    if not file_path.exists():
        return False
    if file_path.stat().st_size == 0:
        return False
    return True

# Font settings and management
def setup_rajdhani_fonts():
    """Setup Rajdhani fonts from local files."""
    font_dir = Path(__file__).parent / 'fonts'
    
    # Define font files
    fonts = {
        'medium': font_dir / 'Rajdhani-Medium.ttf',
        'bold': font_dir / 'Rajdhani-Bold.ttf'
    }
    
    try:
        # Check if fonts exist
        missing_fonts = [name for name, path in fonts.items() if not validate_font_file(path)]
        if missing_fonts:
            error_msg = f"""
Missing Rajdhani font files: {', '.join(missing_fonts)}
Please download Rajdhani fonts from Google Fonts and place them in {font_dir}:
1. Visit https://fonts.google.com/specimen/Rajdhani
2. Download the font family
3. Extract the zip file
4. Copy Rajdhani-Medium.ttf and Rajdhani-Bold.ttf to {font_dir}
"""
            logger.error(error_msg)
            return 'DejaVu Sans', 'DejaVu Sans'
        
        # Add fonts to matplotlib
        for path in fonts.values():
            fm.fontManager.addfont(str(path))
        
        # Force matplotlib to reload font cache
        fm._load_fontmanager(try_read_cache=False)
        
        # Verify fonts are available
        font_names = [f.name for f in fm.fontManager.ttflist]
        logger.info(f"Available Rajdhani fonts: {[f for f in font_names if 'Rajdhani' in f]}")
        
        if not any('Rajdhani' in name for name in font_names):
            logger.warning("No Rajdhani fonts found after installation")
            return 'DejaVu Sans', 'DejaVu Sans'
            
        return 'Rajdhani Medium', 'Rajdhani Bold'
        
    except Exception as e:
        logger.error(f"Error setting up Rajdhani fonts: {str(e)}")
        return 'DejaVu Sans', 'DejaVu Sans'

# Setup fonts
FONT_MEDIUM, FONT_BOLD = setup_rajdhani_fonts()

# Common style parameters
STYLE = {
    # Font settings
    'font.family': 'sans-serif',
    'font.sans-serif': [FONT_MEDIUM, 'DejaVu Sans'],
    
    # Title font settings
    'axes.titleweight': 'bold',
    'figure.titleweight': 'bold',
    'axes.titlelocation': 'left',
    'axes.titlecolor': COLORS['cyberpunk_red'],
    'axes.titlesize': 14,
    'axes.titlepad': 12,
    
    # Figure settings
    'figure.facecolor': COLORS['background'],
    'figure.edgecolor': COLORS['background'],
    'figure.titlesize': 24,  # Larger main title
    'figure.subplot.top': 0.85,  # More space for main title
    
    # Axes settings
    'axes.facecolor': COLORS['background'],
    'axes.edgecolor': COLORS['cyberpunk_red_30'],
    'axes.labelcolor': COLORS['cyberpunk_red'],
    'axes.labelsize': 12,
    'axes.labelweight': 'bold',  # Bold axis labels
    'axes.grid': True,
    'axes.grid.axis': 'y',  # Only show horizontal grid lines
    'axes.spines.top': False,  # Hide top spine
    'axes.spines.right': False,  # Hide right spine
    
    # Grid settings
    'grid.color': COLORS['shadow'],
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,  # Thinner grid lines
    
    # Tick settings
    'xtick.color': COLORS['cyberpunk_red_30'],
    'ytick.color': COLORS['cyberpunk_red_30'],
    'xtick.labelcolor': COLORS['cyberpunk_red'],
    'ytick.labelcolor': COLORS['cyberpunk_red'],
    'xtick.major.size': 5,
    'ytick.major.size': 5,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    
    # Text settings
    'text.color': COLORS['cyberpunk_red'],
    
    # Legend settings
    'legend.facecolor': COLORS['background'],
    'legend.edgecolor': 'none',  # No legend edge
    'legend.framealpha': 1.0,
    'legend.labelcolor': COLORS['cyberpunk_red'],
    'legend.fontsize': 10,
    'legend.loc': 'upper right',  # Default legend position
    'legend.borderpad': 0.2,
    
    # Saving settings
    'savefig.facecolor': COLORS['background'],
    'savefig.edgecolor': COLORS['background'],
    'savefig.transparent': False
} 