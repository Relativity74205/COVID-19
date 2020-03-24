import plotly.express as px
import plotly
from plotly.subplots import make_subplots
import pandas as pd

from CSSE_data_analysis import main_functions as mf
import plot_functions as pf

df_deaths = pd.read_csv('data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
df_deaths = df_deaths.drop(['Lat', 'Long', 'Province/State'], axis=1)
df_deaths = df_deaths.rename(columns={'Country/Region': 'country'})
df_deaths_tidy = mf.tidy_data(df_deaths, value_name='deaths', rolling_window=3)
df_deaths_tidy_filtered = mf.filter_tidy_data(df_tidy=df_deaths_tidy, min_cases=20, value_name='deaths')

#%%

fig = make_subplots(rows=1, cols=2)

subfig1 = px.line(df_deaths_tidy_filtered, x='date', y='deaths', color='country')
subfig2 = px.line(df_deaths_tidy_filtered, x='date', y='factor_deaths_increase_smoothed', color='country',
                  hover_data=['deaths'])

amount_countries = len(df_deaths_tidy_filtered.country.unique().tolist())

for data in subfig1.data:
    fig.add_trace(data, row=1, col=1)
for data in subfig2.data:
    fig.add_trace(data, row=1, col=2)
for i in range(amount_countries, 2 * amount_countries):
    fig.data[i].showlegend = False
fig.update_layout(updatemenus=[pf.get_log_linear_buttons()])
fig.update_yaxes(title="Summed deaths", row=1, col=1)
fig.update_yaxes(title="Smoothed daily increase (Rolling 3 day window)", row=1, col=2)
fig.show()
