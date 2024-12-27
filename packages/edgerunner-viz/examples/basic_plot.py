import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src import COLORS, COLOR_SEQUENCE, STYLE
from src.theme import FONT_MEDIUM, FONT_SEMIBOLD

# Set the style
plt.style.use('dark_background')
for key, value in STYLE.items():
    plt.rcParams[key] = value

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot with thicker lines for cyberpunk aesthetic
ax.plot(x, y1, color=COLOR_SEQUENCE[0], label='Signal 1', linewidth=2.5)
ax.plot(x, y2, color=COLOR_SEQUENCE[1], label='Signal 2', linewidth=2.5)

# Customize the plot with different font weights
ax.set_title('EdgeRunner Visualization Demo', 
             pad=20, fontsize=16, fontfamily=FONT_SEMIBOLD)  # SemiBold for title
ax.set_xlabel('Time', fontsize=12, fontfamily=FONT_MEDIUM)  # Medium for labels
ax.set_ylabel('Amplitude', fontsize=12, fontfamily=FONT_MEDIUM)

# Style the legend with Medium weight
ax.legend(frameon=True, 
         facecolor=COLORS['background'],
         edgecolor=COLORS['slate'],
         fontsize=10,
         prop={'family': FONT_MEDIUM})

# Adjust layout and display
plt.tight_layout()
plt.show() 