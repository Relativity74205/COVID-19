from typing import Tuple

import numpy as np
import pandas as pd
import main_functions as mf


#%%
df = mf.get_csse_data('deaths', min_cases=0, rolling_window=1)
df_germany = df[df.country == 'Germany']

#%%
def calculate_case_ci(date, deaths: int, p_min: float, p_max: float, n: int) \
        -> Tuple[int, int]:
    print(date)
    try:
        amount_digits = int(np.log10(deaths + 0.001)) + 1
    except OverflowError:
        amount_digits = 0
    min_cases = None
    delta_cases = 10**amount_digits
    cases = int(int(0.8 * deaths / p_max)/10**amount_digits)*10**amount_digits
    while True:
        arr_p = np.random.uniform(p_min, p_max, n)
        # arr_p = np.max(np.random.normal(p_mu, p_sigma, n), 0)
        arr_deaths_expected = np.random.binomial(cases, arr_p, n)
        deaths_expected_lower_ci = np.quantile(arr_deaths_expected, 0.025)
        deaths_expected_upper_ci = np.quantile(arr_deaths_expected, 0.975)
        if deaths_expected_upper_ci > deaths and min_cases is None:
            min_cases = cases
        if deaths_expected_lower_ci > deaths:
            max_cases = cases
            break
        cases += delta_cases

    return min_cases, max_cases


s_cases_ci = df_germany.apply(lambda row: calculate_case_ci(row.date, row.deaths, 0.003, 0.01, 1000), axis=1)
#%%
df_cases_ci = pd.DataFrame(s_cases_ci.tolist(), index=s_cases_ci.index, columns=['cases_lower_ci',
                                                                                 'cases_upper_ci'])
df_germany2 = df_germany.join(df_cases_ci)

#%%
df_germany_short = df_germany2[['date', 'cases_lower_ci', 'cases_upper_ci']]
df_germany_short['delta_cases_lower_ci'] = df_germany_short['cases_lower_ci'] - df_germany_short['cases_lower_ci'].shift(1).fillna(0)
df_germany_short['delta_cases_upper_ci'] = df_germany_short['cases_upper_ci'] - df_germany_short['cases_upper_ci'].shift(1).fillna(0)
df_germany_short_t = df_germany_short.melt(id_vars='date')

import plotly.express as px
fig = px.line(x='date', y='value', color='variable', data_frame=df_germany_short_t)
# fig.update_yaxes(type='log')
fig.show()
# cases_lower_ci, cases_upper_ci = calculate_case_ci(0, 0.003, 0.01, 10000)
# print(cases_lower_ci)
# print(cases_upper_ci)

# n = 10000
#
# deaths = 400
# # p_mu = 0.0094
# p_mu = 0.01
# p_sigma = 0.001
# p = 0.01
#
# np.random.seed(42)
# valid_cases = []
# # for cases in range(int(deaths * 100 * 0.5), int(deaths * 100 * 1.5), 1000):
# for cases in range(25000, 55000, 250):
#     print(f'{cases=}')
#     # for _ in range(n):
#     alpha = deaths
#     beta = cases - alpha
#     # p = np.random.normal(p_mu, p_sigma)
#     # arr = np.random.binomial(cases, max(0, p))
#     arr = np.random.beta(alpha, beta, n)
#     results = (arr - p) > 0
#     # prop = arr > deaths
#     valid_cases.append({'cases': cases, 'prop': np.mean(results)})
#
# df = pd.DataFrame(valid_cases)

#
# n = 10000
#
# deaths = 100
# # p_mu = 0.0094
# p_mu = 0.01
# p_sigma = 0.001
# p = 0.01
#
# np.random.seed(42)
# valid_cases = []
# # for cases in range(int(deaths * 100 * 0.5), int(deaths * 100 * 1.5), 1000):
# for cases in range(5000, 15000, 100):
#     print(f'{cases=}')
#     results = []
#     for _ in range(n):
#         p = 0.01
#         arr = np.random.binomial(cases, max(0, p))
#         prop = arr > deaths
#         results.append(prop)
#
#     valid_cases.append({'cases': cases, 'prop': abs(1 - np.mean(results))})
#
# df = pd.DataFrame(valid_cases)