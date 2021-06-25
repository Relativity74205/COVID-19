from collections import Counter
from collections import defaultdict

import pandas as pd
import numpy as np


max_day = 75
base_cases = 2
double_time = 3
daily_factor = 2**(1/double_time)

p = 0.01
sample_size = 100000
mean_time = 17.3
sigma_time = 2
pop = 82_000_000

deaths_cumulated = defaultdict(int)
cases_cumulated = []
day = 0
cases = base_cases
while cases <= pop*0.9999 and day < 1000:
    if day % 10 == 0:
        print(f'{day=}; {cases=}')

    uninfected_factor = (pop - cases) / pop
    daily_factor_corrected = (1 + (daily_factor - 1) * uninfected_factor)
    new_cases = int(np.round(cases * daily_factor_corrected - cases))
    cases += new_cases
    new_deaths = np.random.binomial(new_cases, p)
    new_death_times = np.round(np.random.normal(mean_time, sigma_time, new_deaths)).astype('int')
    new_death_times = dict(Counter(new_death_times))
    for days_to_death, new_deaths_day in new_death_times.items():
        day_of_death = day + days_to_death
        deaths_cumulated[day_of_death] += new_deaths_day
    cases_cumulated.append({'day': day, 'cases': cases, 'new_cases': new_cases, 'resulting_deaths': new_deaths})
    day += 1

df_cases = pd.DataFrame(cases_cumulated)
df_deaths = pd.DataFrame({'day': list(deaths_cumulated.keys()),
                          'deaths': list(deaths_cumulated.values())}).sort_values('day')

df = df_cases.set_index('day').join(df_deaths.set_index('day'), how='outer').reset_index()
df = df.fillna(0)
df['cumsum_deaths'] = df['deaths'].cumsum(skipna=False)

#%%

import plotly.express as px
import plot_functions as pf


fig = px.line(x='day', y='cases', data_frame=df)
fig.update_layout(updatemenus=pf.get_log_linear_buttons())
# fig.update_layout(yaxis_type="log")
# fig.update_layout(yaxis={"type": "log"})
fig.show()


#%%

import plotly.express as px

fig = px.line(x='day', y='deaths', data_frame=df)
fig.update_layout(updatemenus=pf.get_log_linear_buttons())
fig.show()


#%%


import plotly.express as px

fig = px.line(x='day', y='cumsum_deaths', data_frame=df)
fig.add_scatter(x=df['day'], y=df['cumsum_cases'], mode='lines')
fig.update_layout(updatemenus=pf.get_log_linear_buttons())
fig.show()
