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


def sum_1(N, i):
    sum1 = 0
    for j in range(1, i + 1):
        sum1 += float(N - i) / float(N - j)
    return sum1


def sum_2(N, i):
    sum2 = 0
    for j in range(i + 1, N):
        sum2 += float(i) / float(j)
    return sum2


timeToRun = datetime.now()
"""
Configure experimental variables
"""
experimentPopulation = 20
experimentCount = 19
trialCount = 10000

startAllelePop = []

gens = []
fixationsExperimentally = []
for x in range(experimentCount):
    gens.append(0)
    fixationsExperimentally.append(0)
    startAllelePop.append(experimentPopulation / (experimentCount + 1) * (x + 1))
    for y in range(trialCount):
        current_seed = y
        allele_counts = neutral_moran(experimentPopulation, startAllelePop[x], current_seed)
        if y < 10:  # only save first 10 graphs
            plt.clf()  # clear figure
            plt.cla()  # clear axes
            plt.plot(allele_counts)
            plt.xlabel("Generations")
            plt.ylabel("Population")
            plt.title(
                "Moran Neutral Drift N = {}, i = {}, Seed = {}".format(experimentPopulation, startAllelePop[x],
                                                                       current_seed))
            plt.savefig(
                "graphs/Neutral Drift N = {} i = {}, Seed = {}".format(experimentPopulation, startAllelePop[x],
                                                                       current_seed))
        gens[x] += len(allele_counts)
        if allele_counts[-1][0] != 0:
            fixationsExperimentally[x] += 1

startingRatios = []
for x in range(len(fixationsExperimentally)):
    startingRatios.append(float(x + 1) / float(experimentCount + 1))

#   define theoretical success rate per experiment
fixationRatioMath = []
for x in startingRatios:
    fixationRatioMath.append(x)

#   calc avg success rate per experiment
fixationRatiosAvg = []
for x in fixationsExperimentally:
    fixationRatiosAvg.append(float(x) / float(trialCount))

plt.clf()
plt.cla()
plt.plot(startingRatios, fixationRatioMath, 'b-')
plt.plot(startingRatios, fixationRatiosAvg, 'ro')
plt.axis([0, 1, 0, 1])
plt.xlabel("Starting %")
plt.ylabel("Fixation Rate")
plt.title("Fixation Rate vs. Starting %")
plt.savefig(
    "Fixation Rate Pop:{} Exp Count:{} Trial Count:{}".format(experimentPopulation, experimentCount, trialCount))

#   define theoretical gens per experiment
generationsMath = []
experimentRatios = []
for x in range(1, experimentPopulation):
    generationsMath.append(experimentPopulation * (sum_1(experimentPopulation, x) + sum_2(experimentPopulation, x)))
    experimentRatios.append(float(x) / float(experimentPopulation))

#   calc avg gens per experiment
generationsAvg = []
for x in gens:
    generationsAvg.append(x / trialCount)
plt.clf()
plt.cla()
plt.plot(experimentRatios, generationsMath, 'b-')
plt.plot(startingRatios, generationsAvg, 'ro')
plt.xlabel("Starting Allele Ratio")
plt.ylabel("Generations")
plt.title("Generations vs. Starting Allele Ratio")
plt.savefig(
    "Generation Count Pop:{} Exp Count:{} Trial Count:{}".format(experimentPopulation, experimentCount, trialCount))

print "Completed at {} in {} seconds.".format(datetime.now(), (datetime.now() - timeToRun).seconds)
