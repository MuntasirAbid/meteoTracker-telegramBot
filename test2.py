from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Create a new map with a specific projection
m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')

# Draw coastlines and countries
m.drawcoastlines()
m.drawcountries()

# Plot some data on the map
x, y = m(-74.0059, 40.7128)
m.plot(x, y, 'ro', markersize=10)

# Show the map
plt.show()
