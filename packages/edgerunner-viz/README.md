# EdgeRunner Visualization Theme

A seaborn-compatible theme for creating cyberpunk-inspired data visualizations. This theme provides a consistent, modern aesthetic inspired by The Economist's Sybil library.

## Color Palette

```python
COLORS = {
    'cyberpunk_red': '#F75049',    # Primary color for emphasis and titles
    'arctic': '#FFFFFF',           # Pure white for high contrast elements
    'shadow': '#424242',           # Subtle grid lines and backgrounds
    'slate': '#979797',           # Secondary elements and borders
    'cyberpunk_cyan': '#5EF6FF',   # Accent color for contrast
    'background': '#000000'        # True black background
}
```

## Typography & Text

- **Titles**: 
  - Left-aligned
  - Bold weight
  - Cyberpunk red color
  - Main title: 20pt
  - Subtitle: 16pt
  - Positioned at x=0.12 margin

- **Axis Labels**:
  - All caps
  - Bold weight
  - Cyberpunk red color
  - 12pt font size

- **Data Labels**:
  - Regular weight
  - 10pt font size
  - Positioned next to data points
  - Color matches the data series

## Grid & Axes

- **Grid Lines**:
  - Horizontal only
  - Shadow color (#424242)
  - 30% opacity
  - 0.5pt line width

- **Axes**:
  - Left and bottom spines only
  - Cyberpunk red color
  - Ticks in cyberpunk red
  - Integer ticks for years

## Legend

- **Style**:
  - Slate-colored outline (#979797)
  - 1pt line width
  - No background fill
  - Text in cyberpunk red

## Credits & Attribution

- Positioned at bottom left (x=0.12)
- Slate color
- 10pt font size

## Usage

```python
from edgerunner_viz.theme import set_theme, color

# Apply the theme
set_theme()

# Access colors
primary_color = color('cyberpunk_red')
accent_color = color('cyberpunk_cyan')
```

## Example Plots

See the `examples/` directory for sample visualizations using this theme. 