# Tutorial: Using Ter_Charts-py

This tutorial walks through common use cases step by step, using the included `Data_Example.csv` file. By the end, you will know how to produce a single ternary chart, a multi-chart figure, and a chart with a contour or heatmap overlay.

---

## Prerequisites

Make sure you have completed the installation steps in [README.md](README.md) before proceeding.

---

## A Note on File Paths for Windows Users

When setting the `myfile` variable to your CSV file path, Windows users should be aware that copied file paths use single backslashes (`\`), which Python treats as escape characters. To avoid errors, use one of the following formats:

**Option 1 — Double backslashes:**

```python
myfile = "C:\\Users\\Lily\\Documents\\data.csv"
```

**Option 2 — Raw string (prefix with `r`):**

```python
myfile = r"C:\Users\Lily\Documents\data.csv"
```

**Option 3 — Forward slashes (also works on Windows):**

```python
myfile = "C:/Users/Lily/Documents/data.csv"
```

Mac and Linux users can copy and paste their paths without any changes.

---

## Tutorial 1: Running the Example Out of the Box

The repository includes a ready-to-run example. To try it immediately:

```bash
python ternary_charts_viz_tool.py
```

This loads `Data_Example.csv` and produces a figure with four ternary charts using the default configuration. You should see a matplotlib window with multiple charts displayed side by side, each with different rotation, scale, and grid settings.

### Important: Before Continuing to Tutorials 2–6

The bottom of `ternary_charts_viz_tool.py` contains several `Draw_Segment` and `Additional_Label` calls that are part of the four-chart example in Tutorial 1. These lines reference `apply_chart=3` (the fourth chart), so they will cause an error if you run the script with fewer than four charts.

Before working through Tutorials 2–6, comment out those lines by placing a `#` at the start of each one:

```python
# Draw_Segment(axs, [90, 10, 0], [90, 0, 10], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [10, 90, 0], [0, 90, 10], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [0, 10, 90], [10, 0, 90], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [0, 60, 40], [60, 0, 40], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [90, 5, 5], [5, 90, 5], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [5, 90, 5], [5, 5, 90], apply_chart=3, color='black', linewidth=1)
# Draw_Segment(axs, [5, 5, 90], [90, 5, 5], apply_chart=3, color='black', linewidth=1)
# Additional_Label("Opx", (-10, -3), apply_chart=3, fontsize=10, color='black')
# Additional_Label("OI", (50, 93), apply_chart=3, fontsize=10, color='black')
# Additional_Label("Cpx", (110, -3), apply_chart=3, fontsize=10, color='black')
# Additional_Label("E", [50, 50], apply_chart=3, fontsize=10, color='black')
# Additional_Label("D", [50, 18], apply_chart=3, fontsize=10, color='black')
```

You can uncomment them again any time you want to run the full four-chart example.

---

## Tutorial 2: Creating a Single Ternary Chart

This is the minimal setup for one chart with one dataset.

**Step 1 — Use the included sample file.**

The file `ternary_tutorial_single_chart.csv` is included in the repository for this tutorial. It contains the following data:

```
L0,R0,T0,Series0
40,40,20,a
30,50,20,a
50,30,20,a
20,60,20,b
60,20,20,b
```

- `L0`, `R0`, `T0` are the three ternary components (left, right, top). Each row must sum to 100.
- `Series0` contains a letter label for each data subset. Rows sharing the same letter are plotted with the same marker.

**Step 2 — Edit `ternary_charts_viz_tool.py`.**

Find and update these variables near the bottom of the file:

```python
myfile = "ternary_tutorial_single_chart.csv"     # path to your CSV

steps            = [10]          # grid interval
cuts             = [[0, 0, 0]]   # no edge cuts
axs_shifts       = [[0, 0]]      # no translation
rot_angles       = [0]           # no rotation
m_factors        = [1]           # no scaling
l_widths         = [0.3]         # gridline width
l_colors         = ['black']     # gridline color
c_maps           = ['Blues']
con_levels       = [10]
con_types        = ['density']
con_choices      = ['no']        # no contour overlay
show_axis_labels = ['yes']       # show tick labels on chart sides
corner_labels    = ['no']
```

**Step 3 — Run the script.**

```bash
python ternary_charts_viz_tool.py
```

You will see a single equilateral triangle with your data points plotted. Points belonging to subset `a` and subset `b` will appear with different markers and colors automatically.

---

## Tutorial 3: Multiple Charts in One Figure

Ter_Charts-py supports up to four charts in a single figure. Each chart is independently positioned and styled.

**Step 1 — Use the included sample file.**

The file `ternary_tutorial_two_charts.csv` is included in the repository for this tutorial. It contains the following data:

```
L0,R0,T0,Series0,L1,R1,T1,Series1
40,40,20,a,60,20,20,a
30,50,20,a,20,60,20,a
50,30,20,b,50,30,20,b
```

Each group of four columns (L, R, T, Series) defines one chart. The column headers must follow the pattern `L0,R0,T0,Series0`, `L1,R1,T1,Series1`, etc.

**Step 2 — Update the configuration lists to have two entries (one per chart).**

```python
myfile = "ternary_tutorial_two_charts.csv"

steps            = [10, 5]
cuts             = [[0, 0, 0], [0, 0, 0]]
axs_shifts       = [[0, 0], [200, 0]]      # shift chart 2 to the right
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

## Tutorial 4: Adding a Contour or Heatmap Overlay

You can overlay a density contour or heatmap on any chart by changing two parameters.

**Density contour:**

```python
con_choices = ['yes']       # enable overlay for chart 1
con_types   = ['density']   # contour type
con_levels  = [12]          # number of contour levels
c_maps      = ['Blues']     # colormap
```

**Heatmap:**

```python
con_choices = ['yes']
con_types   = ['heatmap']
c_maps      = ['Reds']
```

Run the script. A colored overlay will appear inside the triangle, clipped to the chart boundary, with an automatic colorbar.

---

## Tutorial 5: Rotating and Scaling a Chart

Each chart can be rotated and scaled independently.

```python
rot_angles = [0, 180]            # second chart is flipped 180 degrees
m_factors  = [1, 0.6]            # second chart is scaled to 60% of original size
axs_shifts = [[0, 0], [300, 50]] # reposition the scaled chart
```

Rotation is always applied around the center of the chart, defined as:

```python
rot_point = [50.00, 50 * math.sqrt(3) / 3]
```

This value is fixed in the script and does not need to be changed for standard use.

---

## Tutorial 6: Using Edge Cuts

Edge cuts trim the corners of a triangle to zoom in on a specific region. They are specified per chart as `[left_cut, right_cut, top_cut]`, where each value is between 0 and 50.

```python
cuts = [[20, 20, 0]]    # cut 20 units from the left and right corners
```

This is useful when data are concentrated in a particular region and you want to expand that area without changing the underlying data.

---

## Next Steps

For a complete reference of all parameters and the CSV input format, see [README.md](README.md).
