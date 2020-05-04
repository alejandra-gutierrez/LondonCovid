import geopandas as gpd
import pandas as pd
import descartes
import matplotlib.pyplot as plt
from openpyxl import Workbook

# ----- MAP ------
fp = "data/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"

map_df = gpd.read_file(fp)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe
map_df.head()

# print(map_df.shape)

# map_df.plot()
# plt.show()

# ----- BOROUGHS ------

df = pd.read_csv('data/london_borough.csv', header = 0)

df.head()
# print(df.head())

df = df[['Area name','Happiness score 2011-14 (out of 10)', 'Anxiety score 2011-14 (out of 10)', 'Population density (per hectare) 2015', 'Mortality rate from causes considered preventable']]

data_for_map = df.rename(index=str, columns={"Happiness score 2011-14 (out of 10)": "happiness",
"Anxiety score 2011-14 (out of 10)": "anxiety",
"Population density (per hectare) 2015": "pop_density_per_hectare",
"Mortality rate from causes considered preventable": "mortality"})
# check dat dataframe
data_for_map.head()

# See the very end of this code to understand how this line works
merged = map_df.set_index('NAME').join(data_for_map.set_index('Area name'))
print(merged.head())



# set a variable that will call whatever column we want to visualise on the map
variable = 'mortality'
# set the range for the choropleth
vmin, vmax = 120, 220
# Create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))


# create map
merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
ax.set_title('Preventable death rate in London', fontdict={'fontsize': '25', 'fontweight' : '3'})
ax.annotate('Source: London Datastore, 2014',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm)
plt.show()


#   'set1'
#     A key
# 0  A0  K0
# 1  A1  K1
# 2  A2  K2
# 3  A3  K3
# 4  A4  K4
# 5  A5  K5

#  'set2'
#  B key
# 0  B0  K0
# 1  B1  K1
# 2  B2  K2

# set1.set_index('key').join(set2.set_index('key'))
#
#         A    B
#     key
#     K0   A0   B0
#     K1   A1   B1
#     K2   A2   B2
#     K3   A3  NaN
#     K4   A4  NaN
#     K5   A5  NaN