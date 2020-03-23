import plotly.express as px
import plotly
import pandas as pd

from CSSE_data_analysis import main_functions as mf

df_cases = pd.read_csv(
    '../data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

df_cases = df_cases.drop(['Lat', 'Long', 'Province/State'], axis=1)
df_cases = df_cases.rename(columns={'Country/Region': 'country'})


#%%

df_cases_tidy = mf.tidy_data(df_cases, value_name='cases', rolling_window=3)
test_germany = df_cases_tidy[df_cases_tidy.country == 'Germany']
df_cases_tidy_filtered = mf.filter_tidy_data(df_tidy=df_cases_tidy, min_cases=100)

#%%

fig = px.line(df_cases_tidy_filtered, x='date', y='cases', color='country')
fig.update_layout(yaxis_type="log")
fig.show()

#%%
fig = px.line(df_cases_tidy_filtered, x='date', y='log_cases', color='country')
fig.show()
plotly.offline.plot(fig, 'cases.html')


#%%

fig = px.line(df_cases_tidy_filtered, x='date', y='delta_log_cases_smoothed', color='country')
fig.show()

#%%



