import geopandas as gpd
import matplotlib.pyplot as plt
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords, coords_to_points

fig, ax = plt.subplots(figsize=(10, 10))

world = gpd.read_file("data/ne_10m_admin_0_countries.shp")
avg_temp = gpd.read_file("data/2020-05-31_avg_temp.geojson")

swe = world[world['ADM0_A3'] == 'SWE']  # Filter out Sweden from the world using pandas syntax
swe = swe.to_crs(epsg=3395)             # convert to World Mercator CRS
swe_shape = swe.iloc[0].geometry        # get the Polygons for Sweden
avg_temp = avg_temp.to_crs(swe.crs)     # convert the stations coordinates to World Mercator crs
pts = [p for p in coords_to_points(points_to_coords(avg_temp.geometry)) if p.within(swe_shape)]  # converts to shapely Point
coords = points_to_coords(pts)          # convert back to simple NumPy coordinate array
poly_shapes, pts, poly_to_pt_assignments = voronoi_regions_from_coords(coords, swe_shape)

swe.boundary.plot(ax=ax, edgecolor='black')
avg_temp.plot(ax=ax, column=avg_temp.val, marker='o', markersize=10, legend=True)
plot_voronoi_polys_with_points_in_area(ax,
                                       swe_shape,
                                       poly_shapes,
                                       pts,
                                       poly_to_pt_assignments,
                                       voronoi_and_points_cmap='gnuplot')

ax.axis('off')
plt.axis('equal')
plt.show()
