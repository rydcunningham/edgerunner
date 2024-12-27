"""
Recreation of AI benchmark visualization using seaborn with EdgeRunner theme.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime
from io import StringIO
from adjustText import adjust_text

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.theme import set_theme, color, text_size

# Set the EdgeRunner theme
set_theme()

# Raw data
scatter_data = """Model,Release Date,Accuracy,Category
T5-Small,10/22/2019,26.7%,Open
GPT-NeoX 20B,2/8/2022,33.6%,Open
OPT-66B,5/1/2022,36.0%,Open
BLOOM-176B,7/10/2022,39.1%,Open
GLM 130B,8/3/2022,44.8%,Open
LLaMa-1 65B,2/23/2023,63.4%,Open
LLaMa-2 70B,7/17/2023,68.9%,Open
Grok-1,11/2/2023,73.0%,Open
Cohere Command R+,4/3/2024,75.7%,Open
LLaMa-3 70B,4/17/2024,82.0%,Open
Llama 3.1 405B,7/22/2024,87.3%,Open
text-davinci-001,5/27/2020,39.7%,Closed
Copher 280B,12/7/2021,60%,Closed
code-davinci-002,2/28/2022,68.2%,Closed
PaLM 540B,4/3/2022,71.3%,Closed
GPT-4 (original),3/14/2023,86.4%,Closed
Claude 3 Opus,3/3/2024,86.8%,Closed
GPT-4o,5/12/2024,87.2%,Closed
Claude 3.5 Sonnet,6/19/2024,88.7%,Closed"""

# Convert to DataFrame
df = pd.read_csv(StringIO(data))

# Clean up the data
df['Release Date'] = pd.to_datetime(df['Release Date'], format='%m/%d/%Y')
df['Accuracy'] = df['Accuracy'].str.rstrip('%').astype(float)
df['Year'] = df['Release Date'].dt.year

# Create figure with 16:9 aspect ratio
width_inches = 15
height_inches = width_inches * 9/16
plt.figure(figsize=(width_inches, height_inches))

# Create main plot with adjusted position to make room for titles
ax = plt.subplot2grid((1, 1), (0, 0))
plt.subplots_adjust(top=0.85)  # Make room for titles

# Store texts for adjustText
texts = []

# Plot lines for each type
for category, marker in [('Closed', 'o'), ('Open', '^')]:
    data = df[df['Category'] == category]
    color_name = 'arasaka_red' if category == 'Closed' else 'electric_blue'
    
    # Sort by date for proper line plotting
    data = data.sort_values('Release Date')
    
    # Plot the lines and points with steps
    plt.step(data['Release Date'], data['Accuracy'],
            where='post',
            color=color(color_name),
            label=category)
    
    # Add markers
    plt.plot(data['Release Date'], data['Accuracy'],
            color=color(color_name),
            marker=marker,
            linestyle='none')

    # Add model labels
    for _, row in data.iterrows():
        # Calculate offset
        offset_x = pd.Timedelta(days=-60)
        offset_y = 2  # 2 percentage points up
        
        text = plt.text(row['Release Date'] + offset_x, 
                       row['Accuracy'] + offset_y,
                       row['Model'],
                       color=color(color_name),
                       va='center',
                       ha='right' if category == 'Closed' else 'left',  # Align text towards the point
                       fontsize=width_inches * 0.67)
        texts.append(text)

# Add title and subtitle
fig = plt.gcf()
title_size = width_inches * 1.6
subtitle_size = width_inches * 0.8

fig.text(0.12, 0.91, 'TOP-PERFORMING OPEN AND CLOSED AI MODELS',
         fontsize=title_size, fontweight='bold', color=color('arasaka_red'))
fig.text(0.12, 0.87, 'ON MMLU BENCHMARK',
         fontsize=subtitle_size, color=color('arasaka_red'))

# Customize the plot
plt.ylabel('ACCURACY', fontsize=width_inches)
plt.xlabel('')

# Set axis limits
plt.ylim(20, 95)
date_range = pd.date_range(start='2019-01-01', end='2025-01-01', freq='YS')
plt.xlim(date_range[0], date_range[-1])

# Set x-axis ticks to show only years
plt.xticks(date_range, [d.year for d in date_range], fontsize=width_inches * 0.8)
plt.yticks(fontsize=width_inches * 0.8)

# Style the legend with slate outline
handles, labels = plt.gca().get_legend_handles_labels()
legend = plt.legend(fontsize=width_inches * text_size('tick_label'))

# Add credit text
plt.figtext(0.12, 0.03, 'CREDIT: "Open Models Report," EPOCH.AI, Nov 2024',
            fontsize=width_inches * 1, color=color('slate'))

# Adjust text positions to avoid overlaps while maintaining offset
adjust_text(texts,
           expand_points=(1.5, 1.5),
           expand_text=(1.2, 1.2),
           force_points=0.2,
           force_text=0.5,
           only_move={'points': (0, 0), 'text': (0, 1)},  # Only allow vertical movement
           arrowprops=None)

plt.show() 