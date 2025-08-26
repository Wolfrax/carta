import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import geopandas as gpd
import geoplot as gplt
import numpy as np
from scipy import ndimage


def heatmap(d, bins=(100, 100), smoothing=1.3, cmap='jet'):
    longitudes = list(d.geometry.apply(lambda pt: pt.coords[0][0]))
    latitudes = list(d.geometry.apply(lambda pt: pt.coords[0][1]))
    heatmap, xedges, yedges = np.histogram2d(latitudes, longitudes, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    heatmap = ndimage.filters.gaussian_filter(heatmap, smoothing, mode='nearest')

    plt.imshow(heatmap, cmap=cmap, extent=extent)
    plt.gca().invert_yaxis()


# The data below is in epsg:4326 reference system - WGS 84 (https://epsg.io/4326)
world = gpd.read_file("data/ne_10m_admin_1_states_provinces.shp")
swe = world[world['admin'] == 'Sweden']  # Filter out Sweden from the world using pandas syntax
val = gpd.read_file("data/2020-06-02_avg_temp.geojson") # Probably in EPSG 3006 or 3021
val = val.to_crs(epsg=4326)

proj = gplt.crs.AlbersEqualArea()
fig = plt.figure(figsize=(10,5))
#ax1 = plt.subplot(121, projection=proj)
#ax2 = plt.subplot(122, projection=proj)

#gplt.kdeplot(val[val["val"]], cmap='coolwarm', clip=swe, shade=True, n_levels=10, ax=ax1, projection=proj)
#gplt.polyplot(swe, edgecolor="Lightgrey", zorder=1, linewidth=0.5, ax=ax1, projection=proj)

# hue="val", means that we use the val-column (value) to colorize the voronoi regions
#gplt.voronoi(val, cmap='coolwarm', clip=swe, hue="val", legend=True, edgecolor="None", ax=ax2, projection=proj)
#gplt.polyplot(swe, edgecolor="Lightgrey", zorder=1, linewidth=0.5, ax=ax2, projection=proj)

heatmap(val, bins=100, smoothing=5, cmap='coolwarm')
plt.show()