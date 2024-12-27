"""
Basic waveform example demonstrating EdgeRunner visualization theme.
"""
import numpy as np
import matplotlib.pyplot as plt
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
legend = plt.legend(frameon=True, fontsize=width_inches * text_size('tick_label'))
legend.get_frame().set_edgecolor(color('slate'))
legend.get_frame().set_linewidth(1)

# Add credit text
plt.figtext(text_pos('title_x'), text_pos('credit_y'),
            'CREDIT: EdgeRunner Visualization Library Example',
            fontsize=width_inches * text_size('credit'), color=color('slate'))

plt.show() 