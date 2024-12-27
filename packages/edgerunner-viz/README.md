# EdgeRunner Viz

A Python visualization library inspired by The Economist's Sybil library, with a cyberpunk aesthetic.

## Color Palette

- Cyberpunk Red (`#F75049`)
- Arctic (`#FFFFFF`)
- Shadow (`#424242`)
- Slate (`#979797`)
- Cyberpunk Cyan (`#5EF6FF`)

## Requirements

- Python 3.8+
- matplotlib
- seaborn
- numpy
- pandas
- pillow

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

See the `examples/` directory for usage examples. Basic usage:

```python
import matplotlib.pyplot as plt
from edgerunner_viz.theme import STYLE, COLOR_SEQUENCE

# Apply the EdgeRunner style
plt.style.use('dark_background')
for key, value in STYLE.items():
    plt.rcParams[key] = value

# Create your plot using COLOR_SEQUENCE colors
```

## Font Requirements

This library uses the Rajdhani font family. Please ensure it is installed on your system. 