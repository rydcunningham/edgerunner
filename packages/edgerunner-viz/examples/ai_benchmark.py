"""
Recreation of AI benchmark visualization with EdgeRunner style.
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

# Sample data
years = [2020, 2021, 2022, 2023, 2024]
closed_models = {
    'LSTM': [40, 40, 40, 40, 40],
    'Gopher 280B': [32, 32, 60, 60, 60],
    'PaLM 540B': [32, 32, 70, 70, 70],
    'code-davinci-002': [32, 32, 68, 68, 68],
    'GPT-4': [32, 32, 32, 88, 88],
    'Claude 3 Opus': [32, 32, 32, 32, 89]
}

open_models = {
    'BLOOM-176B': [32, 32, 45, 45, 45],
    'LLaMa-1 65B': [32, 32, 32, 65, 65],
    'LLaMa-2 70B': [32, 32, 32, 75, 75],
    'LLaMa-3 70B': [32, 32, 32, 32, 90]
}

# Create figure
fig, ax = plt.subplots(figsize=(15, 8))

# Plot closed models
for i, (model, scores) in enumerate(closed_models.items()):
    ax.plot(years, scores, color=COLORS['cyberpunk_red'], marker='o', 
            label=model if i == 0 else '_nolegend_')
    # Add label at the end
    if scores[-1] > 50:  # Only label if score is above 50%
        ax.text(2024.1, scores[-1], model, 
                color=COLORS['cyberpunk_red'], 
                fontfamily=FONT_MEDIUM,
                va='center')

# Plot open models
for i, (model, scores) in enumerate(open_models.items()):
    ax.plot(years, scores, color=COLORS['cyberpunk_cyan'], marker='^',
            label=model if i == 0 else '_nolegend_')
    # Add label at the end
    if scores[-1] > 50:  # Only label if score is above 50%
        ax.text(2024.1, scores[-1], model,
                color=COLORS['cyberpunk_cyan'],
                fontfamily=FONT_MEDIUM,
                va='center')

# Customize the plot
ax.set_title('TOP-PERFORMING OPEN AND CLOSED AI MODELS ON MMLU BENCHMARK',
             pad=20, fontsize=20, fontfamily=FONT_BOLD)
ax.set_ylabel('ACCURACY', fontfamily=FONT_BOLD)
ax.set_ylim(30, 90)
ax.set_xlim(2020, 2024.5)  # Extended for labels

# Create custom legend
legend_elements = [
    plt.Line2D([0], [0], color=COLORS['cyberpunk_red'], marker='o', label='CLOSED',
               markerfacecolor=COLORS['cyberpunk_red'], markersize=8),
    plt.Line2D([0], [0], color=COLORS['cyberpunk_cyan'], marker='^', label='OPEN',
               markerfacecolor=COLORS['cyberpunk_cyan'], markersize=8)
]
ax.legend(handles=legend_elements, loc='upper right')

# Add credit text
fig.text(0.02, 0.02, 'CREDIT: "Open Models Report," EPOCH.AI, Nov 2024',
         fontsize=10, fontfamily=FONT_MEDIUM, color=COLORS['slate'])

plt.tight_layout()
plt.show() 