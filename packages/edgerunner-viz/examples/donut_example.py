"""
Donut chart example demonstrating EdgeRunner visualization theme.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.theme import set_theme, color, text_size, text_pos

# Set the EdgeRunner theme
set_theme()

# Create sample data
categories = ['NEURAL', 'QUANTUM', 'HYBRID', 'ANALOG']
values = [45, 25, 20, 10]
colors = [color('arasaka_red'), color('electric_blue'), 
          color('shadow'), color('slate')]

# Create figure with 16:9 aspect ratio
width_inches = 15
height_inches = width_inches * 9/16
plt.figure(figsize=(width_inches, height_inches))

# Create main plot with adjusted position to make room for titles
ax = plt.subplot2grid((1, 1), (0, 0))
plt.subplots_adjust(top=0.85)

# Format percentage labels
def make_autopct(values):
    def my_autopct(pct):
        return f'{pct:.0f}%'
    return my_autopct

# Create donut chart
wedges, texts = plt.pie(values, 
                       colors=colors,
                       labels=[f'{cat} • {val}%' for cat, val in zip(categories, values)],
                       labeldistance=1.2,   # Move labels outside
                       wedgeprops=dict(
                           width=0.27,      # Donut hole
                           edgecolor='black',  # Border color
                           linewidth=1.2    # Border width
                       ),
                       textprops=dict(color=color('arasaka_red')),
                       rotatelabels=False)

# Add connecting lines
for wedge in wedges:
    # Get the angle of the wedge's center
    ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
    # Get the coordinates of the point on the wedge
    x = np.cos(np.deg2rad(ang))
    y = np.sin(np.deg2rad(ang))
    
    # Calculate connection points
    inner_radius = 1.0  # Just outside the donut
    outer_radius = 1.1  # Where the labels are
    
    # Create the line
    con = plt.plot([x * inner_radius, x * outer_radius], 
                   [y * inner_radius, y * outer_radius],
                   color=color('arasaka_red'),
                   linewidth=1)

# Style the labels with larger text
label_size = width_inches * text_size('axis_label')  # Using axis_label size
plt.setp(texts, size=label_size, weight='medium')

# Add title and subtitle
fig = plt.gcf()
fig.text(text_pos('title_x'), text_pos('title_y'), 'COMPUTING PARADIGM DISTRIBUTION',
         fontsize=width_inches * text_size('title'), fontweight='bold', color=color('arasaka_red'))
fig.text(text_pos('title_x'), text_pos('subtitle_y'), 'MARKET SHARE BY ARCHITECTURE TYPE',
         fontsize=width_inches * text_size('subtitle'), color=color('arasaka_red'))

# Add center text
plt.text(0, 0, '2024', 
         ha='center', va='center',
         fontsize=width_inches * text_size('title'),
         fontweight='bold',
         color=color('arasaka_red'))

# Add credit text
plt.figtext(text_pos('title_x'), text_pos('credit_y'),
            'CREDIT: EdgeRunner Market Analysis',
            fontsize=width_inches * text_size('credit'), color=color('slate'))

# Equal aspect ratio ensures circular plot
plt.axis('equal')

plt.show() 