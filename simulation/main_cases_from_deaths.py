import numpy as np
import pandas as pd

n = 30000

deaths = 400
# p_mu = 0.0094
p_mu = 0.01
p_sigma = 0.001

np.random.seed(42)
valid_cases = []
for cases in range(25000, 55000, 100):
    print(f'{cases=}')
    results = []
    for _ in range(n):
        p = np.random.normal(p_mu, p_sigma)
        arr = np.random.binomial(cases, max(0, p))
        prop = arr > deaths
        results.append(prop)
    valid_cases.append({'cases': cases, 'prop': np.mean(results)})

df = pd.DataFrame(valid_cases)
