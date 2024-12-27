"""
Demonstration of Rajdhani font weights in different contexts.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src import COLORS, COLOR_SEQUENCE, STYLE
from src.theme import FONT_MEDIUM, FONT_BOLD

# Set the style
plt.style.use('dark_background')
for key, value in STYLE.items():
    plt.rcParams[key] = value

# Create figure with multiple subplots
fig = plt.figure(figsize=(12, 8))

# Main title (Bold)
fig.suptitle('EdgeRunner Visualization Typography', 
            fontsize=20, fontfamily=FONT_BOLD, y=0.95)

# Create a grid of subplots with more vertical space for subtitles
gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.3)

def add_subtitle(ax, text):
    """Add a left-aligned subtitle below the title."""
    ax.text(0, 1.05, text,
            transform=ax.transAxes,
            fontsize=10,
            fontfamily=FONT_MEDIUM,
            color=COLORS['arasaka_red'])

# Plot 1: Simple line plot
ax1 = fig.add_subplot(gs[0, 0])
x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x), color=COLOR_SEQUENCE[0], linewidth=2)
ax1.set_title('Sine Wave Plot', fontfamily=FONT_BOLD)
add_subtitle(ax1, 'Demonstrating smooth continuous data')
ax1.set_xlabel('Time', fontfamily=FONT_MEDIUM)
ax1.set_ylabel('Amplitude', fontfamily=FONT_MEDIUM)

# Plot 2: Scatter plot
ax2 = fig.add_subplot(gs[0, 1])
np.random.seed(42)
x = np.random.normal(0, 1, 50)
y = np.random.normal(0, 1, 50)
ax2.scatter(x, y, c=COLOR_SEQUENCE[0], s=50, alpha=0.6)
ax2.set_title('Scatter Distribution', fontfamily=FONT_BOLD)
add_subtitle(ax2, 'Showing random normal distribution')
ax2.set_xlabel('X Value', fontfamily=FONT_MEDIUM)
ax2.set_ylabel('Y Value', fontfamily=FONT_MEDIUM)

# Plot 3: Bar plot
ax3 = fig.add_subplot(gs[1, 0])
categories = ['A', 'B', 'C', 'D']
values = [3, 7, 2, 4]
ax3.bar(categories, values, color=COLOR_SEQUENCE[0])
ax3.set_title('Category Distribution', fontfamily=FONT_BOLD)
add_subtitle(ax3, 'Comparing discrete categories')
ax3.set_xlabel('Category', fontfamily=FONT_MEDIUM)
ax3.set_ylabel('Value', fontfamily=FONT_MEDIUM)

# Plot 4: Text showcase
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_title('Typography Sample', fontfamily=FONT_BOLD)
add_subtitle(ax4, 'Demonstrating font weights and styles')
ax4.text(0.05, 0.8, 'Title Text (Bold)', 
         fontsize=12, fontfamily=FONT_BOLD)
ax4.text(0.05, 0.6, 'Body Text (Medium)', 
         fontsize=12, fontfamily=FONT_MEDIUM)
ax4.text(0.05, 0.4, 'Labels & Annotations (Medium)', 
         fontsize=12, fontfamily=FONT_MEDIUM)
ax4.text(0.05, 0.2, '123456789 (Medium)', 
         fontsize=12, fontfamily=FONT_MEDIUM)
ax4.set_xticks([])
ax4.set_yticks([])

# Add a text box with font information
fig.text(0.02, 0.02, 
         'Fonts: Rajdhani Bold (titles) & Rajdhani Medium (body)', 
         fontsize=10, fontfamily=FONT_MEDIUM)

plt.show() 