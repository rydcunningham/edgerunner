# EdgeRunner Visualization Theme

A seaborn-compatible theme for creating cyberpunk-inspired data visualizations. This theme provides a consistent, modern aesthetic inspired by The Economist's Sybil library.

## Color Palette

```python
COLORS = {
    'arasaka_red': '#F75049',    # Primary color for emphasis and titles
    'arctic': '#FFFFFF',           # Pure white for high contrast elements
    'shadow': '#424242',           # Subtle grid lines and backgrounds
    'slate': '#979797',           # Secondary elements and borders
    'electric_blue': '#5EF6FF',   # Accent color for contrast
    'background': '#000000'        # True black background
}
```

## Typography & Text

All font sizes are relative to the figure width for consistent scaling. For a 1000px wide figure:

- **Graph Title**: 
  - Left-aligned at x=0.12
  - Bold weight
  - Arasaka Red color
  - Size: 1.6× figure width
  - Position: y=0.91

- **Graph Subtitle**:
  - Left-aligned at x=0.12
  - Regular weight
  - Arasaka Red color
  - Size: 0.8× figure width
  - Position: y=0.87

- **Axis Labels**:
  - All caps
  - Bold weight
  - Arasaka Red color
  - Size: 1.0× figure width

- **Tick Labels & Legend**:
  - Regular weight
  - Size: 0.8× figure width
  - Arasaka Red color

- **Data Labels**:
  - Regular weight
  - Size: 0.67× figure width
  - Color matches data series
  - Positioned next to points

- **Credits & Sources**:
  - Regular weight
  - Size: 1.0× figure width
  - Slate color
  - Left-aligned at x=0.12
  - Position: y=0.03

## Figure Properties

- Aspect ratio: 16:9 (widescreen)
- Recommended widths: 800-1200px
- Default margins: top=0.85 for title space

## Line Plots

- **Style**:
  - Stepped lines (where='post')
  - Markers at data points
  - No interpolation between points
  - Line color matches markers

## Grid & Axes

- **Grid Lines**:
  - Horizontal only
  - Shadow color (#424242)
  - 30% opacity
  - 0.5pt line width

- **Axes**:
  - Left and bottom spines only
  - Arasaka Red color
  - Integer ticks for years

## Legend

- **Style**:
  - Slate-colored outline
  - 1pt line width
  - No background
  - Text in Arasaka Red

## Usage

```python
from edgerunner_viz.theme import set_theme, color, text_size, text_pos

# Apply theme
set_theme()

# Create figure (1000px at 72dpi)
width_inches = 15
height_inches = width_inches * 9/16
plt.figure(figsize=(width_inches, height_inches))

# Use standardized text sizes and positions
plt.title('CHART TITLE', 
          fontsize=width_inches * text_size('title'),
          x=text_pos('title_x'),
          y=text_pos('title_y'))

# Use colors
primary = color('arasaka_red')
accent = color('electric_blue')
```

See `examples/` directory for complete visualizations. 