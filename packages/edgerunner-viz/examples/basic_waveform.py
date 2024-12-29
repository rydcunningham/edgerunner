"""
Basic waveform example demonstrating EdgeRunner visualization theme.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
import sys

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.theme import set_theme

# Set EdgeRunner theme
theme = set_theme('ARASAKA')

# Create sample data
x = np.linspace(0, 4*np.pi, 100)
signal1 = np.sin(x)
signal2 = np.cos(x)

# Create figure with theme-specified dimensions
width_inches = theme.figure.width
height_inches = width_inches * theme.figure.aspect_ratio
fig = plt.figure(figsize=(width_inches, height_inches))

# Create main plot with adjusted position to make room for titles
ax = plt.subplot2grid((1, 1), (0, 0))

# Configure grid with theme-specified properties
ax.grid(True, which='major', 
        color=theme.color('grid'), 
        linestyle=theme.figure.grid.style, 
        linewidth=theme.figure.grid.width)
ax.set_axisbelow(True)  # Ensure grid is behind the data

# Add semi-transparent background between grid lines
ax.axhspan(-1.2, 1.2, color=theme.color('primary'), 
           alpha=theme.figure.background_opacity)

# Get the top y-coordinate of the plot in axes coordinates
plot_top = ax.get_position().y1

# Add title and subtitle (positioned relative to plot top)
title_offset = 0.05  # Distance above plot
subtitle_offset = 0.02  # Distance below title
fig.text(theme.text_pos('title_x'), plot_top + title_offset, 'SIGNAL ANALYSIS DEMONSTRATION',
         fontsize=width_inches * theme.text_size('title'), fontweight='bold', color=theme.color('primary'))
fig.text(theme.text_pos('title_x'), plot_top + subtitle_offset, 'HARMONIC WAVEFORM COMPARISON',
         fontsize=width_inches * theme.text_size('subtitle'), color=theme.color('primary'))

# Plot signals
plt.plot(x, signal1, color=theme.color('primary'), label='SIGNAL A', 
         linewidth=2, marker='o', markevery=20, markersize=8)
plt.plot(x, signal2, color=theme.color('secondary'), label='SIGNAL B', 
         linewidth=2, marker='^', markevery=20, markersize=8)

# Customize axes
plt.xlabel('TIME (s)', fontsize=width_inches * theme.text_size('axis_label'))
plt.ylabel('AMPLITUDE', fontsize=width_inches * theme.text_size('axis_label'))

# Set axis limits with some padding
plt.ylim(-1.2, 1.2)
plt.xlim(0, 4*np.pi)

# Style tick labels
plt.xticks(fontsize=width_inches * theme.text_size('tick_label'))
plt.yticks(fontsize=width_inches * theme.text_size('tick_label'))

# Style the legend with slate outline
legend = plt.legend(fontsize=width_inches * theme.text_size('tick_label'))
legend.get_frame().set_edgecolor(theme.color('slate'))
legend.get_frame().set_linewidth(1)

# Add credit text
plt.figtext(theme.text_pos('title_x'), theme.text_pos('credit_y'),
            'CREDIT: EDGE/VIZ Library Example',
            fontsize=width_inches * theme.text_size('credit'), color=theme.color('accent_2'))

plt.show() 