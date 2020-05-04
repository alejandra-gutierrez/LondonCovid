import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


DAYS = 60
POPULATION = 10000
SPREAD_FACTOR = 1
DAYS_TO_RECOVER = 10
INITIALLY_AFFECTED = 1

# np.arange() is an array creation routine based on numerical ranges
# np.arange(POPULATION) creates array([0, 1, 2, 3, ... POPULATION-1])
city = pd.DataFrame(data={'id': np.arange(POPULATION), 'infected': False, 'recovery_day': None, 'recovered': False})
city = city.set_index('id')

#sample allows to choose random row/s in the dataframe. replace=false means we cannot sample the same row twice.
firstCases = city.sample(INITIALLY_AFFECTED, replace=False)

#After randomly selecting the people initially infected, change their status to "INFECTED = TRUE" in the dataframe
city.loc[firstCases.index, 'infected'] = True

# People initially infected need 10 days to recover. this sets the counter
city.loc[firstCases.index, 'recovery_day'] = DAYS_TO_RECOVER

# Initialise the value of active_cases with initially_affected. Active_cases will change over time.
stat_active_cases = np.array([INITIALLY_AFFECTED])
stat_recovered = [0]

for today in range(1, DAYS):
    # Mark recovered people, they are not infectious anymore
    city.loc[city['recovery_day'] == today, 'recovered'] = True
    city.loc[city['recovery_day'] == today, 'infected'] = False


    spreadingPeople = city[ (city['infected'] == True)]
    totalCasesToday = round(len(spreadingPeople) * SPREAD_FACTOR)
    casesToday = city.sample(totalCasesToday, replace=True)

    # Ignore already infected or recovered people
    casesToday = casesToday[ (casesToday['infected'] == False) & (casesToday['recovered'] == False) ]

    # Mark the new cases as infected
    city.loc[casesToday.index, 'infected'] = True
    city.loc[casesToday.index, 'recovery_day'] = today + DAYS_TO_RECOVER

    stat_active_cases = np.append(stat_active_cases, len(city[city['infected'] == True]))
    print(stat_active_cases)
    stat_recovered.append(len(city[city['recovered'] == True]))
    # if today >= 5:
    #     SPREAD_FACTOR = 1
    # if today >= 10:
    #     SPREAD_FACTOR = 0.1



fig = plt.figure(figsize=(16, 8))

plt.bar(x=np.arange(DAYS), height=stat_active_cases)
plt.text(145, 90000, f"SPREAD_FACTOR = {SPREAD_FACTOR}", fontsize=14)
plt.show()