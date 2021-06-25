from collections import defaultdict

import numpy as np
import pandas as pd
import plotly.express as px

from Pop import Pop
import config as c


infected_by_outcome = defaultdict(list)
ratio_infected_practice_list = defaultdict(list)


np.random.seed(43)
for i in range(c.initial_infected_pop):
    patient_zero = Pop(i)
    patient_zero.infected(0)
    infected_by_outcome[patient_zero.outcome_day].append(patient_zero)

list_healthy = [Pop(i) for i in range(1, c.total_pop)]
list_recovered = []
list_deaths = []

populations = list()
ratio_healthy = len(list_healthy) / c.total_pop
for day in range(1, c.end_day + 1):
    infection_end_list = infected_by_outcome[day]
    for _ in range(len(infection_end_list)):
        pop = infection_end_list.pop()
        if pop.outcome_death:
            pop.death(day)
            list_deaths.append(pop)
        else:
            pop.recovered(day)
            list_recovered.append(pop)

    new_infections = Pop.infections_starting[day]

    arr_gets_really_infected = np.random.random(new_infections)
    for infected_prob in arr_gets_really_infected:
        if len(list_healthy) > 0:
            if infected_prob < ratio_healthy:
                pop: Pop = list_healthy.pop()
                pop.infected(day)
                infected_by_outcome[pop.outcome_day].append(pop)
                ratio_healthy = len(list_healthy) / c.total_pop
                ratio_infected_practice_list[day].append(1)
            else:
                ratio_infected_practice_list[day].append(0)

    populations.append({'day': day,
                        'healthy': len(list_healthy),
                        'infected': sum([len(v) for k, v in infected_by_outcome.items()]),
                        'recovered': len(list_recovered),
                        'deaths': len(list_deaths)
                        })

df = pd.DataFrame(populations)
df['delta_recovered'] = df['recovered'] - df['recovered'].shift(1).fillna(0)
df['delta_infected'] = df['infected'] - df['infected'].shift(1).fillna(0) + df['delta_recovered']

#%%
df_t = df.melt(id_vars='day', var_name='metric', value_name='pop_size')
fig = px.line(x='day', y='pop_size', color='metric', data_frame=df_t)
fig.show()

#%%
ratio_infected_practice_list_sum = {k: np.mean(v)*c.R for k, v in ratio_infected_practice_list.items()}
df_mean_infections_per_day = pd.DataFrame({'day': list(ratio_infected_practice_list_sum.keys()),
                                           'mean_infected': list(ratio_infected_practice_list_sum.values())
                                           })
fig = px.line(x='day', y='mean_infected', data_frame=df_mean_infections_per_day)
fig.show()
