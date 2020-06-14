# Import libraries
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from tabulate import tabulate

# Read Data
df = pd.read_csv("data/covid_19_data.csv")
print(tabulate(df[152:169], headers='keys', tablefmt='psql'))

# Rename columns
df = df.rename(columns={'Country/Region':'Country'})
df = df.rename(columns={'ObservationDate':'Date'})
df['Active'] = df['Confirmed']-df['Recovered']

# Manipulate Dataframe
df_countries = df.groupby(['Country', 'Date']).mean().reset_index().sort_values('Date', ascending=False)
df_countries = df_countries.drop_duplicates(subset = ['Country'])
df_countries = df_countries[df_countries['Active']>0]

# Manipulating the original dataframe
df_countrydate = df[df['Active']>0]
df_countrydate = df_countrydate.groupby(['Date','Country']).mean().reset_index()
min_cases = df_countrydate['Active'].min()

# Creating the visualization
fig = px.choropleth(df_countrydate,
                    locations="Country",
                    locationmode="country names",
                    color="Active",
                    hover_name="Country",
                    animation_frame="Date",
                    # range_color=(0, 20000),
                    range_color=(0, 20000),
                    color_continuous_scale=px.colors.sequential.OrRd,
                    color_continuous_midpoint=min_cases,
                    )
fig.update_layout(
    title_text='Global Spread of Coronavirus - Active cases',
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=False,
    ))

# fig.show()