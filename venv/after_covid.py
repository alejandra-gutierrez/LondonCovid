# Import libraries
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from tabulate import tabulate

# Read Data
df = pd.read_csv("data/Global_Mobility_Report.csv", low_memory=False)

# Rename columns
df = df.rename(columns={'country_region':'Country'})
df = df.rename(columns={'date':'Date'})
df = df.rename(columns={'retail_and_recreation_percent_change_from_baseline':'retail'})
df = df.rename(columns={'grocery_and_pharmacy_percent_change_from_baseline':'pharmacy'})
df = df.rename(columns={'parks_percent_change_from_baseline':'parks'})
df = df.rename(columns={'transit_stations_percent_change_from_baseline':'transit_station'})
df = df.rename(columns={'workplaces_percent_change_from_baseline':'workplaces'})
df = df.rename(columns={'residential_percent_change_from_baseline':'residential'})

print(tabulate(df[152:160], headers='keys', tablefmt='psql'))

# Manipulate Dataframe
df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False)
df_countries = df_countries.drop_duplicates(subset = ['Country'])
# df_countries = df_countries[df_countries['Active']>0]

# Manipulating the original dataframe
df_countrydate = df
df_countrydate = df_countrydate.groupby(['Date','Country']).sum().reset_index()
min_cases = df_countrydate['residential'].min()

# Creating the visualization
fig = px.choropleth(df_countrydate,
                    locations="Country",
                    locationmode="country names",
                    color="residential",
                    hover_name="Country",
                    animation_frame="Date",
                    # range_color=(0, 20000),
                    range_color=(-500, 500),
                    color_continuous_scale=px.colors.diverging.Picnic,
                    color_continuous_midpoint=min_cases,
                    )
fig.update_layout(
    title_text='Stay at home (quarantine) during coronavirus pandemic',
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=False,
    ))

fig.show()