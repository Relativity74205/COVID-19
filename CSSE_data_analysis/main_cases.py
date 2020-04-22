import os
import pathlib

import plotly.express as px
from plotly.subplots import make_subplots

import main_functions as mf
import plot_functions as pf

if pathlib.Path.cwd().name == 'corona':
    os.chdir('CSSE_data_analysis')


value_name = 'cases'
df_cases_tidy_filtered = mf.get_csse_data(value_name, min_cases=100, rolling_window=7)
test_germany = df_cases_tidy_filtered[df_cases_tidy_filtered.country == 'Germany']

#%%


fig = make_subplots(rows=1, cols=2)

subfig1 = px.line(df_cases_tidy_filtered, x='date', y=value_name, color='country', width=500, height=500)
subfig2 = px.line(df_cases_tidy_filtered, x='date', y=f'factor_{value_name}_increase_smoothed', color='country',
                  hover_data=[value_name], width=500, height=500)

amount_countries = len(df_cases_tidy_filtered.country.unique().tolist())

for data in subfig1.data:

    fig.add_trace(data, row=1, col=1)
for data in subfig2.data:
    fig.add_trace(data, row=1, col=2)
for i in range(amount_countries, 2 * amount_countries):
    fig.data[i].showlegend = False
fig.update_layout(updatemenus=[pf.get_log_linear_buttons()])
fig.update_layout(width=1500, height=500)
fig.update_yaxes(title=f'Summed {value_name}', row=1, col=1)
fig.update_yaxes(title='Smoothed daily increase (Rolling 3 day window)', row=1, col=2)
fig.show()
