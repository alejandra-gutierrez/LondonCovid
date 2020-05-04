import numpy as np
import geopandas as gpd
import pandas as pd
import descartes
import matplotlib.pyplot as plt

# ----- MAP ------
fp = "data/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp"
map_df = gpd.read_file(fp)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe
map_df.head()

# print(map_df.shape)

# map_df.plot()
# plt.show()

# ----- BOROUGHS ------
df = pd.read_csv('data/pubs_numbers.csv', header = 0)
# print(df.head())

pub_borough = df[['Unnamed: 1', '2017']]


days=["column1", "column2", "column3",
         "column4", "column5", "column6",
         "column7", "column8", "column9",
         "column10", "column11", "column12",
         "column13", "column14", "column15",
         "column16", "column17", "column18",
         "column19", "column20", "column21",
         "column22", "column23", "column24",
         "column25", "column26", "column27",
         "column28", "column29", "column30",
      "column31", "column32", "column33",
      "column34", "column35", "column36",
      "column37", "column38", "column39",
      "column40", "column41", "column42",
      "column43", "column44", "column45",
      "column46", "column47", "column48",
      "column49", "column50", "column51",
      "column52", "column53", "column54",
      "column55", "column56", "column57",
      "column58", "column59", "column60"
      ]

DAYS = 60
SPREAD_FACTOR = 1
DAYS_TO_RECOVER = 10
INITIALLY_AFFECTED = 1
allDays = pd.DataFrame()

for ind in pub_borough.index:
    # print(df['Unnamed: 1'][ind], df['2017'][ind])
    value = df['2017'][ind]
    POPULATION = 50*value
    city = pd.DataFrame(data={'id': np.arange(POPULATION), 'infected': False, 'recovery_day': None, 'recovered': False})
    city = city.set_index('id')
    firstCases = city.sample(INITIALLY_AFFECTED, replace=False)
    city.loc[firstCases.index, 'infected'] = True
    city.loc[firstCases.index, 'recovery_day'] = DAYS_TO_RECOVER
    stat_active_cases = np.array([INITIALLY_AFFECTED])
    stat_recovered = [0]

    for today in range(1, DAYS):
        # Mark recovered people, they are not infectious anymore
        city.loc[city['recovery_day'] == today, 'recovered'] = True
        city.loc[city['recovery_day'] == today, 'infected'] = False

        spreadingPeople = city[(city['infected'] == True)]
        totalCasesToday = round(len(spreadingPeople) * SPREAD_FACTOR)
        casesToday = city.sample(totalCasesToday, replace=True)

        # Ignore already infected or recovered people
        casesToday = casesToday[(casesToday['infected'] == False) & (casesToday['recovered'] == False)]

        # Mark the new cases as infected
        city.loc[casesToday.index, 'infected'] = True
        city.loc[casesToday.index, 'recovery_day'] = today + DAYS_TO_RECOVER

        stat_active_cases = np.append(stat_active_cases, len(city[city['infected'] == True]))
        stat_recovered.append(len(city[city['recovered'] == True]))

    day = pd.DataFrame(stat_active_cases.reshape(-1, len(stat_active_cases)), columns=days)
    allDays = allDays.append(day, ignore_index=True)

    day = []
    city = []
    firstCases = []
    stat_active_cases = []
    stat_recovered = []

newsheet = pd.concat([pub_borough,allDays], axis=1)
print(newsheet)

merged = map_df.set_index('NAME').join(newsheet.set_index('Unnamed: 1'))
print(merged)
# merged.to_csv('merged_dataframe.csv')



# Set variables
for i in range(1, 61, 10):
    number = str(i)
    variable = "column"+ number
    vmin, vmax = 0, 500
    fig, ax = plt.subplots(1, figsize=(10, 6))

    # Create map
    merged.plot(column= variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
    ax.axis('off')
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm)
plt.show()



