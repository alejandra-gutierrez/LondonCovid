import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


# ----- MAP ------
fp = "data/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"
map_df = gpd.read_file(fp)

# check data type = GEOdataframe
map_df.head()

# print(map_df.shape)
# map_df.plot()
# plt.show()

# ----- BOROUGHS ------

df = pd.read_csv('data/pubs_numbers.csv', header = 0)
df.head()


df_map = df[['Unnamed: 1','2017']]
print(df_map)

# See the very end of this code to understand how this line works
merged = map_df.set_index('NAME').join(df_map.set_index('Unnamed: 1'))


# set a variable that will call whatever column we want to visualise on the map
variable = '2017'
# set the range for the choropleth
vmin, vmax = 0, 300
# Create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))


# create map
merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')


ax.axis('off')
ax.set_title('Pubs in London', fontdict={'fontsize': '15', 'fontweight' : '2'})
# create an annotation for the data source
ax.annotate('Source: London Datastore, 2014',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)
#
# # fig.savefig("map_export.png", dpi=300)
#
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