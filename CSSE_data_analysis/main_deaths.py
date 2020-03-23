import plotly.express as px
import pandas as pd

from CSSE_data_analysis import main_functions as mf

df_deaths = pd.read_csv('../data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
df_deaths = df_deaths.drop(['Lat', 'Long', 'Province/State'], axis=1)
df_deaths = df_deaths.rename(columns={'Country/Region': 'country'})


#%%

df_deaths_tidy = mf.tidy_data(df_deaths, value_name='deaths', rolling_window=3)
df_deaths_tidy_filtered = mf.filter_tidy_data(df_tidy=df_deaths_tidy, min_cases=20, value_name='deaths')

#%%

fig = px.line(df_deaths_tidy_filtered, x='date', y='deaths', color='country')
fig.update_layout(yaxis_type="log")
fig.show()

#%%
fig = px.line(df_deaths_tidy_filtered, x='date', y='log_deaths', color='country',
              hover_data=['deaths'])
fig.show()
# plotly.offline.plot(fig, 'cases.html')


#%%

fig = px.line(df_deaths_tidy_filtered, x='date', y='factor_deaths_increase_smoothed', color='country',
              hover_data=['deaths', 'delta_log_deaths_smoothed'])
fig.show()

#%%



