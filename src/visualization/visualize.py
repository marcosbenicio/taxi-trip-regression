import pandas as pd

import geopandas as gpd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.colors import  Normalize
from features.statistics import boxplot_stats


def plot_points_map(df, gdf_map, geometry_col, ax, title='', within_map=True, 
                    color_map='beige', color_points='orange'):
    """
    Plots a map with points from a DataFrame onto a given Axes object.

    Parameters:
    - df: DataFrame with the coordinates to plot.
    - gdf_map: GeoDataFrame of the map boundaries.
    - geometry_col: GeoDataFrame column with geometry data.
    - ax: Matplotlib Axes object to plot on.
    - title: Title of the plot.
    - within_map: If True, only plots points within the map boundaries.
    - color_map: Color for the map.
    - color_points: Color for the points.
    """

    gdf_points = gpd.GeoDataFrame(df, geometry=geometry_col)
    gdf_points.crs = gdf_map.crs

    if within_map:
        gdf_points = gpd.sjoin(gdf_points, gdf_map, how="inner", predicate='within')
        df = df.loc[gdf_points.index]

    gdf_map.plot(ax = ax, color=color_map, edgecolor='grey')
    gdf_points.plot(ax =ax, markersize=1, color = color_points)
    ax.set_xlabel('Longitude', fontsize=14)
    ax.set_ylabel('Latitude', fontsize=14)
    ax.set_title(title, fontsize=20)

    return df

def plot_clusters_map(  df, gdf_map, latitude_col, longitude_col, cluster_col, ax, 
                        title=' ', sample_size=0, color_map= 'beige', edgecolor= 'grey', 
                        random_state=42, cmap='tab20', alpha=0.2):
    
    """
    Plots a geographical map with clusters from a DataFrame.

    Parameters:
    - df: DataFrame containing the data to be plotted.
    - gdf_map: GeoDataFrame representing the geographical boundaries.
    - latitude_col: Name of the column containing latitude data.
    - longitude_col: Name of the column containing longitude data.
    - cluster_col: Name of the column containing cluster identifiers.
    - ax: Matplotlib Axes object for plotting.
    - title: Title of the plot.
    - sample_size: Number of data points to sample from df (0 for all).
    - color_map: Color for the map.
    - edgecolor: Edge color for the map.
    - random_state: Random state for reproducibility in sampling.
    - cmap: Colormap for clusters.
    - alpha: Transparency level for cluster points.
    """
    
    
    if sample_size > 0:
        df = df.sample(sample_size, random_state=random_state)
        
    # Create geometry and GeoDataFrame
    geometry = gpd.points_from_xy(df[longitude_col], df[latitude_col])
    gdf_clusters = gpd.GeoDataFrame(df, geometry=geometry).set_crs(epsg=4326)
    
    # Convert map to the same CRS
    gdf_map = gdf_map.to_crs(epsg=4326)
    gdf_map.plot(ax=ax, color=color_map, edgecolor=edgecolor)  # Plot the NYC boundary
    
    # Scatter plot for clusters
    ax.scatter( gdf_clusters.geometry.x, gdf_clusters.geometry.y, s=1, 
                c=df[cluster_col].values, cmap=cmap, alpha=alpha)  # Plot clusters
    
    # Set labels and title
    ax.set_xlabel('Longitude', fontsize=14)
    ax.set_ylabel('Latitude', fontsize=14)
    ax.set_title(title, fontsize=20)


def plot_distribution_boxplot(  series, ax1, ax2, title='', label='', log1p=True, 
                                draw_quartiles=True, kde=True):
    """
    Plot the distribution and boxplot of a series on given axes.

    Args:
    - series (pandas.Series): The series to plot.
    - ax1 (matplotlib.axes.Axes): The axes for the histogram.
    - ax2 (matplotlib.axes.Axes): The axes for the boxplot.
    - title (str): The title of the plot.
    - label (str): The label for the x-axis.
    - log1p (bool): If True, applies log1p transformation to the series.
    - draw_quartiles (bool): If True, draws quartile lines on the histogram.
    - kde (bool): If True, plots a KDE over the histogram.
    """
    if log1p:
        series = np.log1p(series)
    stats = boxplot_stats(series)

    sns.histplot(   series, bins=40, linewidth=0.5, color='#dfdc7bff', alpha=0.2,
                    ax=ax1, kde=kde, line_kws={'lw': 3})
    ax1.set_title(f'{title} Histogram', fontsize=15)
    ax1.set_xlabel(label, fontsize=14)
    ax1.set_ylabel('Count', fontsize=14)

    sns.boxplot(data=series, color='#dfdc7bff', ax=ax2,
                fliersize=3, flierprops={'color': '#50566dff', 'markeredgecolor': '#50566dff'})
    
    ax2.set_title(f'{title} Boxplot', fontsize=15)
    ax2.set_ylabel(label, fontsize=14)

    if draw_quartiles:
        quartiles = [stats['Q1'], stats['Q3'], stats['lower_whis'], stats['upper_whis']]
        for line in quartiles:
            ax1.axvline(line, color='#50566dff', linestyle='--', alpha=1, lw=2)
            y_center = ax1.get_ylim()[1] / 2
            ax1.text(   line, y_center, f'{line:.2f}',
                        fontsize=18, color='black', va='center', ha='right', rotation=90)

def plot_feature_importance(df, x, y, ax, threshold=0.002, title='Feature Importance', 
                            xlabel='Features', ylabel='Importance', palette=None):
    """
    Function to plot the feature importance with a distinction of importance based on a threshold.

    Parameters:
    - df: pandas.DataFrame
        DataFrame containing features and their importance scores.
    - x: str
        Name of the column representing feature names.
    - y: str
        Name of the column representing feature importance scores.
    - ax: matplotlib axis object
        Axis on which to draw the plot.
    - threshold: float, optional (default=0.002)
        Value above which bars will be colored differently.
    - pad: float, optional (default=5.0)
        Adjust the layout of the plot.
    - title: str, optional (default='Feature Importance')
        Title of the plot.
    - xlabel: str, optional (default='Features')
        Label for the x-axis.
    - ylabel: str, optional (default='Importance')
        Label for the y-axis.
    - palette: list, optional
        A list of two colors. The first color is for bars below the threshold and the second is for bars above.

    Returns:
    - None (modifies ax in-place)
    """
    if palette is None:
        palette = ["blue", "red"]
    
    blue, red = palette
    colors = [red if value >= threshold else blue for value in df[y]]
    sns.barplot(x=x, y=y, data=df, ax=ax, alpha=0.5, palette=colors, legend= False, hue = x)
    ax.set_xticks(range(len(df[x])))
    ax.set_xticklabels(df[x], rotation=90, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.set_xlabel(xlabel, fontsize=15) 
    ax.grid(axis='y')
    ax.set_title(title, fontsize=15)
    
def plot_corr_ellipses(data, figsize, **kwargs):
    """
    Plots a correlation matrix using ellipses to represent the correlations.

    Parameters:
    - data (pd.DataFrame): A 2D array or DataFrame containing the correlation matrix.
    - figsize: Tuple specifying the figure size.
    - kwargs: Additional keyword arguments for EllipseCollection.

    Returns:
    - A tuple containing the EllipseCollection object and the Axes object.

    """
    M = np.array(data)
    if not M.ndim == 2:
        raise ValueError('Data must be a 2D array.')

    # Mask the upper triangle of the matrix
    mask = np.triu(np.ones_like(M, dtype=bool), k=1)
    M[mask] = np.nan

    # Initialize the plot
    fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={'aspect': 'equal'})
    ax.set_xlim(-0.5, M.shape[1] - 0.5)
    ax.set_ylim(-0.5, M.shape[0] - 0.5)
    ax.invert_yaxis()
    ax.set_xticklabels([])
    ax.grid(False)

    # Determine xy locations of each ellipse center
    xy = np.indices(M.shape)[::-1].reshape(2, -1).T

    # Define ellipse properties
    w = np.ones_like(M).ravel() + 0.01  # Widths of ellipses
    h = 1 - np.abs(M).ravel() - 0.01   # Heights of ellipses
    a = 45 * np.sign(M).ravel()        # Rotation angles

    # Create and add the ellipse collection
    ec = EllipseCollection( widths=w, heights=h, angles=a, units='x', offsets=xy,
                            norm=Normalize(vmin=-1, vmax=1), transOffset=ax.transData, 
                            array=M.ravel(), **kwargs)
    ax.add_collection(ec)

    # Add a color bar for correlation values
    cb = fig.colorbar(ec, ax=ax, orientation='horizontal', fraction=0.047, pad=0.00)
    cb.ax.xaxis.set_ticks_position('bottom')
    cb.ax.xaxis.set_label_position('bottom')
    cb.ax.tick_params(top=False, labeltop=False)

    # Feature names on the diagonal
    if isinstance(data, pd.DataFrame):
        diagonal_positions = np.arange(M.shape[1])
        for i, label in enumerate(data.columns):
            ax.annotate(" -  " + label, (i - 0.4, i - 1), ha='left', va='bottom', rotation=90)
        ax.set_yticks(diagonal_positions)
        ax.set_yticklabels(data.index)

    # Hide the plot spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    return ec, ax
