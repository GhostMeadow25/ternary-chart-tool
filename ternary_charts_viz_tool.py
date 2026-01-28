# -*- coding: utf-8 -*-
def Tlines(step, cut, cc = None, lw = None, rot_angle = 0, rot_point = [0, 0], axs_shift = [0, 0], m_factor = 1):

    """
    This function draws a triangle with grids
    cut reprenst edge cut
    S1, S2, ...., S6 tri - coordinates for the perimiter of the traingle
    LtR, RtL, TtB are tri - ccordinate going from left to right, right to left and top to bottom
    Ltr_g_x is x - values for the 2D coordinates. Saem applies for others
    bc_LtR_g_x is the 2D coordinate for the gride lines
    l_cords is the 2D coordinats for drawing gride lines
    axs_lab are the outside axes lables for the triangle  
    per are the coordinates for perimiter for the trangle
    """
#   Counting number of of points a long each cut    
    n0 = cut[0]//step
    n1 = cut[1]//step
    n2 = cut[2]//step
#   Coordinates for each segment(S) on the perimeter of the chart
    S1 = [[x, 100 - x, 0] for x in range(100 - cut[0], cut[1] - 1, - step)]
    S2 = [[cut[1] - i*step, 100 - cut[1], i*step] for i in range(n1 + 1)]
    S3 = [[0, x, 100 - x] for x in range(100 - cut[1], cut[2] - 1, - step)]
    S4 = [[i*step, cut[2] - i*step, 100 - cut[2]] for i in range(n2 + 1)]
    S5 = [[100 - x, 0, x] for x in range(100 - cut[2], cut[0] - 1, - step)]
    S6 = [[100 - cut[0], i*step, cut[0] - i*step] for i in range(n0 + 1)]
#   perim represents all of the the coordinates of the outside perimeter 
    perim = S1+S2+S3+S4+S5+S6
    perim_bc = TtB(perim)
#   Setup 2D coordinates for grid lines 
    LtR_g_x = S6[: - 1] + S1
    LtR_g_y = S4[:: - 1] + S3[:: - 1][1:]
    RtL_g_x = S1 + S2[1:]
    RtL_g_y = S5[:: - 1] + S4[:: - 1][1:]
    TtB_g_x = S5 + S6[1:]
    TtB_g_y = S3[:: - 1] + S2[:: - 1][1:]
#   Converting tri - coordinates to 2D coordinate
    bc_LtR_g_x = TtB(LtR_g_x, axs_shift, rot_angle, rot_point, m_factor)
    bc_LtR_g_y = TtB(LtR_g_y, axs_shift, rot_angle, rot_point, m_factor)
    bc_RtL_g_x = TtB(RtL_g_x, axs_shift, rot_angle, rot_point, m_factor)    
    bc_RtL_g_y = TtB(RtL_g_y, axs_shift, rot_angle, rot_point, m_factor)
    bc_TtB_g_x = TtB(TtB_g_x, axs_shift, rot_angle, rot_point, m_factor)
    bc_TtB_g_y = TtB(TtB_g_y, axs_shift, rot_angle, rot_point, m_factor)
    #print('bc_LtR_g_x',bc_LtR_g_x)
    res0 = [[a] + [b] for (a, b) in zip(bc_LtR_g_x, bc_LtR_g_y)]
    res1 = [[a] + [b] for (a, b) in zip(bc_RtL_g_x, bc_RtL_g_y)]    
    res2 = [[a] + [b] for (a, b) in zip(bc_TtB_g_x, bc_TtB_g_y)]
#   labels for the chart sides
    l_lab = [x[1] for x in S1] 
    r_lab = [x[2] for x in S3]
    t_lab = [x[0] for x in S5]
#   Axes labels-values that are listed on the sides of the charts    
    axs_labs = [l_lab, r_lab, t_lab]
#   per represents only the coordinate  of the chart's outside edges  
    per = [S1[0], S1[ - 1], S2[ - 1], S3[ - 1], S4[-1], S6[0], S1[0]]
#    print('per',per)
    per_bc = TtB(per, axs_shift, rot_angle, rot_point, m_factor)
    res = res0, res1, res2, axs_labs, per_bc, perim_bc
    
    return res
# ========================================================================
def TtB(tcords, axs_shift=(0.0, 0.0), rot_angle=0.0, rot_point=(0.0, 0.0), m_factor=1.0):
    """
    Convert ternary (L, R, T) -> XY, then apply:
      scale about rot_point → rotate about rot_point → translate by axs_shift.
    """
    # Drop zero-sum triplets and normalize each to 100               This sshould be done while reading input file**
    rows = [row for row in tcords if sum(row) != 0]
    if not rows:
        return [[], []]

    arr = np.asarray(rows, dtype=float)
    arr = 100.0 * arr / arr.sum(axis=1, keepdims=True)  # normalize to 100

    L, Rv, T = arr[:, 0], arr[:, 1], arr[:, 2]

    # Ternary to XY (equilateral orientation):
    # y = T * cos(30°) = T * sqrt(3)/2
    # x = R + y * tan(30°) = R + T/2
#    cos30 = np.sqrt(3) / 2.0
#    tan30 = 1.0 / np.sqrt(3)

    y = T * np.sqrt(3) / 2.0
    x = Rv + y * 1.0 / np.sqrt(3)

    # Apply S→R→T in one place (about rot_point)
    return Rotate_Data([x, y], rot_angle=rot_angle, rot_point=rot_point, m_factor=m_factor,  axs_shift=axs_shift)

#=========================================================================     
def Rotate_Data(coords, rot_angle=0.0, rot_point=(0.0, 0.0), m_factor=1.0, axs_shift=(0.0, 0.0)):
    """
    coords: [xs, ys] lists/arrays
    rot_angle: rotation (degrees)
    rot_point: (cx, cy) pivot in same coordinate system as coords
    m_factor: uniform or (sx, sy) scale ABOUT rot_point (not about the origin)
    axs_shift: final translation (tx, ty), applied AFTER scale+rotate (not scaled)
    """
    xs = np.asarray(coords[0], dtype=float)
    ys = np.asarray(coords[1], dtype=float)
    P = np.column_stack([xs, ys])

    cx, cy = rot_point
    sx, sy = (m_factor, m_factor) if np.isscalar(m_factor) else m_factor
    tx, ty = axs_shift

    # move pivot to origin → scale → rotate → move back → final shift
    P0 = P - np.array([cx, cy])
    P1 = P0 * np.array([sx, sy])

    th = np.deg2rad(rot_angle)
    c, s = np.cos(th), np.sin(th)
    R = np.array([[c, -s], [s,  c]])
    P2 = P1 @ R.T

    P3 = P2 + np.array([cx, cy]) + np.array([tx, ty])

    return [P3[:, 0].tolist(), P3[:, 1].tolist()]
#========================================================================= 
def Input_Data(df):
    out = {}
    df = df.copy()
    # treat blank/whitespace cells as NaN so we can detect markers cleanly
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    n_groups = df.shape[1] // 4
    for g in range(n_groups):
        sub = df.iloc[:, 4*g:4*(g+1)]
        if sub.shape[1] < 4:
            continue
        # dataset key from 4th column header
        ds_key = str(sub.columns[3]).strip() or f"Series{g}"
        # numeric triplets
        num = sub.iloc[:, :3].apply(pd.to_numeric, errors="coerce")
        if not num.notna().any(axis=1).any():
            out[ds_key] = {}
            continue
        # marker letters
        mark = sub.iloc[:, 3].astype("string").fillna("").str.strip()
        idx = np.flatnonzero(mark.to_numpy() != "")

        subsets = {}
        start = 0
        if len(idx) == 0:
            # no markers -> single subset
            rows = num.dropna(how="all").values.tolist()
            if rows:
                subsets["ALL"] = rows
        else:
            for j in idx:
                label = mark.iat[j]
                rows = num.iloc[start:j+1].dropna(how="all").values.tolist()
                if rows:
                    subsets.setdefault(label, []).extend(rows)  # append if repeats
                start = j + 1
            # include rows after the last marker under that last label
            if start < len(num):
                tail = num.iloc[start:].dropna(how="all").values.tolist()
                if tail:
                    subsets.setdefault(mark.iat[idx[-1]], []).extend(tail)
        out[ds_key] = subsets
    return out
#========================================================================= 
def Contours(ax, data_dict, tri_perim, con_level=12, cmap='Blues', 
             con_type="density", bins=None, sigma=None, norm=None, zorder=1):
    """
    Draw a density contour or heatmap inside the ternary plot perimeter.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object on which to draw the contours.
    data_dict : dict
        Dictionary where values contain x,y coordinate pairs to be plotted. 
        Keys are used to identify different data series.
    con_level : int, optional (default=12)
        Amount of contour levels to generate.
    cmap : str, optional (default='Blues')
        Matplotlib colormap name for the contour/heatmap visualization.
    tri_perim : tuple of (list, list)
        Triangle perimeter coordinates that defines the boundary contours are drawn and clipped.
    con_type : str, optional (default="density")
        Type of contour plot: "density" for contourf or "heatmap" for pcolormesh.
    bins : int or tuple of (int, int) or None, optional (default=None)
        Histogram bin specification. If int: number of bins in both x and y.
        If tuple: (nx, ny) bins. Default: 150 for density, 50 for heatmap.
    sigma : float or None, optional (default=None)
        Gaussian smoothing parameter. Higher values create smoother contours.
        Default: 8 for density, 1 for heatmap.
    norm : matplotlib.colors.Normalize or None, optional (default=None)
        Normalization instance for mapping data values to colors. If None,
        creates a new normalization from 0 to max(H).
    zorder : int or float, optional (default=1)
        Drawing order for layering elements. Higher values are drawn on top.
    
    Returns
    -------
    tuple of (mappable, colorbar, norm)
        mappable : matplotlib contour/mesh object or None
            The plotted contour (contourf) or heatmap (pcolormesh) object.
        colorbar : matplotlib.colorbar.Colorbar or None
            The colorbar object associated with the plot.
        norm : matplotlib.colors.Normalize or None
            The normalization object used for color mapping.
    
    Raises
    ------
    ValueError
        If data_dict values are not shape (N, 2).
        If tri_perim is None.
        If con_type is not "density" or "heatmap".
    """
    # Collect all points from all data series
    series = [np.asarray(v) for v in data_dict.values() if len(v)]
    if not series:
        return None, None, norm
    all_coords = np.concatenate(series, axis=0)
    if all_coords.shape[1] != 2:
        raise ValueError("data_dict values must be arrays of shape (N, 2)")
    
    # Define triangle perimeter as a closed path for clipping
    if tri_perim is None:
        raise ValueError("tri_perim=(xs, ys) is required")
    perim_xy = np.column_stack(tri_perim)
    tri_path = Path(perim_xy, closed=True)
    
    inside_mask = tri_path.contains_points(all_coords, radius=0.1)
    all_coords = all_coords[inside_mask]
    
    if len(all_coords) == 0:
        return None, None, norm
    
    x, y = all_coords[:, 0], all_coords[:, 1]
    
    # Determine grid bounds from perimeter
    x_min, x_max = perim_xy[:, 0].min(), perim_xy[:, 0].max()
    y_min, y_max = perim_xy[:, 1].min(), perim_xy[:, 1].max()

    # Set default bin counts based on contour type
    if bins is None:
        bins = 30
    if np.isscalar(bins):
        nx = ny = int(bins)
    else:
        nx, ny = map(int, bins)
        
    # Create histogram bin edges
    x_edges = np.linspace(x_min, x_max, nx + 1)
    y_edges = np.linspace(y_min, y_max, ny + 1)
    
    # Compute 2D histogram (counts in each bin)
    H, _, _ = np.histogram2d(x, y, bins=[x_edges, y_edges])
    
    # Apply Gaussian smoothing to histogram
    if sigma is None:
        sigma = 2 if con_type == "density" else 1
    if sigma and sigma > 0:
        H = gaussian_filter(H, sigma=sigma, mode='constant')
    
    # Create or use provided normalization for color mapping
    if norm is None:
        vmax = H.max()
        if vmax <= 0:
            vmax = 1.0
        norm = mpl.colors.Normalize(vmin=0.0, vmax=float(vmax))
        
    # Compute bin centers for contourf
    xc = 0.5 * (x_edges[:-1] + x_edges[1:])
    yc = 0.5 * (y_edges[:-1] + y_edges[1:])
    GXc, GYc = np.meshgrid(xc, yc, indexing='xy')
    
    # Mask bins outside the triangle using bin centers
    mask = ~tri_path.contains_points(np.c_[GXc.ravel(), GYc.ravel()]).reshape(GXc.shape)
    Z = np.ma.array(H.T, mask=mask)
    
    # Create the contour or heatmap plot
    if con_type == "density":
        # Generate contour levels
        if np.isscalar(con_level):
            con_level = int(con_level)
            con_level = max(con_level, 2)
            levels = np.linspace(norm.vmin, norm.vmax, con_level)
        else:
            levels = np.asarray(con_level)
        # Draw filled contours
        cs = ax.contourf(GXc, GYc, Z, levels=levels, cmap=cmap, norm=norm, antialiased=True, zorder=zorder)
    elif con_type == "heatmap":
        # Create mesh grid using bin edges for pcolormesh
        GXe, GYe = np.meshgrid(x_edges, y_edges, indexing='xy')
        Zp = np.ma.array(H.T, mask=mask)
        # Draw pixelated heatmap
        cs = ax.pcolormesh(GXe, GYe, Zp, cmap=cmap, norm=norm, shading='auto', zorder=zorder, rasterized=True)
    else:
        raise ValueError("con_type must be 'density' or 'heatmap'")
        
    # Clip visualization to triangle boundary
    poly = Polygon(perim_xy, closed=True, transform=ax.transData)
    cs.set_clip_path(poly)
    
    # Colorbar
    cbar = ax.figure.colorbar(cs, ax=ax, pad=0.02, fraction=0.025, label=f"{'Density' if con_type=='density' else 'Heatmap'}")
    cbar.ax.tick_params(labelsize=8)                            
    cbar.formatter = mticker.FormatStrFormatter('%.1f')  
       
    return cs, cbar, norm


#========================================================================= 
def Axis_Labels(ax, axs_labs, tick_coords, axs_shift=[0,0], rot_angle=0, rot_point=[0,0],
                m_factor=1, font_size=8):
    """
    Plot axis labels for ternary plots along the three sides of the triangle.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object on which to place the labels.
    axs_labs : list of lists
        Three lists containing label values for [left_side, right_side, top_side].
        Each inner list contains numeric or string values to display as tick labels.
    tick_coords : list of lists
        Three lists containing coordinate values corresponding to tick positions
        for [left_side, right_side, top_side]. Must match the structure of axs_labs.
    axs_shift : list of [float, float], optional (default=[0,0])
        Translation offset [x_shift, y_shift] applied to all labels.
    rot_angle : float, optional (default=0)
        Rotation angle in degrees applied to the coordinate system.
    rot_point : list of [float, float], optional (default=[0,0])
        Point [x, y] about which rotation is applied.
    m_factor : float, optional (default=1)
        Magnification/scaling factor for adjusting label spacing from the axes.
    font_size : int or float, optional (default=8)
        Font size for the axis label text.
    
    Returns
    -------
    None
        Labels are placed directly on the axes.
    
    Notes
    -----
    Labels are positioned with simple x,y offsets in screen coordinates.
    Adjust offset_x and offset_y values for each side to control positioning.
    """
    
    l_lab, r_lab, t_lab = axs_labs
    l_coords, r_coords, t_coords = tick_coords

    ang_rad = np.radians(rot_angle)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)

    # BOTTOM side labels
    for val, lc in zip(l_lab, l_coords[::-1]):
        coord = [lc, 100 - lc, 0]
        X, Y = TtB([coord], axs_shift=axs_shift, rot_angle=rot_angle,
                   rot_point=rot_point, m_factor=m_factor)
        # Offset 
        perp_x = 0
        perp_y = -4
        offset_x = (perp_x * cos_a - perp_y * sin_a) / m_factor
        offset_y = (perp_x * sin_a + perp_y * cos_a) / m_factor
        ax.text(X[0] + offset_x, Y[0] + offset_y,
                str(val), ha='center', va='center', fontsize=font_size, rotation=0)
    
    # RIGHT side labels
    for val, rc in zip(r_lab, r_coords):
        coord = [0, 100 - rc, rc]
        X, Y = TtB([coord], axs_shift=axs_shift, rot_angle=rot_angle,
                   rot_point=rot_point, m_factor=m_factor)
        # Offset
        perp_x = 5  
        perp_y = 1
        offset_x = (perp_x * cos_a - perp_y * sin_a) / m_factor
        offset_y = (perp_x * sin_a + perp_y * cos_a) / m_factor
        ax.text(X[0] + offset_x, Y[0] + offset_y,
                str(val), ha='center', va='center', fontsize=font_size, rotation=0)
    
    # LEFT side labels
    for val, tc in zip(t_lab, t_coords):
        coord = [tc, 0, 100 - tc]
        X, Y = TtB([coord], axs_shift=axs_shift, rot_angle=rot_angle,
                   rot_point=rot_point, m_factor=m_factor)
        # Offset
        perp_x = -5
        perp_y = 1
        offset_x = (perp_x * cos_a - perp_y * sin_a) / m_factor
        offset_y = (perp_x * sin_a + perp_y * cos_a) / m_factor
        ax.text(X[0] + offset_x, Y[0] + offset_y,
                str(val), ha='center', va='center', fontsize=font_size, rotation=0)

    
#=========================================================================  
def Fill_Region(ax, coords, facecolor='blue', edgecolor='black', alpha=0.3, linewidth=1):
    """
    Fill a polygonal region on the plot from given coordinates.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object on which to draw the filled region.
    coords : array-like of shape (N, 2)
        Sequence of (x, y) coordinate pairs defining the polygon vertices.
        The polygon is automatically closed between the last and first points.
    facecolor : str or color specification, optional (default='blue')
        Fill color for the interior of the polygon. Accepts matplotlib color formats.
    edgecolor : str or color specification, optional (default='black')
        Color for the polygon boundary line.
    alpha : float, optional (default=0.3)
        Transparency level from 0 (fully transparent) to 1 (fully opaque).
    linewidth : float, optional (default=1)
        Width of the polygon edge line in points.
    
    Returns
    -------
    matplotlib.patches.Polygon
        The polygon patch object that was added to the axes.
    
    Notes
    -----
    The polygon is created with closed=True, automatically connecting the last
    vertex back to the first. The returned patch can be further modified or
    removed from the axes if needed.
    """
    # Create a polygon object with the given coordinates and style
    poly = Polygon(coords, closed=True, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, linewidth=linewidth)
    # Add the shape to the plot
    ax.add_patch(poly)
    return poly


#========================================================================= 
def Draw_Segment(ax, coord1, coord2, apply_chart=None, axs_shift=[0,0], 
                 rot_angle=0, rot_point_param=[0,0], m_factor=1, linewidth=2, 
                 color='black', linestyle='-', label=None, zorder=0):
    """
    Draw a line segment between two coordinates on the plot.
    Automatically detects ternary [L, R, T] or Cartesian [x, y] based on length.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes object on which to draw the segment.
    coord1 : list or tuple
        First endpoint:
        - Length 3: [L, R, T] ternary coordinates
        - Length 2: [x, y] Cartesian coordinates
    coord2 : list or tuple
        Second endpoint in the same format as coord1.
    apply_chart : int or None, optional (default=None)
        If specified, applies the transformation settings (axs_shift, rot_angle,
        rot_point, m_factor) from the specified chart index. This overrides
        the individual transformation parameters.
    axs_shift : list of [float, float], optional (default=[0,0])
        Translation offset [x_shift, y_shift]. Ignored if apply_chart is set.
    rot_angle : float, optional (default=0)
        Rotation angle in degrees. Ignored if apply_chart is set.
    rot_point_param : list of [float, float], optional (default=[0,0])
        Point [x, y] about which rotation is applied. Ignored if apply_chart is set.
    m_factor : float, optional (default=1)
        Magnification/scaling factor. Ignored if apply_chart is set.
    linewidth : float, optional (default=2)
        Width of the line segment in points.
    color : str or color specification, optional (default='black')
        Color of the line segment.
    linestyle : str, optional (default='-')
        Line style: '-' (solid), '--' (dashed), ':' (dotted), '-.' (dash-dot).
    label : str or None, optional (default=None)
        Label for the segment (useful for legend).
    zorder : int or float, optional (default=10)
        Drawing order for layering elements.
    
    Returns
    -------
    matplotlib.lines.Line2D
        The line object that was added to the axes.
    
    Raises
    ------
    ValueError
        If apply_chart index is out of range.
    
    Examples
    --------
    # Use chart 1's transformations
    Draw_Segment(ax, [30, 50, 20], [50, 30, 20], apply_chart=0, color='red')
    
    # Use custom transformations
    Draw_Segment(ax, [25.5, 15.0], [45.2, 30.8], rot_angle=90, color='blue')
    """
    # Apply chart transformations if specified
    if apply_chart is not None:
        if apply_chart < 0 or apply_chart >= len(axs_shifts):
            raise ValueError(f"apply_chart={apply_chart} is out of range. "
                           f"Valid range is 0 to {len(axs_shifts)-1}")
        axs_shift = axs_shifts[apply_chart]
        rot_angle = rot_angles[apply_chart]
        rot_point_to_use = rot_point
        m_factor = m_factors[apply_chart]
    else:
        rot_point_to_use = rot_point_param
    
    # Check coordinate lengths
    len1 = len(coord1)
    len2 = len(coord2)
    
    if len1 != len2:
        raise ValueError(f"coord1 and coord2 must have the same length. "
                        f"Got {len1} and {len2}")
    
    if len1 == 3:
        # Ternary coordinates 
        coords = [coord1, coord2]
        xy = TtB(coords, axs_shift=axs_shift, rot_angle=rot_angle, 
                 rot_point=rot_point_to_use, m_factor=m_factor)
        x_vals = xy[0]
        y_vals = xy[1]
        
    elif len1 == 2:
        # Cartesian coordinates
        coords = [[coord1[0], coord2[0]], [coord1[1], coord2[1]]]
        xy = Rotate_Data(coords, rot_angle=rot_angle, rot_point=rot_point_to_use, 
                        m_factor=m_factor, axs_shift=axs_shift)
        x_vals = xy[0]
        y_vals = xy[1]
        
    else:
        raise ValueError(f"Coordinates must be length 2 (Cartesian) or 3 (ternary). "
                        f"Got length {len1}")
    
    # Draw the line segment
    line = ax.plot(x_vals, y_vals, linewidth=linewidth, color=color, 
                   linestyle=linestyle, label=label, zorder=zorder)[0]
    
    return line


#=========================================================================
def Additional_Label(text, coords, apply_chart=None, rotation=0, rot_point_param=(0, 0), 
                     rot_angle_param=0, fontsize=10, color='black', 
                     ha='center', va='center', **kwargs):
    """
    Place labels anywhere in the plot with optional rotation.
    
    Parameters
    ----------
    text : str
        The text string to display as a label.
    coords : list/tuple of length 2 or 3
        The coordinates where the label will be placed:
        - Length 3: [A, B, C] ternary coordinates
        - Length 2: (x, y) Cartesian coordinates
    apply_chart : int or None, optional (default=None)
        If specified, applies the transformation settings (rot_angle, rot_point)
        from the specified chart index. This overrides rot_angle_param and rot_point_param.
        Uses global variables: rot_angles, rot_point
    rotation : float, optional (default=0)
        Text rotation angle in degrees. Rotates the text itself (not the position).
    rot_point_param : tuple of (float, float), optional (default=(0, 0))
        Point (x, y) about which coordinate rotation is applied.
        Ignored if apply_chart is set.
    rot_angle_param : float, optional (default=0)
        Rotation angle in degrees applied to the label's position coordinates.
        Ignored if apply_chart is set.
    fontsize : int or float, optional (default=10)
        Font size for the label text.
    color : str or color specification, optional (default='black')
        Color of the label text. Accepts matplotlib color formats.
    ha : str, optional (default='center')
        Horizontal alignment: 'left', 'center', or 'right'.
    va : str, optional (default='center')
        Vertical alignment: 'top', 'center', or 'bottom'.
    **kwargs : dict
        Additional keyword arguments passed to plt.text() for advanced styling
        (e.g., weight, style, bbox, alpha).
    
    Returns
    -------
    None
        Label is placed directly on the current plot.
    
    Raises
    ------
    ValueError
        If apply_chart index is out of range, or if coords length is invalid,
        or if ternary coordinates don't sum to 100.
    
    Examples
    --------
    # Use Cartesian coordinates with chart 0's transformations
    Additional_Label("My Label", (50, 50), apply_chart=0)
    
    # Use custom transformations with Cartesian coords
    Additional_Label("Custom", (25, 75), rot_angle_param=45, rotation=30)
    """
    # Apply chart transformations if specified
    if apply_chart is not None:
        if apply_chart < 0 or apply_chart >= len(rot_angles):
            raise ValueError(f"apply_chart={apply_chart} is out of range. "
                           f"Valid range is 0 to {len(rot_angles)-1}")
        rot_angle_to_use = rot_angles[apply_chart]
        rot_point_to_use = rot_point
        axs_shift_to_use = axs_shifts[apply_chart]
        m_factor_to_use = m_factors[apply_chart]
    else:
        rot_angle_to_use = rot_angle_param
        rot_point_to_use = rot_point_param
        axs_shift_to_use = (0, 0)
        m_factor_to_use = 1
    
    # Check coordinate length and convert if needed
    coord_len = len(coords)
    
    if coord_len == 3:
        # Ternary coordinates
        coord_sum = sum(coords)
        if not (99.9 <= coord_sum <= 100.1):  # Allow small floating point errors
            raise ValueError(f"Ternary coordinates must sum to 100, got {coord_sum}")
        
        # Convert ternary [A, B, C] to Cartesian using TtB
        # TtB expects a list of points, so wrap in list and extract result
        ternary_points = [coords]
        xy = TtB(ternary_points, axs_shift=axs_shift_to_use, rot_angle=rot_angle_to_use,
                 rot_point=rot_point_to_use, m_factor=m_factor_to_use)
        x, y = xy[0][0], xy[1][0]
        
    elif coord_len == 2:
        # Cartesian coordinates
        x, y = coords
        # Apply transformations to the label position
        if rot_angle_to_use != 0 or axs_shift_to_use != (0, 0) or m_factor_to_use != 1:
            rotated = Rotate_Data([[x], [y]], rot_angle=rot_angle_to_use, 
                                 rot_point=rot_point_to_use, m_factor=m_factor_to_use,
                                 axs_shift=axs_shift_to_use)
            x, y = rotated[0][0], rotated[1][0]
    else:
        raise ValueError(f"Coordinates must be length 2 (Cartesian) or 3 (ternary). "
                        f"Got length {coord_len}")
    
    # Place the label text
    filtered_kwargs = {k: v for k, v in kwargs.items() 
                      if k not in ['rot_point', 'rot_angle', 'rot_point_param', 
                                   'rot_angle_param', 'axs_shift', 'm_factor']}
    
    plt.text(x, y, text, rotation=rotation, fontsize=fontsize, color=color, 
             ha=ha, va=va, **filtered_kwargs)


#========================================================================= 
def Corner_Labels(axs, per_bc, fontsize=13, fontweight="bold", zorder=50):
    """
    Add letter labels to all unique corner points created by cuts.
    
    Parameters
    ----------
    axs : matplotlib.axes.Axes
        The axes object on which to place the corner labels.
    per_bc : tuple of (list, list)
        Perimeter boundary coordinates as (x_coords, y_coords). The last point
        is assumed to be a duplicate of the first (closing the perimeter) and
        is excluded before processing.
    fontsize : int or float, optional (default=13)
        Font size for the corner label letters.
    fontweight : str or int, optional (default="bold")
        Font weight specification: 'normal', 'bold', 'light', or numeric values
        from 100-900.
    zorder : int or float, optional (default=50)
        Drawing order for layering. Higher values draw on top of other elements.
    
    Returns
    -------
    None
        Labels are placed directly on the axes.
    
    Notes
    -----
    Corner points are identified by extracting unique (x, y) coordinate pairs
    from the perimeter. Labels are assigned alphabetically starting with 'A'
    based on sorted coordinate positions. This ensures consistent labeling
    across multiple plots with the same geometry.
    """
    xs, ys = per_bc

    xs = xs[:-1]
    ys = ys[:-1]

    corners = list(set(zip(xs, ys)))
    corners.sort()

    for j, (x, y) in enumerate(corners):
        label = chr(ord("A") + j)
        axs.text(x, y, label, ha="center", va="center", fontsize=fontsize,
            fontweight=fontweight, zorder=zorder)
        
#========================================================================= 
"""
This is the main program where functions are called and excuted
"""
import math as ma
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
import matplotlib as mpl
import sys
from scipy.ndimage import gaussian_filter
from matplotlib.path import Path
from matplotlib.patches import Polygon

myfile = "Data_Example.csv"
df = pd.read_csv(myfile)

# Default data for charts
steps = [10, 5, 10, 10]
cuts = [[10, 20, 10], [30, 30, 30], [0, 30, 0], [0, 0, 0]]
axs_shifts = [[50, 10], [200, 0], [330, 0], [450, 0]]
rot_angles = [60, 180, 0, 0]
m_factors = [1, 1.5, .6, 1]
l_widths = [.2, .3, .2, .4]
l_colors = ['blue', 'black', 'red', 'green']
c_maps = ['Blues', 'Greys', 'Reds', 'Reds']
con_levels = [12,10,10,5]
con_types = ['density','density','density','density']           
con_choices = ['no','no','yes','no']                           
show_axis_labels = ['no', 'yes', 'no', 'no'] 
corner_labels = ['no', 'no', 'yes', 'no']  

rot_point = [50.00, 50*ma.sqrt(3)/3]            # coordinate of the rotation point which is the center of the chart 

# Checks for data compatibility 
flat_cuts = [x[i] for x in cuts for i in range(len(x))] 
if(any([i in [1,2,5,10] for i in steps])) == False:
    print('steps must be in 1,2,5,10')
    sys.exit()
elif(min(flat_cuts) < 0 or max(flat_cuts) > 50):
    print('cuts must be positive and between 0 and 50 inclusive')
    sys.exit()
elif(any(0 <= i <= 180 for i in rot_angles)) == False:
    print('rotation angles must be between 0 and 180')
    sys.exit()
elif(any(0 <= i <= 1 for i in m_factors)) == False:
    print('magnification factor must be 0 < m_factor =< 1')
    sys.exit()

fig, axs =  plt.subplots(figsize = (8, np.cos(np.pi/30)*8))
sets = Input_Data(df)

# Marker styles
markers = ['o', 's', '^', 'D', 'x', '*', 'P', 'v', 'H', '+']
series_colors = ['green', 'purple', 'orange', 'cyan', 'pink', 'gray', 'olive', 'brown']

# Number of subsets (a, b, c) on each chart
total_subkeys = sum(len(sub_dict) for sub_dict in sets.values())
for i, (set_name, sub_dict) in enumerate(sets.items()):
    res = Tlines(steps[i], cuts[i], axs_shift=axs_shifts[i], rot_angle=rot_angles[i],
                 rot_point=rot_point, m_factor=m_factors[i])
    res0, res1, res2, axs_labs, per_bc, perim_bc = res
    marker_map = {key: markers[j % len(markers)] for j, key in enumerate(sub_dict)}
    color_map = {key: series_colors[j % len(series_colors)] for j, key in enumerate(sub_dict)}
    axs.set_aspect('equal')
    perim_path = Path(np.column_stack([per_bc[0], per_bc[1]]), closed=True)
    
    for j in range(len(res) - 3):
        axs.plot(res[j][0], res[j][1], marker='', linestyle='-', 
             linewidth=l_widths[i], color=l_colors[j])
    sub_dict_full = {}
    for key, points in sub_dict.items():
        points = TtB(points, rot_angle = rot_angles[i], axs_shift = axs_shifts[i], 
                     rot_point = rot_point, m_factor = m_factors[i])
        x_vals = np.array(points[0])
        y_vals = np.array(points[1])
        sub_dict_full[key] = np.column_stack([x_vals, y_vals])
        coords = np.column_stack([x_vals, y_vals])
        mask = perim_path.contains_points(coords, radius=0.1)
        x_vals_filtered = x_vals[mask]
        y_vals_filtered = y_vals[mask]
        axs.scatter(x_vals_filtered, y_vals_filtered, marker=marker_map[key], 
            linewidth=l_widths[i], color=color_map[key], s=50)
    axs.set_axis_off()
    axs.plot(res[4][0], res[4][1], marker = '', linestyle = '-', linewidth = 1.5, color = 'blue', zorder=0)
    
    if con_choices[i] == 'yes': 
        Contours(ax=axs, data_dict=sub_dict_full, tri_perim=[per_bc[0], per_bc[1]],
                 con_level=con_levels[i], cmap=c_maps[i], con_type=con_types[i])
    
    if show_axis_labels[i] == 'yes':
        tick_coords = axs_labs
        
        Axis_Labels(axs, axs_labs=axs_labs, tick_coords=tick_coords,
            axs_shift=axs_shifts[i], rot_angle=rot_angles[i],
            rot_point=rot_point, m_factor=m_factors[i], font_size=8)
    
    if corner_labels[i] == "yes":
        Corner_Labels(axs, per_bc)
       
    Draw_Segment(axs, [90, 10, 0], [90, 0, 10], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [10, 90, 0], [0, 90, 10], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [0, 10, 90], [10, 0, 90], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [0, 60, 40], [60, 0, 40], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [90, 5, 5], [5, 90, 5], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [5, 90, 5], [5, 5, 90], apply_chart=3, color='black', linewidth=1)
    Draw_Segment(axs, [5, 5, 90], [90, 5, 5], apply_chart=3, color='black', linewidth=1)

    Additional_Label("Opx", (-10, -3), apply_chart=3, fontsize=10, color='black')
    Additional_Label("OI", (50, 93), apply_chart=3, fontsize=10, color='black')
    Additional_Label("Cpx", (110, -3), apply_chart=3, fontsize=10, color='black')
    Additional_Label("E", [50, 50], apply_chart=3, fontsize=10, color='black')
    Additional_Label("D", [50, 18], apply_chart=3, fontsize=10, color='black')
    
plt.show()