# ternary-chart-tool

A Python tool for creating flexible ternary diagrams. Ter_Charts-py supports multiple charts in a single figure, with options for rotation, scaling, translation, edge cuts, contour overlays, and heatmaps.

## Features

- Up to four ternary charts in a single figure object
- Variable grid step sizes: 1, 2, 5, or 10
- Per-chart rotation (0, 90, 180 degrees), translation, and scaling
- Configurable edge cuts (left, right, and top) for zooming into dense regions
- Contour and heatmap overlays
- Multiple data subsets per chart, each plotted with a distinct marker
- Axis labels, corner labels, custom text labels, and line segment annotations
- Builds on matplotlib's full formatting options

## Requirements

- Python 3.13.2 or newer
- See [requirements.txt](requirements.txt) for required packages

## Quick Start

1. Open your IDE or use a Jupyter Notebook in your browser.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Place your data in a CSV file following the format described in the **Input** section below.
4. Open `ternary_charts_viz_tool.py` and set the `myfile` variable to your CSV file path.
5. Adjust the configuration parameters (steps, cuts, rotations, etc.) as needed.
6. Run the script: `python ternary_charts_viz_tool.py`

A matplotlib figure window will open displaying your ternary chart(s), or it will appear inline. To run the included example immediately, no changes are needed — the script is pre-configured to load `Data_Example.csv`.

## Repository Contents

| File | Description |
|------|-------------|
| `ternary_charts_viz_tool.py` | Main script containing all functions and execution logic |
| `Data_Example.csv` | Example input dataset for testing and demonstration |
| `requirements.txt` | Python package dependencies |
| `TUTORIAL.md` | Step-by-step walkthrough for common use cases |
| `LICENSE` | MIT License |

## Input

### CSV Data File

Input data is provided as a comma-separated values (CSV) file. The file can contain up to four datasets (one per chart), each occupying four columns.

**Column structure:**

| Column | Name | Description |
|--------|------|-------------|
| 1 | `L0` | Left component of dataset 0 (numeric) |
| 2 | `R0` | Right component of dataset 0 (numeric) |
| 3 | `T0` | Top component of dataset 0 (numeric) |
| 4 | `Series0` | Subset label for dataset 0 (single letter, e.g. `a`, `b`, `c`) |
| 5 | `L1` | Left component of dataset 1 |
| ... | ... | Pattern continues for datasets 1, 2, and 3 |

- Each row's three numeric values (L, R, T) must sum to 100. If they do not, the tool normalizes them automatically.
- The `Series` column assigns each row to a named subset. Rows sharing the same letter are plotted with the same marker and color. A chart may have one or more subsets.
- Datasets do not need to have the same number of rows. Empty cells in shorter datasets are ignored.
- Only data to be plotted should be included in the file; no extra formatting or summary rows.

### Setting the File Path

At the bottom of `ternary_charts_viz_tool.py`, set the `myfile` variable to the path of your CSV file:

```python
myfile = "Data_Example.csv"     # relative or absolute path
```

## Configuration Parameters

All configuration parameters are Python lists. Each list must contain one entry per chart. If you have two charts, each list must have two entries; for one chart, each list has one entry.

### `steps`

**Type:** list of int | **Valid values:** `1`, `2`, `5`, or `10`

The gridline interval for each chart, expressed as a percentage. A value of `10` draws gridlines every 10 units (10 divisions per side); `5` draws them every 5 units (20 divisions).

```python
steps = [10, 5, 10, 10]
```

### `cuts`

**Type:** list of list of int, each inner list is `[left_cut, right_cut, top_cut]` | **Valid values:** 0 to 50

Trims the corners of the triangle. A cut of `0` means no trimming on that edge. Useful for zooming in on densely populated regions.

```python
cuts = [[10, 20, 10], [30, 30, 30], [0, 30, 0], [0, 0, 0]]
```

### `axs_shifts`

**Type:** list of list of float, each inner list is `[x_shift, y_shift]`

Translates each chart horizontally and vertically within the figure. Use this to position multiple charts side by side.

```python
axs_shifts = [[50, 10], [200, 0], [330, 0], [450, 0]]
```

### `rot_angles`

**Type:** list of float | **Valid values:** 0 to 180

Rotation angle in degrees for each chart, applied around the center of the triangle. Common values are `0` (standard), `90`, and `180` (inverted).

```python
rot_angles = [60, 180, 0, 0]
```

### `m_factors`

**Type:** list of float | **Valid values:** greater than 0 and up to 1

Scale factor for each chart. A value of `1` keeps the original size; `0.6` renders it at 60%.

```python
m_factors = [1, 1.5, 0.6, 1]
```

### `l_widths`

**Type:** list of float

Line width of the gridlines for each chart, in matplotlib point units.

```python
l_widths = [0.2, 0.3, 0.2, 0.4]
```

### `l_colors`

**Type:** list of str

Color of the gridlines for each chart. Accepts any matplotlib color string (e.g., `'black'`, `'blue'`, `'#FF5733'`).

```python
l_colors = ['blue', 'black', 'red', 'green']
```

### `c_maps`

**Type:** list of str

Matplotlib colormap name for contour or heatmap overlays. Only active when the corresponding `con_choices` entry is `'yes'`.

```python
c_maps = ['Blues', 'Greys', 'Reds', 'Reds']
```

### `con_levels`

**Type:** list of int

Number of contour levels in the overlay. Only active when `con_choices` is `'yes'` and `con_types` is `'density'`.

```python
con_levels = [12, 10, 10, 5]
```

### `con_types`

**Type:** list of str | **Valid values:** `'density'` or `'heatmap'`

Type of overlay. `'density'` draws filled contours; `'heatmap'` draws a pixelated grid. Only active when `con_choices` is `'yes'`.

```python
con_types = ['density', 'density', 'density', 'density']
```

### `con_choices`

**Type:** list of str | **Valid values:** `'yes'` or `'no'`

Whether to draw a contour or heatmap overlay on each chart.

```python
con_choices = ['no', 'no', 'yes', 'no']
```

### `show_axis_labels`

**Type:** list of str | **Valid values:** `'yes'` or `'no'`

Whether to display numeric tick labels along the three sides of each chart.

```python
show_axis_labels = ['no', 'yes', 'no', 'no']
```

### `corner_labels`

**Type:** list of str | **Valid values:** `'yes'` or `'no'`

Whether to draw alphabetical labels (A, B, C, ...) at the corner points created by edge cuts.

```python
corner_labels = ['no', 'no', 'yes', 'no']
```

## Output

The script produces matplotlib figure(s). To save to a file, add the following line before `plt.show()` in the script:

```python
plt.savefig("output.png", dpi=300, bbox_inches='tight')
```

Supported formats include PNG, PDF, SVG, and EPS.

## Expected Behavior and Validation

The script performs basic validation before plotting and exits with an informative message if any of the following conditions are violated:

- `steps` values must be in `{1, 2, 5, 10}`
- `cuts` values must be between 0 and 50 inclusive
- `rot_angles` values must be between 0 and 180 inclusive
- `m_factors` values must be greater than 0 and no greater than 1

Data points that fall outside the triangle boundary after applying cuts are automatically filtered and not plotted. Rows with all three components equal to zero are silently skipped. Rows that do not sum to 100 are normalized automatically.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Authors

EK Esawi and Lily Meadow, Eastern Oregon University
