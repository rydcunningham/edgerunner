"""Test font installation and usage."""
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src import STYLE

def main():
    """Test font installation and display available fonts."""
    # Print all available fonts
    print("Available fonts:")
    fonts = sorted([f.name for f in fm.fontManager.ttflist])
    for font in fonts:
        if 'Rajdhani' in font:
            print(f"Found Rajdhani font: {font}")
    
    # Create a simple test plot
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.text(0.5, 0.5, 'Testing Rajdhani Font', 
            ha='center', va='center', fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

if __name__ == '__main__':
    main() 