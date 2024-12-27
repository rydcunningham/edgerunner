"""
Basic waveform example demonstrating EdgeRunner visualization theme.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import matplotlib.image as mpimg
from pathlib import Path
import sys

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.theme import set_theme, color, text_size, text_pos

# Set EdgeRunner theme
set_theme()

# Create sample data
x = np.linspace(0, 4*np.pi, 100)
signal1 = np.sin(x)
signal2 = np.cos(x)

# Create figure with 16:9 aspect ratio
width_inches = 15
height_inches = width_inches * 9/16
fig = plt.figure(figsize=(width_inches, height_inches))

# Create main plot with adjusted position to make room for titles
ax = plt.subplot2grid((1, 1), (0, 0))

# Configure grid with solid lines and semi-transparent background
ax.grid(True, which='major', color=color('shadow'), linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)  # Ensure grid is behind the data

# Add semi-transparent background between grid lines
ax.axhspan(-1.2, 1.2, color=color('arasaka_red'), alpha=0.11)

# Add watermark
watermark_path = Path(__file__).parent.parent.parent.parent / 'web' / 'public' / 'img' / 'logo.png'
if watermark_path.exists():
    img = mpimg.imread(str(watermark_path))
    imagebox = OffsetImage(img, zoom=0.5, alpha=0.15)
    anchored_box = AnchoredOffsetbox(loc='center',
                                    child=imagebox,
                                    pad=0,
                                    frameon=False,
                                    bbox_to_anchor=(0.5, 0.5),
                                    bbox_transform=fig.transFigure)
    fig.add_artist(anchored_box)

# Get the top y-coordinate of the plot in axes coordinates
plot_top = ax.get_position().y1

# Add title and subtitle (positioned relative to plot top)
title_offset = 0.05  # Distance above plot
subtitle_offset = 0.02  # Distance below title
fig.text(text_pos('title_x'), plot_top + title_offset, 'SIGNAL ANALYSIS DEMONSTRATION',
         fontsize=width_inches * text_size('title'), fontweight='bold', color=color('arasaka_red'))
fig.text(text_pos('title_x'), plot_top + subtitle_offset, 'HARMONIC WAVEFORM COMPARISON',
         fontsize=width_inches * text_size('subtitle'), color=color('arasaka_red'))

# Plot signals
plt.plot(x, signal1, color=color('arasaka_red'), label='SIGNAL A', 
         linewidth=2, marker='o', markevery=20, markersize=8)
plt.plot(x, signal2, color=color('electric_blue'), label='SIGNAL B', 
         linewidth=2, marker='^', markevery=20, markersize=8)

# Customize axes
plt.xlabel('TIME (s)', fontsize=width_inches * text_size('axis_label'))
plt.ylabel('AMPLITUDE', fontsize=width_inches * text_size('axis_label'))

# Set axis limits with some padding
plt.ylim(-1.2, 1.2)
plt.xlim(0, 4*np.pi)

# Style tick labels
plt.xticks(fontsize=width_inches * text_size('tick_label'))
plt.yticks(fontsize=width_inches * text_size('tick_label'))

# Style the legend with slate outline
legend = plt.legend(fontsize=width_inches * text_size('tick_label'))
legend.get_frame().set_edgecolor(color('slate'))
legend.get_frame().set_linewidth(1)

# Add credit text
plt.figtext(text_pos('title_x'), text_pos('credit_y'),
            'CREDIT: EdgeRunner Visualization Library Example',
            fontsize=width_inches * text_size('credit'), color=color('slate'))

plt.show() 