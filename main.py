from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


def neutral_moran(N, i=1, seed=0):  # the moran processes iteration for a given population a given neutral allele
    """
    Return the population counts for the Moran process as an ordered pair of each population
        with neutral drift at each iteration
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
    """
    used for finding expected generations
    see https://wikimedia.org/api/rest_v1/media/math/render/svg/1357d063b01000efd7f85646e6721385b9245efd
    """
    sum1 = 0
    for j in range(1, i + 1):
        sum1 += float(N - i) / float(N - j)
    return sum1


def sum_2(N, i):
    """
    used for finding expected generations
    see https://wikimedia.org/api/rest_v1/media/math/render/svg/1357d063b01000efd7f85646e6721385b9245efd
    """
    sum2 = 0
    for j in range(i + 1, N):
        sum2 += float(i) / float(j)
    return sum2


def make_plot(xLabel, yLabel, title, fileName, plot1, plot1pair=None, plot1arg=None, plot2=None, plot2pair=None,
              plot2arg=None):
    plt.clf()
    plt.cla()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    actual_plot(plot1, plot1pair, plot1arg)
    if plot2 is not None:
        actual_plot(plot2, plot2pair, plot2arg)
    plt.savefig(fileName)


def actual_plot(plot, pair=None, arg=None):
    if pair is None:
        if arg is None:
            plt.plot(plot)
        else:
            plt.plot(plot, arg)
    else:
        if arg is None:
            plt.plot(plot, pair)
        else:
            plt.plot(plot, pair, arg)


"""
This is the start of the runtime code
Code runtime duration is tracked to give runtime feedback when changing experimental variables
"""
timeToRun = datetime.now()

"""
Configure experimental variables
Experiment population will be fixed for the entirety of the program
Experiment count will adjust the number of experiments preformed
Each experiment will have a unique starting population, equally spaced between 0 and N, the fixed experiment population
    excluding 0 and N
Each experiment will consist of multiple trials to gain an average. Each trial will be seeded with its trail number in
    order to make these experiments repeatable
Because there are a large number of trials, only the first 5 of each are saved as graphs to reduce file count
"""
experimentPopulation = 20
experimentCount = 19
trialCount = 10000
graphsSavedPerTrail = 5

"""
The following list variables will keep track of results throughout trials for graphing and analysis
Each index is an experiment
"""
allelePopulationExperiments = []
generationsUntilFixationExperiments = []
fixationsExperimentally = []

"""
The for loop contains all of the trails from all experiments
allele_counts holds the coordinates of the current trial
Only the first 10 trials are graphed 
"""
for x in range(experimentCount):
    generationsUntilFixationExperiments.append(0)
    fixationsExperimentally.append(0)
    allelePopulationExperiments.append(experimentPopulation / (experimentCount + 1) * (x + 1))
    for y in range(trialCount):
        current_seed = y
        allele_counts = neutral_moran(experimentPopulation, allelePopulationExperiments[x], current_seed)
        if y < graphsSavedPerTrail:  # only save first 10 Neutral Drift Trial Graphs
            make_plot("Generations", "Population",
                      "Moran Neutral Drift N = {}, i = {}, Seed = {}".format(experimentPopulation,
                                                                             allelePopulationExperiments[x],
                                                                             current_seed),
                      "Neutral Drift Trial Graphs/Neutral Drift N = {} i = {}, Seed = {}".format(experimentPopulation,
                                                                                                 allelePopulationExperiments[
                                                                                                     x], current_seed),
                      allele_counts)
            # plt.clf()  # clear figure
            # plt.cla()  # clear axes
            # plt.plot(allele_counts)
            # plt.xlabel("Generations")
            # plt.ylabel("Population")
            # plt.title(
            #     "Moran Neutral Drift N = {}, i = {}, Seed = {}".format(experimentPopulation,
            #                                                            allelePopulationExperiments[x],
            #                                                            current_seed))
            # plt.savefig(
            #     "Neutral Drift Trial Graphs/Neutral Drift N = {} i = {}, Seed = {}".format(experimentPopulation,
            #                                                                                allelePopulationExperiments[
            #                                                                                    x],
            #                                                                                current_seed))
        generationsUntilFixationExperiments[x] += len(allele_counts)  # stores the total generations, avg later
        if allele_counts[-1][0] != 0:  # if the ending state is a fixation in favor of the tracked allele
            fixationsExperimentally[x] += 1

#   define starting ratios for each experiment, used for graphing and calculations TODO move into experiment loop?
startingRatios = []
for x in range(len(fixationsExperimentally)):
    startingRatios.append(float(x + 1) / float(experimentCount + 1))

#   define mathematical success rate per experiment
fixationRatioMath = []
for x in startingRatios:
    fixationRatioMath.append(x)

#   calc avg success rate per experiment
fixationRatiosAvg = []
for x in fixationsExperimentally:
    fixationRatiosAvg.append(float(x) / float(trialCount))

#   plot success rate experiment vs math
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

#   define mathematical gens per experiment
generationsMath = []
experimentRatios = []
for x in range(1, experimentPopulation):
    generationsMath.append(experimentPopulation * (sum_1(experimentPopulation, x) + sum_2(experimentPopulation, x)))
    experimentRatios.append(float(x) / float(experimentPopulation))

#   calc avg gens per experiment TODO remove generationsAvg
generationsAvg = []
for x in generationsUntilFixationExperiments:
    generationsAvg.append(x / trialCount)

#   plot success rate experiment vs math
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
