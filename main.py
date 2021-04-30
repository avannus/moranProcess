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
experimentPopulation = 20
experimentCount = 9
trialCount = 1000

gens = []
successes = []
for x in range(experimentCount):
    gens.append(0)
    successes.append(0)
    for y in range(trialCount):
        startAllelePop = (experimentPopulation / (experimentCount + 1)) * (x + 1)
        current_seed = y
        allele_counts = neutral_moran(experimentPopulation, startAllelePop, current_seed)
        if y < 10:  # only save first 10 graphs
            plt.clf()  # clear figure
            plt.cla()  # clear axes
            plt.plot(allele_counts)
            plt.xlabel("Generations")
            plt.ylabel("Population")
            plt.title(
                "Neutral Moran Population:{} Starting Allele Population:{}, Seed:{}".format(experimentPopulation,
                                                                                            startAllelePop,
                                                                                            current_seed))
            plt.savefig(
                "graphs/Neutral Moran Pop:{} Start Allele Pop:{}, Seed:{}".format(experimentPopulation, startAllelePop,
                                                                                  current_seed))
        gens[x] += len(allele_counts)
        if allele_counts[-1][0] != 0:
            successes[x] += 1

#   calc avg success rate per experiment
avgSuccessRates = []
for x in successes:
    avgSuccessRates.append(float(x) / float(trialCount))
startingRatios = []
for x in range(len(successes)):
    startingRatios.append(float(x + 1) / float(experimentCount + 1))

plt.clf()
plt.cla()
plt.plot(startingRatios, avgSuccessRates, 'ro')
plt.plot([.1, .2, .3, .4, .5, .6, .7, .8, .9], [.1, .2, .3, .4, .5, .6, .7, .8, .9], 'b-')
plt.axis([0, 1, 0, 1])
plt.xlabel("Starting %")
plt.ylabel("Fixation Rate")
plt.title("Fixation Rate vs. Starting %")
plt.savefig(
    "Fixation Rate Pop:{} Exp Count:{} Trial Count:{}".format(experimentPopulation, experimentCount, trialCount))
#   calc avg gens per experiment
avgGens = []
for x in gens:
    avgGens.append(x / trialCount)

print "Completed in {} seconds.".format((datetime.now() - timeToRun).seconds)
