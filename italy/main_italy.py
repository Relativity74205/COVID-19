import pandas as pd
import plotly.express as px

import plot_functions as pf


base_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/'
file_name = 'dpc-covid19-ita-andamento-nazionale.csv'
df = pd.read_csv(f'{base_url}{file_name}')
df = df.rename(columns={'data': 'date',
                        'ricoverati_con_sintomi': 'hospitalized_non_critical',
                        'terapia_intensiva': 'critical',
                        'totale_ospedalizzati': 'hospitalized',
                        'isolamento_domiciliare': 'quarantine',
                        'totale_attualmente_positivi': 'active_cases',
                        'dimessi_guariti': 'recovered',
                        'deceduti': 'deaths',
                        'totale_casi': 'total_cases',
                        'tamponi': 'tests_performed',
                        })
df = df.drop(['stato', 'note_it', 'note_en'], axis=1)

df['new_cases'] = (df['total_cases'] - df['total_cases'].shift(1)).fillna(0)
df['test_ratio'] = df['total_cases'] / df['tests_performed']
df['test_ratio_last_day'] = ((df['total_cases'] - df['total_cases'].shift(1)) /
                             (df['tests_performed'] - df['tests_performed'].shift(1))
                             ).fillna(0)


#%%
df_t = df.melt(id_vars='date', var_name='metric', value_name='amount')
fig = px.line(x='date', y='amount', color='metric', data_frame=df_t)
fig.update_layout(updatemenus=[pf.get_log_linear_buttons()])
fig.show()
