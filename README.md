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
- numpy>=1.24.0
- matplotlib>=3.7.0
- pandas>=2.0.0
- scipy>=1.10.0

## Repository Contents

| File | Description |
|------|-------------|
| `ternary_charts_viz_tool.py` | Main script containing all functions and execution logic |
| `Data_Example.csv` | Example input dataset for testing and demonstration |
| `requirements.txt` | Python package dependencies |
| `ternary_tutorial_single_chart.csv` | Sample dataset for Tutorial 2 (single chart) |
| `ternary_tutorial_two_charts.csv` | Sample dataset for Tutorial 3 (two charts) |
| `LICENSE` | MIT License |

---

## Quick Start

1. Open your IDE or use a Jupyter Notebook in your browser.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Place your data in a CSV file following the format described in the [Input](#input) section below.
4. Open `ternary_charts_viz_tool.py` and set the `myfile` variable to your CSV file path.
5. Adjust the configuration parameters (steps, cuts, rotations, etc.) as needed.
6. Run the script:
   ```
   python ternary_charts_viz_tool.py
   ```

A matplotlib figure window will open displaying your ternary chart(s), or it will appear inline. **To run the included example immediately, no changes are needed** — the script is pre-configured to load `Data_Example.csv`.

---

## Tutorials

### A Note on File Paths for Windows Users

When setting the `myfile` variable, Windows users should be aware that copied file paths use single backslashes (`\`), which Python treats as escape characters. Use one of the following formats instead:

```python
# Option 1 — Double backslashes
myfile = "C:\\Users\\username\\Documents\\data.csv"

# Option 2 — Raw string
myfile = r"C:\Users\username\Documents\data.csv"

# Option 3 — Forward slashes (also works on Windows)
myfile = "C:/Users/username/Documents/data.csv"
```

Mac and Linux users can copy and paste paths without any changes.

---

### Tutorial 1: Running the Example Out of the Box

The repository includes a ready-to-run example. To try it immediately:

```
python ternary_charts_viz_tool.py
```

This loads `Data_Example.csv` and produces a figure with four ternary charts using the default configuration. You should see a matplotlib window with multiple charts displayed side by side, each with different rotation, scale, and grid settings.

> **Important — Before Continuing to Tutorials 2–6:**
> The bottom of `ternary_charts_viz_tool.py` contains several `Draw_Segment` and `Additional_Label` calls that reference `apply_chart=3` (the fourth chart). These will cause an error if you run the script with fewer than four charts. Before working through Tutorials 2–6, comment them out by placing a `#` at the start of each line:
>
> ```python
> # Draw_Segment(axs, [90, 10, 0], [90, 0, 10], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [10, 90, 0], [0, 90, 10], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [0, 10, 90], [10, 0, 90], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [0, 60, 40], [60, 0, 40], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [90, 5, 5], [5, 90, 5], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [5, 90, 5], [5, 5, 90], apply_chart=3, color='black', linewidth=1)
> # Draw_Segment(axs, [5, 5, 90], [90, 5, 5], apply_chart=3, color='black', linewidth=1)
> # Additional_Label("Opx", (-10, -3), apply_chart=3, fontsize=10, color='black')
> # Additional_Label("OI", (50, 93), apply_chart=3, fontsize=10, color='black')
> # Additional_Label("Cpx", (110, -3), apply_chart=3, fontsize=10, color='black')
> # Additional_Label("E", [50, 50], apply_chart=3, fontsize=10, color='black')
> # Additional_Label("D", [50, 18], apply_chart=3, fontsize=10, color='black')
> ```
> You can uncomment them again any time you want to run the full four-chart example.

---

### Tutorial 2: Creating a Single Ternary Chart

**Step 1 — Use the included sample file.**

The file `ternary_tutorial_single_chart.csv` is included in the repository. It contains the following data:

```
L0,R0,T0,Series0
40,40,20,a
30,50,20,a
50,30,20,a
20,60,20,b
60,20,20,b
```

`L0`, `R0`, `T0` are the three ternary components (left, right, top). Each row must sum to 100. `Series0` contains a letter label for each data subset — rows sharing the same letter are plotted with the same marker.

**Step 2 — Edit `ternary_charts_viz_tool.py`.**

Find and update these variables near the bottom of the file:

```python
myfile = "ternary_tutorial_single_chart.csv"

steps            = [10]
cuts             = [[0, 0, 0]]
axs_shifts       = [[0, 0]]
rot_angles       = [0]
m_factors        = [1]
l_widths         = [0.3]
l_colors         = ['black']
c_maps           = ['Blues']
con_levels       = [10]
con_types        = ['density']
con_choices      = ['no']
show_axis_labels = ['yes']
corner_labels    = ['no']
```

**Step 3 — Run the script.**

```
python ternary_charts_viz_tool.py
```

You will see a single equilateral triangle with your data points plotted. Points belonging to subset `a` and subset `b` will appear with different markers and colors automatically.

---

### Tutorial 3: Multiple Charts in One Figure

Ter_Charts-py supports up to four charts in a single figure. Each chart is independently positioned and styled.

**Step 1 — Use the included sample file.**

The file `ternary_tutorial_two_charts.csv` contains the following data:

```
L0,R0,T0,Series0,L1,R1,T1,Series1
40,40,20,a,60,20,20,a
30,50,20,a,20,60,20,a
50,30,20,b,50,30,20,b
```

Each group of four columns (`L`, `R`, `T`, `Series`) defines one chart.

**Step 2 — Update the configuration lists to have two entries (one per chart).**

```python
myfile = "ternary_tutorial_two_charts.csv"

steps            = [10, 5]
cuts             = [[0, 0, 0], [0, 0, 0]]
axs_shifts       = [[0, 0], [200, 0]]
rot_angles       = [0, 0]
m_factors        = [1, 1]
l_widths         = [0.3, 0.3]
l_colors         = ['black', 'black']
c_maps           = ['Blues', 'Reds']
con_levels       = [10, 10]
con_types        = ['density', 'density']
con_choices      = ['no', 'no']
show_axis_labels = ['yes', 'yes']
corner_labels    = ['no', 'no']
```

**Step 3 — Run the script.** Two charts will appear side by side in the same figure.

---

### Tutorial 4: Adding a Contour or Heatmap Overlay

Overlay a density contour or heatmap on any chart by changing two parameters.

**Density contour:**
```python
con_choices = ['yes']
con_types   = ['density']
con_levels  = [12]
c_maps      = ['Blues']
```

**Heatmap:**
```python
con_choices = ['yes']
con_types   = ['heatmap']
c_maps      = ['Reds']
```

Run the script. A colored overlay will appear inside the triangle, clipped to the chart boundary, with an automatic colorbar.

---

### Tutorial 5: Rotating and Scaling a Chart

Each chart can be rotated and scaled independently.

```python
rot_angles = [0, 180]             # second chart is flipped 180 degrees
m_factors  = [1, 0.6]             # second chart is scaled to 60% of original size
axs_shifts = [[0, 0], [300, 50]]  # reposition the scaled chart
```

Rotation is always applied around the center of the chart:

```python
rot_point = [50.00, 50 * math.sqrt(3) / 3]
```

This value is fixed in the script and does not need to be changed for standard use.

---

### Tutorial 6: Using Edge Cuts

Edge cuts trim the corners of a triangle to zoom in on a specific region. They are specified per chart as `[left_cut, right_cut, top_cut]`, where each value is between 0 and 50.

```python
cuts = [[20, 20, 0]]    # cut 20 units from the left and right corners
```

This is useful when data are concentrated in a particular region and you want to expand that area without changing the underlying data.

---

## Input

### CSV Data File

Input data is provided as a comma-separated values (CSV) file. The file can contain up to four datasets (one per chart), each occupying four columns.

| Column | Name | Description |
|--------|------|-------------|
| 1 | L0 | Left component of dataset 0 (numeric) |
| 2 | R0 | Right component of dataset 0 (numeric) |
| 3 | T0 | Top component of dataset 0 (numeric) |
| 4 | Series0 | Subset label for dataset 0 (single letter, e.g. a, b, c) |
| 5 | L1 | Left component of dataset 1 |
| ... | ... | Pattern continues for datasets 1, 2, and 3 |

- Each row's three numeric values (L, R, T) must sum to 100. If they do not, the tool normalizes them automatically.
- The Series column assigns each row to a named subset. Rows sharing the same letter are plotted with the same marker and color.
- Datasets do not need to have the same number of rows. Empty cells in shorter datasets are ignored.
- Only data to be plotted should be included in the file; no extra formatting or summary rows.

### Setting the File Path

At the bottom of `ternary_charts_viz_tool.py`, set the `myfile` variable to the path of your CSV file:

```python
myfile = "Data_Example.csv"     # relative or absolute path
```

---

## Configuration Parameters

All configuration parameters are Python lists. Each list must contain one entry per chart.

### `steps`
**Type:** list of int | **Valid values:** 1, 2, 5, or 10

The gridline interval for each chart, expressed as a percentage.

```python
steps = [10, 5, 10, 10]
```

### `cuts`
**Type:** list of list of int, each inner list is `[left_cut, right_cut, top_cut]` | **Valid values:** 0 to 50

Trims the corners of the triangle. Useful for zooming in on densely populated regions.

```python
cuts = [[10, 20, 10], [30, 30, 30], [0, 30, 0], [0, 0, 0]]
```

### `axs_shifts`
**Type:** list of list of float, each inner list is `[x_shift, y_shift]`

Translates each chart horizontally and vertically within the figure.

```python
axs_shifts = [[50, 10], [200, 0], [330, 0], [450, 0]]
```

### `rot_angles`
**Type:** list of float | **Valid values:** 0 to 180

Rotation angle in degrees for each chart.

```python
rot_angles = [60, 180, 0, 0]
```

### `m_factors`
**Type:** list of float | **Valid values:** greater than 0 and up to 1

Scale factor for each chart.

```python
m_factors = [1, 1.5, 0.6, 1]
```

### `l_widths`
**Type:** list of float

Line width of the gridlines for each chart.

```python
l_widths = [0.2, 0.3, 0.2, 0.4]
```

### `l_colors`
**Type:** list of str

Color of the gridlines. Accepts any matplotlib color string.

```python
l_colors = ['blue', 'black', 'red', 'green']
```

### `c_maps`
**Type:** list of str

Matplotlib colormap name for contour or heatmap overlays. Only active when `con_choices` is `'yes'`.

```python
c_maps = ['Blues', 'Greys', 'Reds', 'Reds']
```

### `con_levels`
**Type:** list of int

Number of contour levels. Only active when `con_choices` is `'yes'` and `con_types` is `'density'`.

```python
con_levels = [12, 10, 10, 5]
```

### `con_types`
**Type:** list of str | **Valid values:** `'density'` or `'heatmap'`

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

```python
show_axis_labels = ['no', 'yes', 'no', 'no']
```

### `corner_labels`
**Type:** list of str | **Valid values:** `'yes'` or `'no'`

Whether to draw alphabetical labels (A, B, C, ...) at the corner points created by edge cuts.

```python
corner_labels = ['no', 'no', 'yes', 'no']
```

---

## Adding Custom Annotations

Three functions are available for adding custom overlays to your charts. Call them at the bottom of the script, after the main loop, using the same pattern as the examples in Tutorial 1.

---

### `Draw_Segment`

Draws a line segment between two points. Coordinates can be ternary `[L, R, T]` or Cartesian `[x, y]` — the function detects which automatically based on length.

```python
Draw_Segment(ax, coord1, coord2, apply_chart=None, linewidth=2,
             color='black', linestyle='-', label=None)
```

| Parameter | Description |
|-----------|-------------|
| `ax` | The axes object (use `axs`) |
| `coord1` | Start point: `[L, R, T]` ternary or `[x, y]` Cartesian |
| `coord2` | End point in the same format as `coord1` |
| `apply_chart` | Chart index (0-based) whose transformations to use. If `None`, no transformations are applied |
| `linewidth` | Line width in points (default: 2) |
| `color` | Line color — any matplotlib color string (default: `'black'`) |
| `linestyle` | `'-'` solid, `'--'` dashed, `':'` dotted, `'-.'` dash-dot (default: `'-'`) |
| `label` | Optional label string for use in a legend |

**Examples:**
```python
# Line between two ternary points on chart 0
Draw_Segment(axs, [30, 50, 20], [50, 30, 20], apply_chart=0, color='red')

# Dashed line using Cartesian coordinates
Draw_Segment(axs, [25.5, 15.0], [45.2, 30.8], apply_chart=0, linestyle='--', color='blue')
```

---

### `Additional_Label`

Places a text label anywhere on the plot. Coordinates can be ternary `[L, R, T]` or Cartesian `(x, y)`.

```python
Additional_Label(text, coords, apply_chart=None, rotation=0,
                 fontsize=10, color='black', ha='center', va='center', **kwargs)
```

| Parameter | Description |
|-----------|-------------|
| `text` | The string to display |
| `coords` | Position: `[L, R, T]` ternary or `(x, y)` Cartesian |
| `apply_chart` | Chart index (0-based) whose transformations to use |
| `rotation` | Rotation of the text itself in degrees (default: 0) |
| `fontsize` | Font size (default: 10) |
| `color` | Text color (default: `'black'`) |
| `ha` | Horizontal alignment: `'left'`, `'center'`, or `'right'` (default: `'center'`) |
| `va` | Vertical alignment: `'top'`, `'center'`, or `'bottom'` (default: `'center'`) |
| `**kwargs` | Any additional `plt.text()` keyword arguments (e.g., `weight`, `bbox`) |

**Examples:**
```python
# Label at a ternary position on chart 0
Additional_Label("Feldspar", [60, 20, 20], apply_chart=0, fontsize=9, color='darkred')

# Label at a Cartesian position with bold text
Additional_Label("Region A", (50, 50), apply_chart=0, weight='bold')
```

---

### `Fill_Region`

Fills a polygonal region with a color. Coordinates must be Cartesian `(x, y)` pairs — convert ternary coordinates first using `TtB()` if needed.

```python
Fill_Region(ax, coords, facecolor='blue', edgecolor='black', alpha=0.3, linewidth=1)
```

| Parameter | Description |
|-----------|-------------|
| `ax` | The axes object (use `axs`) |
| `coords` | List of `(x, y)` pairs defining the polygon vertices |
| `facecolor` | Fill color (default: `'blue'`) |
| `edgecolor` | Border color (default: `'black'`) |
| `alpha` | Opacity from 0 (transparent) to 1 (opaque) (default: 0.3) |
| `linewidth` | Border line width in points (default: 1) |

**Example:**
```python
# Convert ternary corners to Cartesian, then fill
p1 = TtB([[40, 40, 20]], axs_shift=axs_shifts[0], rot_angle=rot_angles[0],
          rot_point=rot_point, m_factor=m_factors[0])
p2 = TtB([[60, 20, 20]], axs_shift=axs_shifts[0], rot_angle=rot_angles[0],
          rot_point=rot_point, m_factor=m_factors[0])
p3 = TtB([[20, 60, 20]], axs_shift=axs_shifts[0], rot_angle=rot_angles[0],
          rot_point=rot_point, m_factor=m_factors[0])

coords = [(p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (p3[0][0], p3[1][0])]
Fill_Region(axs, coords, facecolor='yellow', edgecolor='black', alpha=0.4)
```

---

## Output

The script produces matplotlib figure(s). To save to a file, add the following line before `plt.show()` in the script:

```python
plt.savefig("output.png", dpi=300, bbox_inches='tight')
```

Supported formats include PNG, PDF, SVG, and EPS.

---

## Expected Behavior and Validation

The script performs basic validation before plotting and exits with an informative message if any of the following conditions are violated:

- `steps` values must be in {1, 2, 5, 10}
- `cuts` values must be between 0 and 50 inclusive
- `rot_angles` values must be between 0 and 180 inclusive
- `m_factors` values must be greater than 0 and no greater than 1

Data points that fall outside the triangle boundary after applying cuts are automatically filtered and not plotted. Rows with all three components equal to zero are silently skipped. Rows that do not sum to 100 are normalized automatically.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Authors

EK Esawi and Lily Meadow, Eastern Oregon University
