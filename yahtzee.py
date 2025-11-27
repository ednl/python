from math import sqrt
import numpy as np
from secrets import randbits
rng = np.random.default_rng(randbits(128))

# Simulation parameters (constants)
DICE  = 5
MAJOR = (DICE + 1) // 2
SIDES = 6
BATCH = 10000
ERROR = 0.005

# Simulation progress variables
games = 0  # simulation counter
sum = 0    # total number of throws in all games
in3 = 0    # games that ended in at most 3 throws

# Simulation goal: average number of throws until Yahtzee
# https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford%27s_online_algorithm
mean = 0    # running mean
m2var = 0   # unscaled variance
stddev = 1  # standard deviation (init value >ERROR)

while stddev >= ERROR:
    for _ in range(BATCH):
        games += 1

        bins = np.zeros(SIDES, dtype=int)
        throws = 0  # number of throws of the dice
        high = 0    # highest count of one die value
        pips = 0    # which die value has the highest count

        while high < DICE:
            throws += 1

            # Roll remaining dice
            size = DICE - high
            bins += np.bincount(rng.integers(low=0, high=SIDES, size=size), minlength=SIDES)

            # Find or update highest count of any die value (pips)
            if high < MAJOR:
                # Switch is still possible
                pips = np.argmax(bins)  # index of max count
                high = bins[pips]       # max count
                if high < MAJOR:
                    bins = np.zeros(SIDES, dtype=int)  # reset
                    if high > 1:
                        bins[pips] = high  # restore
                    else:                  # high=1
                        high = 0           # re-roll with all dice
            else:
                # Majority reached, so die value locked in
                high = bins[pips]

        sum += throws
        in3 += 1 if throws < 4 else 0
        estm = sum / games
        delta = estm - mean
        mean += delta / games
        m2var += delta * (estm - mean)

    stddev = sqrt(m2var / games)
    print(stddev)

print(f'Yahtzee takes {mean:.2f} throws on average in {games}.')
print(f'At most three throws in {in3 / games * 100:.2f} percent of games.')
