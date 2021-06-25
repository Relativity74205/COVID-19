import numpy as np
import pymc3 as pm


with pm.Model() as model:
    n_prior = pm.Uniform('n', 5000, 15000)
    # p_prior = pm.Uniform('p', 0.009, 0.011)

    obs = pm.Binomial('obs', n=n_prior, p=0.01, observed=100)

    trace = pm.sample(1000, chains=4, tune=500)  # , target_accept=0.9)

print(trace[0])
print(trace['n'].mean())
print(trace['n'].min())
print(trace['n'].max())
# np.mean(trace['n'])
# basic_model = pm.Model()
#
# with basic_model:
#
#     # Priors for unknown model parameters
#     alpha = pm.Normal('alpha', mu=0, sigma=10)
#     beta = pm.Normal('beta', mu=0, sigma=10, shape=2)
#     sigma = pm.HalfNormal('sigma', sigma=1)
#
#     # Expected value of outcome
#     mu = alpha + beta[0]*X1 + beta[1]*X2
#
#     # Likelihood (sampling distribution) of observations
#     Y_obs = pm.Normal('Y_obs', mu=mu, sigma=sigma, observed=Y)
