import plotly.express as px
from plotly.subplots import make_subplots

from app import main_functions as mf
import plot_functions as pf

value_name = 'deaths'
df_deaths_tidy_filtered = mf.get_csse_data(value_name, min_cases=20, rolling_window=3)


#%%

fig = make_subplots(rows=1, cols=2)

subfig1 = px.line(df_deaths_tidy_filtered, x='date', y=value_name, color='country')
subfig2 = px.line(df_deaths_tidy_filtered, x='date', y=f'factor_{value_name}_increase_smoothed', color='country',
                  hover_data=[value_name])

amount_countries = len(df_deaths_tidy_filtered.country.unique().tolist())

for data in subfig1.data:
    fig.add_trace(data, row=1, col=1)
for data in subfig2.data:
    fig.add_trace(data, row=1, col=2)
for i in range(amount_countries, 2 * amount_countries):
    fig.data[i].showlegend = False
fig.update_layout(updatemenus=[pf.get_log_linear_buttons()])
fig.update_yaxes(title=f'Summed {value_name}', row=1, col=1)
fig.update_yaxes(title='Smoothed daily increase (Rolling 3 day window)', row=1, col=2)
fig.show()
