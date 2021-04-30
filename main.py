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
initPop = 1000
experimentCount = 9
trialCount = 1
for x in range(experimentCount):
    for y in range(trialCount):
        startAllelePop = (initPop / (experimentCount + 1)) * (x + 1)
        seed = y
        plt.clf()  # clear figure
        plt.cla()  # clear axes
        plt.plot(neutral_moran(initPop, startAllelePop, seed))
        plt.xlabel("Generations")
        plt.ylabel("Population")
        plt.title("Neutral Moran Population:{} Start Allele Population:{}, Seed:{}".format(initPop, startAllelePop, seed))
        plt.savefig("graphs/Neutral Moran Pop:{} Start Allele Pop:{}, Seed:{}".format(initPop, startAllelePop, seed))
print "Completed in {} seconds.".format((datetime.now() - timeToRun).seconds)
