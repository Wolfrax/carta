import cartopy.io.shapereader as shpreader
import geopandas
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib

#matplotlib.use('TkAgg')
#matplotlib.use('WebAgg')

shpfilename = shpreader.natural_earth(resolution='10m',
                                      category='cultural',
                                      name='admin_1_states_provinces')

df = geopandas.read_file(shpfilename)  # df = Data Frame, pandas

# Using pandas syntax, below we select the row in the data frame where 'admin' equals 'Sweden'
# From this we get the values of the geometry, ie the polygons making up Sweden provinces
polygons = df[df['admin'] == 'Sweden']['geometry'].values

fig = plt.figure(figsize=[10, 10])
ax = fig.add_subplot(projection=ccrs.Mercator())
# Extent limits taken from: https://epsg.io/5208-datum
ax.set_extent([10.93, 24.17, 55.28, 69.07], crs=ccrs.PlateCarree())
ax.add_geometries(polygons, crs=ccrs.PlateCarree(), facecolor=cfeature.COLORS['land'], edgecolor='black')

plt.show()
