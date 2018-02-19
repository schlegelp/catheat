#    This script is part of pymaid (http://www.github.com/schlegelp/catheat).
#    Copyright (C) 2017 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

def heatmap(data, cmap={}, palette='hls', ax=None, legend=True, leg_pos='right', **sns_kws):
    """ Class to plot categorical heatmap using seaborn.

    Parameters
    ----------
    data :      rectangular dataset
                2D dataset that can be coerced into an ndarray. If a Pandas
                DataFrame is provided, the index/column information will be
                used to label the columns and rows.
    cmap :      dict, optional
                Colors for each category in the dataset. Missing colors will
                be added from the palette.
    palette :   matplotlib/seaborn color palette name or object
    ax :        matplotlib ax, optional
    legend :    bool, optional
                If True, plot legend
    leg_pos :   {'right','top'}
                Position of legend.
    **sns_kws : seaborn.heatmap kwargs, optional

    Returns
    -------
    seaborn.heatmap

    Examples
    --------
    """

    if not isinstance(data, (pd.DataFrame, pd.Series, np.ndarray)):
        raise TypeError('Unable to work with data of type "{0}"'.format(type(data)))

    # If not provided, get ax
    if ax is None:
        fig, ax = plt.subplots()

    # Get unique values in dataset
    if isinstance(data, (pd.DataFrame, pd.Series)):
        unique_values = sorted( np.unique(data.values.astype(str)) )
    else:
        unique_values = sorted( np.unique(data.astype(str)) )

    n_unique = len(unique_values)

    # Prepare colors
    if not cmap:
        # Generate colors -> for the heatmap
        colors = _gen_colors( palette, n_unique )

        # We have colours, let's generate a cmap -> for the legend
        cmap = { v : colors[i] for i,v in enumerate(unique_values) }
    elif isinstance(cmap, dict):
        # Check for missing entries
        missing_entries = [ v for v in unique_values if v not in cmap ]

        # Generate missing colors
        colors = _gen_colors( palette, len(missing_entries) )

        # Update colormap
        cmap.update( { v : colors[i] for i,v in enumerate(missing_entries) } )

        # Generate colours in order -> for legend
        colors = [cmap[cat] for cat in unique_values]

    else:
        raise TypeError('Unable to intepret colormap of type "{0}"'.format(type(cmap)))

    # Turn data into numeric values
    vmap = { c : i for i, c in enumerate(unique_values) }

    mapper = lambda t: vmap[str(t)]
    vfunc = np.vectorize(mapper)

    if isinstance(data, pd.DataFrame):
        numerical_data = data.applymap(mapper)
    elif isinstance(data, np.ndarray):
        numerical_data = vfunc(data)

    # Plot heatmap
    cmap_object = mcolors.LinearSegmentedColormap.from_list('custom', colors, N=len(colors))
    sns_ax = sns.heatmap(   numerical_data,
                            ax=ax,
                            cmap=cmap_object,
                            cbar=False,
                            **sns_kws )

    # Add legend
    if legend:
        patches = [mpatches.Patch(facecolor=cmap[v], edgecolor='black') for v in unique_values]

        if leg_pos.lower() == 'top':
            bbox_to_anchor = (0., 1.02, 1., .102)
            ncol = n_unique
        elif leg_pos.lower() == 'right':
            bbox_to_anchor = (1.02, 0., 0.102, 1.)
            ncol = 1

            box = sns_ax.get_position()

            # Make heatmap a bit less wide
            sns_ax.set_position( [box.x0, box.y0, box.width*.9, box.height])


        l = sns_ax.legend(      patches,
                                unique_values,
                                bbox_to_anchor=bbox_to_anchor,
                                ncol=ncol,
                                mode="expand",
                                fontsize=8
                                )

    return sns_ax

def _is_categorical(x):
    """ Returns True if data is categorical (i.e. not numerical)."""
    if isinstance(x, pd.DataFrame):
        num_cols = x.mean(axis=0).index.tolist()
        return [ col not in num_cols for col in x.columns ]
    elif isinstance(x, pd.Series):
        try:
            x.mean()
            return True
        except:
            return False
    elif isinstance(x, np.ndarray):
        if x.ndim > 2:
            raise ValueError('Can only process 1d or 2d arrays.')
        elif x.ndim == 2:
            is_cat = []
            for i in range(x.shape[1]):
                try:
                    x[:,i].astype(int)
                    cat_cols.append(False)
                except:
                    cat_cols.append(True)
        elif x.ndim == 1:
            try:
                x.astype(int)
                return False
            except:
                return True


def _gen_colors(pal, n):
    """ Generate colours from provided palette.
    """

    # If string
    if isinstance(pal, str):
        # First, check if seaborn palette
        try:
            colors = sns.color_palette(pal, n)
        # If not, try getting the matplotlib palette
        except:
            pal = plt.get_cmap(pal)
            colors = [ pal(i) for i in np.linspace(0,1,n) ]
    # If palette provided
    elif isinstance(pal, mcolors.LinearSegmentedColormap):
        colors = [ pal(i) for i in np.linspace(0,1,n) ]
    # If list of colors
    elif isinstance(pal, (list, np.ndarray)):
        if len(pal) < n:
            raise ValueError('Must provide at least as many colors as there are unique entries: {0}'.format(len(unique_values)))
        else:
            colors = pal
    else:
        raise TypeError('Unable to generate colors from palette of type "{0}"'.format(type(pal)))

    return colors



