from collections import defaultdict

import numpy as np

import config as c


class Pop:
    total_infected: int = 0
    infections_starting = defaultdict(int)

    def __init__(self, pop_number: int):
        self.pop_number: int = pop_number
        self.state: int = 0
        self.day_infected = None
        self.day_recovered = None
        self.day_death = None
        self.outcome_death = None
        self.outcome_day = None

    def infected(self, infection_day: int):
        Pop.total_infected += 1

        self.state = 1
        self.day_infected = infection_day
        self.outcome_death = np.random.binomial(1, c.infection_fatality_rate)
        if self.outcome_death:
            outcome_time = int(round(np.random.normal(c.mean_time_to_death, c.sigma_time_to_death), 0))
        else:
            outcome_time = int(round(np.random.normal(c.mean_time_to_recovery, c.sigma_time_to_recovery), 0))
        self.outcome_day = infection_day + outcome_time
        incubation_time = np.random.normal(c.mean_incubation_time, c.sigma_incubation_time)
        amount_infected = np.random.poisson(c.R)
        infection_times = np.random.normal(c.mean_infection_time, c.sigma_infection_time, amount_infected)
        new_infections_in_days = [int(round(incubation_time + infection_time, 0)) for infection_time in infection_times]
        for infection_time in new_infections_in_days:
            Pop.infections_starting[infection_day + infection_time] += 1

    def recovered(self, recovery_day: int):
        self.state = 2
        self.day_recovered = recovery_day

    def death(self, death_day: int):
        self.state = 3
        self.day_death = death_day
