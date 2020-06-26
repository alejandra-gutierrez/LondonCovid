# Import libraries
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from tabulate import tabulate
import seaborn as sns

# Read Data
df = pd.read_csv("data/New_Global_Mobility_Report.csv", low_memory=False)

# Rename columns
df = df.rename(columns={'country_region':'Country'})
df = df.rename(columns={'date':'Date'})
df = df.rename(columns={'retail_and_recreation_percent_change_from_baseline':'retail'})
df = df.rename(columns={'grocery_and_pharmacy_percent_change_from_baseline':'pharmacy'})
df = df.rename(columns={'parks_percent_change_from_baseline':'parks'})
df = df.rename(columns={'transit_stations_percent_change_from_baseline':'transit_station'})
df = df.rename(columns={'workplaces_percent_change_from_baseline':'workplaces'})
df = df.rename(columns={'residential_percent_change_from_baseline':'residential'})
df.drop(['country_region_code','sub_region_1', 'sub_region_2', 'census_fips_code', 'iso_3166_2_code'], axis=1, inplace = True)
# print(tabulate(df[20000:20050], headers='keys', tablefmt='psql'))

# ----------------------------------- Assign Continent -------------------------------
asia = ['Malaysia','Turkey','South Korea','India','Israel','Indonesia','Tajikistan','Qatar','Nepal','Singapore','Malaysa','Thailand','Nepal','Taiwan','Hong Kong','Russia','Mozambique','Afghanistan', 'Sri Lanka','Bahrain', 'United Arab Emirates','Saudi Arabia', 'Kuwait', 'Qatar', 'Oman',
    'Sultanate of Oman','Lebanon', 'Iraq', 'Yemen', 'Pakistan', 'Lebanon', 'Philippines', 'Jordan', 'Japan', 'Singapore',
        'Laos', 'Tanzania', 'Cambodia', 'Mongolia', 'Vietnam']
europe = ['Belarus','Belgium','Czechia','Moldova','Germany','Ireland','Scotland' ,'Spain', 'France', 'Ukraine','Italy', 'Netherlands', 'Norway', 'Sweden','Czech Republic', 'Finland',
      'Denmark', 'Czech Republic', 'Switzerland', 'UK', 'UK&I', 'Poland', 'Greece','Austria',
      'Bulgaria', 'Hungary', 'Luxembourg', 'Romania' , 'Slovakia', 'Estonia', 'Slovenia','Portugal',
      'Croatia', 'Lithuania', 'Latvia','Serbia', 'Estonia','Rwanda', 'ME', 'Iceland' , 'United Kingdom']
africa = ['Uganda', 'Senegal','Cape Verde','Namibia', 'South Africa', 'Angola', 'Mali', 'Cameroon', 'Niger', 'Botswana', 'Libya','Rwanda','Togo','Ghana','Morocco', 'Nigeria','Egypt','Tunisia', 'Africa', 'ZA', 'Kenya', 'Zimbabwe', 'Zambia', 'Namibia']
Latin_America = ['Panama','Belize', 'Mexico', 'Costa Rica', 'Nicaragua','Puerto Rico', 'Honduras', 'Venezuela', 'Chile', 'Argentina', 'Brazil', 'Bolivia', 'Colombia',
                 'Ecuador', 'Dominican Republic', 'Guatemala', 'Antigua and Barbuda', 'Peru', 'El Salvador',
                 'Uruguay', 'Paraguay', 'Jamaica']
North_America = ['United States', 'Canada']
Oceania = ['Australia', 'New Zealand', 'Tasmania', 'Fiji', 'Samoa', 'Papua New Guinea', 'Tonga', 'New Caledonia']

def GetConti(counry):
    if counry in asia:
        return "Asia"
    elif counry in europe:
        return "Europe"
    elif counry in africa:
        return "Africa"
    elif counry in Oceania:
        return "Oceania"
    elif counry in North_America:
        return "North America"
    elif counry in Latin_America:
        return "Latin America"
    else:
        return "other"

df['Continent'] = df['Country'].apply(lambda x: GetConti(x))
df = df[df.Continent != 'other']


# -------------------------------------------- Manipulate Dataframe ----------------------------------------
df_countries = df.groupby(['Country', 'Date', 'Continent']).mean().reset_index().sort_values('Date', ascending=False)
a="India"
b="Sweden"
c="United States"
d="New Zealand"
e="France"
f="Italy"
df_country = df.groupby(['Country','Date']).mean().reset_index()
c1 = df_country[df_country['Country']==a]
c2 = df_country[df_country['Country']==b]
c3 = df_country[df_country['Country']==c]
c4 = df_country[df_country['Country']==d]
c5 = df_country[df_country['Country']==e]
c6 = df_country[df_country['Country']==f]

frames = [c1, c2, c3, c4, c5, c6]
countries = pd.concat(frames)
# -------------------------------- Line Graph -------------------------------------
fig = px.line(countries, x="Date", y="retail", title='retail', color = 'Country')
fig.show()

# -------------------------------- Scatter Plot -------------------------------------

# Find the minimum!!!!!!!!
df_country = df.groupby(['Country', 'Continent'])['retail'].mean().reset_index(name ='Mean_Retail')
df_country = df_country.groupby(['Country','Continent'])['Mean_Retail'].mean().reset_index(name ='Minimum')

# Truncate
df_truncated = df.groupby(['Country', 'Date', 'Continent']).mean().reset_index().sort_values('Date', ascending=False)
df_truncated['Date'] = pd.to_datetime(df_truncated['Date'], format = '%Y-%m-%d')
df_truncated.set_index('Date', inplace=True)
df_truncated = df_truncated.sort_index()
df_truncated = df_truncated.truncate(before='2020-06-15 00:00:00')

# Find the maximum!!!!!
df_truncated = df_truncated.groupby(['Country', 'Continent'])['retail'].mean().reset_index(name ='Maximum')

# Merge
merged = df_country.merge(df_truncated, left_on='Country', right_on='Country')

# Create new columns
merged['Difference'] = merged['Maximum'] - merged['Minimum']
merged['Annotation'] = " "

merged.loc[merged.Country == a , "Annotation"] = a
merged.loc[merged.Country == b , "Annotation"] = b
merged.loc[merged.Country == c , "Annotation"] = c
merged.loc[merged.Country == d , "Annotation"] = d
merged.loc[merged.Country == e , "Annotation"] = e
merged.loc[merged.Country == f , "Annotation"] = f


fig = px.scatter(merged, x="Minimum", y="Maximum",  labels={'x':'Worst', 'y':'Best'},
                 hover_data=['Country'], color = "Continent_x", text="Annotation", size_max=30)
fig.show()

# ------------------------------ Chroropleth Graph -----------------------------------
# Manipulating the original dataframe
df_countrydate = df
df_countrydate = df_countrydate.groupby(['Date','Country', 'Continent']).mean().reset_index()

fig = px.choropleth(df_countrydate,
                    locations="Country",
                    locationmode="country names",
                    color="retail",
                    hover_name="Country",
                    animation_frame="Date",
                    range_color=(-100, 50),
                    color_continuous_scale=px.colors.diverging.Picnic
                    )
fig.update_layout(
    title_text='Retail ',
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=False,
    ))
# fig.show()
