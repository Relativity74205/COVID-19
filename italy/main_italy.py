import pandas as pd
import plotly.express as px

df_org = pd.read_csv('../data/COVID-19_italy/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')
df_org = df_org.rename(columns={'data': 'date',
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
df_org = df_org.drop(['stato', 'nuovi_attualmente_positivi'], axis=1)


#%%
df_t = df_org.melt(id_vars='date', var_name='metric', value_name='amount')
fig = px.line(x='date', y='amount', color='metric', data_frame=df_t)
fig.show()


#%%
df = df_org.copy()
df['test_ratio'] = df_org['total_cases'] / df_org['tests_performed']
df['test_ratio_last'] = (df_org['total_cases'] - df_org['total_cases'].shift(1)) / \
                        (df_org['tests_performed'] - df_org['tests_performed'].shift(1))
