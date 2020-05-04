import numpy as np
import geopandas as gpd
import pandas as pd
import descartes
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import row, column
from bokeh.models import Column


fp = "data/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"
map_df = gpd.read_file(fp)

infection_df = pd.read_csv('infection_dataframe.csv')

merged = map_df.merge(infection_df, left_on = 'NAME', right_on = 'Unnamed: 1')

merged_json = json.loads(merged.to_json())
json_data = json.dumps(merged_json)

#Define function that returns json_data for year selected by user.
def json_data(selectedYear):
    yr = selectedYear
    column_name = 'column'+yr
    df_yr = infection_df[['Unnamed: 1', column_name]]
    merged = map_df.merge(df_yr, left_on = 'NAME', right_on = 'Unnamed: 1')
    merged.drop(['Unnamed: 1'], axis=1, inplace=True)
    merged = merged.rename(index=str, columns={column_name: "number"})
    print(list(merged))
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    return json_data


#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data('1'))
#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.

color_mapper = LinearColorMapper(palette = palette, low = 0, high = 5000, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}
#Add hover tool
#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides =
tick_labels)
#Create figure object.
p = figure(title = 'London Covid', plot_height = 600 , plot_width = 950, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure.
p.patches('xs','ys', source = geosource,fill_color = {'field' :'number', 'transform' : color_mapper},
line_color = 'black', line_width = 0.25, fill_alpha = 1)
#Specify layout
p.add_layout(color_bar, 'below')
# Define the callback function: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    print(yr)
    new_data = json_data(yr)
    geosource.geojson = new_data

slider = Slider(title = 'Day',start = 1, end = 60, step = 1, value = 1)
slider.on_change('value', update_plot)
# Make a column layout of widgetbox(slider) and plot, and add it to the current document

layout = column(p,widgetbox(slider))
curdoc().add_root(layout)
#Display plot inline in Jupyter notebook
# output_notebook()
#Display plot
show(layout)

