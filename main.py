from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


def neutral_moran(N, i=1, seed=0):
    """
    Return the population counts for the Moran process with neutral drift.
    """
    population = [0 for _ in range(i)] + [1 for _ in range(N - i)]
    counts = [(population.count(0), population.count(1))]
    np.random.seed(seed)
    while len(set(population)) == 2:
        reproduce_index = np.random.randint(N)
        eliminate_index = np.random.randint(N)
        population[eliminate_index] = population[reproduce_index]
        counts.append((population.count(0), population.count(1)))
    return counts


timeToRun = datetime.now()
"""
Configure experimental variables
"""
initPop = 20
experimentCount = 9
trialCount = 1000

gens = []
successes = []
for x in range(experimentCount):
    gens.append(0)
    successes.append(0)
    for y in range(trialCount):
        startAllelePop = (initPop / (experimentCount + 1)) * (x + 1)
        current_seed = y
        allele_counts = neutral_moran(initPop, startAllelePop, current_seed)
        if y < 10:  # only save first 10 graphs
            plt.clf()  # clear figure
            plt.cla()  # clear axes
            plt.plot(allele_counts)
            plt.xlabel("Generations")
            plt.ylabel("Population")
            plt.title(
                "Neutral Moran Population:{} Starting Allele Population:{}, Seed:{}".format(initPop, startAllelePop,
                                                                                            current_seed))
            plt.savefig(
                "graphs/Neutral Moran Pop:{} Start Allele Pop:{}, Seed:{}".format(initPop, startAllelePop,
                                                                                  current_seed))
        gens[x] += len(allele_counts)
        if allele_counts[-1][0] != 0:
            successes[x] += 1
# for x in successes:
#     print "Successes: {}".format(x)
# for x in gens:
#     print "Gens: {}".format(x)
"""
TODO make 2 graphs
    1: plotting success % as a function of starting %
    2: plotting generations as a function of starting % (with a given population)
"""
#   calc avg gens per experiment
avgGens = []
for x in gens:
    avgGens.append(x / trialCount)
#   calc avg success rate per experiment
avgSuccessRates = []
for x in successes:
    avgSuccessRates.append(float(x) / float(trialCount))
print avgGens
print avgSuccessRates
print successes
print "Completed in {} seconds.".format((datetime.now() - timeToRun).seconds)
