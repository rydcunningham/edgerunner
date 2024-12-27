"""
Recreation of AI benchmark visualization using seaborn with EdgeRunner theme.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add the package root to Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.theme import set_theme, color

# Set the EdgeRunner theme
set_theme()

# Sample data
years = [2020, 2021, 2022, 2023, 2024]
models = {
    # Closed models
    'LSTM': {'scores': [40, 40, 40, 40, 40], 'type': 'CLOSED'},
    'Gopher 280B': {'scores': [32, 32, 60, 60, 60], 'type': 'CLOSED'},
    'PaLM 540B': {'scores': [32, 32, 70, 70, 70], 'type': 'CLOSED'},
    'code-davinci-002': {'scores': [32, 32, 68, 68, 68], 'type': 'CLOSED'},
    'GPT-4': {'scores': [32, 32, 32, 88, 88], 'type': 'CLOSED'},
    'Claude 3 Opus': {'scores': [32, 32, 32, 32, 89], 'type': 'CLOSED'},
    # Open models
    'BLOOM-176B': {'scores': [32, 32, 45, 45, 45], 'type': 'OPEN'},
    'LLaMa-1 65B': {'scores': [32, 32, 32, 65, 65], 'type': 'OPEN'},
    'LLaMa-2 70B': {'scores': [32, 32, 32, 75, 75], 'type': 'OPEN'},
    'LLaMa-3 70B': {'scores': [32, 32, 32, 32, 90], 'type': 'OPEN'}
}

# Convert to DataFrame
df = pd.DataFrame([
    {'Year': year, 'Model': model, 'Accuracy': score, 'Type': info['type']}
    for model, info in models.items()
    for year, score in zip(years, info['scores'])
])

# Create figure with more space at top for titles
plt.figure(figsize=(15, 9))

# Create main plot with adjusted position to make room for titles
ax = plt.subplot2grid((1, 1), (0, 0))
plt.subplots_adjust(top=0.85)  # Make room for titles

# Plot lines for each type
for model_type, marker in [('CLOSED', 'o'), ('OPEN', '^')]:
    data = df[df['Type'] == model_type]
    color_name = 'cyberpunk_red' if model_type == 'CLOSED' else 'cyberpunk_cyan'
    
    # Plot the lines and points without error bands
    sns.lineplot(
        data=data,
        x='Year', 
        y='Accuracy',
        color=color(color_name),
        marker=marker,
        label=model_type,
        ci=None  # Remove error bands
    )

    # Add model labels next to their last non-constant value
    last_points = data.groupby('Model').last()
    for model, row in last_points.iterrows():
        if row['Accuracy'] > 50:
            # Find where the model's accuracy last changed
            model_data = data[data['Model'] == model]
            accuracies = model_data['Accuracy'].values
            # Find the last point where accuracy changed
            changes = np.where(accuracies[:-1] != accuracies[1:])[0]
            label_year = years[changes[-1] + 1] if len(changes) > 0 else years[-1]
            
            plt.text(label_year + 0.1, row['Accuracy'], model,
                    color=color(color_name),
                    va='center',
                    fontsize=10)

# Add title and subtitle
fig = plt.gcf()
fig.text(0.12, 0.95, 'TOP-PERFORMING OPEN AND CLOSED AI MODELS',
         fontsize=20, fontweight='bold', color=color('cyberpunk_red'))
fig.text(0.12, 0.89, 'ON MMLU BENCHMARK',
         fontsize=16, color=color('cyberpunk_red'))

# Customize the plot
plt.ylabel('ACCURACY')
plt.xlabel('')
plt.ylim(30, 90)
plt.xlim(2020, 2024)

# Set x-axis ticks to show only years
plt.xticks(years)

# Style the legend with slate outline
legend = plt.legend(frameon=True)
legend.get_frame().set_edgecolor(color('slate'))
legend.get_frame().set_linewidth(1)

# Add credit text
plt.figtext(0.12, 0.02, 'CREDIT: "Open Models Report," EPOCH.AI, Nov 2024',
            fontsize=10, color=color('slate'))

plt.show() 