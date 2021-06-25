import os
import pathlib

import altair as alt

import main_functions as mf

if pathlib.Path.cwd().name == 'corona':
    os.chdir('CSSE_data_analysis')


value_name = 'cases'
df_cases_tidy_filtered = mf.get_csse_data(value_name, min_cases=100, rolling_window=3)

#%%
alt.renderers.enable('vegascope')
alt.data_transformers.disable_max_rows()

selection = alt.selection_multi(fields=['series'], bind='legend')
alt.Chart(df_cases_tidy_filtered).mark_line().encode(
    x='date',
    y='cases',
    color='country',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
).interactive().display()
