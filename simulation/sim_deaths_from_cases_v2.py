from collections import defaultdict

import numpy as np
import pandas as pd
import plotly.express as px

from Pop import Pop
import config as c


infected_by_outcome = defaultdict(list)


np.random.seed(43)
for i in range(c.initial_infected_pop):
    patient_zero = Pop(i)
    patient_zero.infected(0)
    infected_by_outcome[patient_zero.outcome_day].append(patient_zero)

list_healthy = [Pop(i) for i in range(1, c.total_pop)]
list_recovered = []
list_deaths = []

populations = list()
for day in range(1, 301):
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
    for new_infection in range(new_infections):
        try:
            pop: Pop = list_healthy.pop()
            pop.infected(day)
            infected_by_outcome[pop.outcome_day].append(pop)
        except IndexError:
            pass
    populations.append({'day': day,
                        'healthy': len(list_healthy),
                        'infected': sum([len(v) for k, v in infected_by_outcome.items()]),
                        'recovered': len(list_recovered),
                        'deaths': len(list_deaths)
                        })

df = pd.DataFrame(populations)

#%%
df_t = df.melt(id_vars='day', var_name='metric', value_name='pop_size')
fig = px.line(x='day', y='pop_size', color='metric', data_frame=df_t)
fig.show()
