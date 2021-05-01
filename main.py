from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def moran_neutral(N, i, seed):
    """
    A moran processes iteration for a given population a given neutral allele
    Return the population counts for the Moran process as an ordered pair of each population
        with neutral drift at each iteration
    """
    populationModel = [0 for _ in range(i)] + [1 for _ in range(N - i)]
    populationModelOrderedPairs = [(populationModel.count(0), populationModel.count(1))]
    np.random.seed(seed)
    while len(set(populationModel)) > 1:
        reproduce_index = np.random.randint(N)
        eliminate_index = np.random.randint(N)
        populationModel[eliminate_index] = populationModel[reproduce_index]
        populationModelOrderedPairs.append((populationModel.count(0), populationModel.count(1)))
    return populationModelOrderedPairs


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


def make_new_plot(xLabel, yLabel, title, fileName, plot1, plot1pair=None, plot1arg=None, plot2=None, plot2pair=None,
                  plot2arg=None):
    plt.clf()
    plt.cla()
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plot_flexibly(plot1, plot1pair, plot1arg)
    if plot2 is not None:
        plot_flexibly(plot2, plot2pair, plot2arg)
    plt.savefig(fileName)


def plot_flexibly(plot, pair=None, arg=None):
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
Population will be fixed for the entirety of the program
Experiment count will adjust the number of experiments preformed
Each experiment will have a unique starting population, equally spaced between 0 and N, the fixed population
    excluding 0 and N
Each experiment will consist of multiple trials to gain an average. Each trial will be seeded with its trail number in
    order to make these experiments repeatable
Because there are a large number of trials, only the first 5 of each are saved as graphs to reduce file count
"""
population = 20
experimentCount = 19
trialCount = 100000
graphsSavedPerExperiment = 10

"""
The following list variables will keep track of results throughout trials for graphing and analysis
Each index is conceptually mapped to each experiment
"""
alleleStartingPopulation = []
generationsUntilFixationExperiments = []
fixationCountsExperimentally = []
startingAlleleRatios = []

"""
The for loop contains all of the trails from all experiments
allele_counts holds the coordinates of the current trial
Only the first 10 trials are graphed 
"""
for x in range(experimentCount):
    experimentRunTime = datetime.now()
    generationsUntilFixationExperiments.append(0)
    fixationCountsExperimentally.append(0)
    alleleStartingPopulation.append(population / (experimentCount + 1) * (x + 1))
    startingAlleleRatios.append(float(alleleStartingPopulation[x]) / float(population))
    for y in range(trialCount):
        current_seed = y
        allele_counts = moran_neutral(population, alleleStartingPopulation[x], current_seed)
        if y < graphsSavedPerExperiment:  # only save first 10 Neutral Drift Trial Graphs
            make_new_plot("Generations", "Population",
                          "Moran Neutral Drift N = {}, i = {}, Seed = {}".format(population,
                                                                                 alleleStartingPopulation[x],
                                                                                 current_seed),
                          "Neutral Drift Trial Graphs/N = {} i = {}, Seed = {}".format(population,
                                                                                       alleleStartingPopulation[x],
                                                                                       current_seed),
                          allele_counts)
        generationsUntilFixationExperiments[x] += len(allele_counts)  # stores the total generations, avg separately
        if allele_counts[-1][0] != 0:  # if the ending state is a fixation in favor of the tracked allele
            fixationCountsExperimentally[x] += 1
    print "Experiment # {} complete in {} seconds".format(x + 1, (datetime.now() - experimentRunTime).seconds)

"""
The expected fixation ratio is calculated
The experimentally derived fixation ratio is calculated
Both ratios are mapped together
"""
#   define mathematical success rate per experiment, mathematically equal to starting ratio
fixationRatioMath = []
for x in startingAlleleRatios:
    fixationRatioMath.append(x)
#   calc avg success rate per experiment
fixationRatiosAvg = []
for x in fixationCountsExperimentally:
    fixationRatiosAvg.append(float(x) / float(trialCount))
#   plot success rate experiment vs math
make_new_plot("Starting Allele Ratio", "Fixation Rate", "Fixation Rate vs. Starting Allele Ratio",
              "Fixation Rate Pop:{} Exp Count:{} Trial Count:{}".format(population, experimentCount,
                                                                        trialCount),
              startingAlleleRatios, fixationRatioMath, 'b-', startingAlleleRatios, fixationRatiosAvg, 'ro')

"""
The expected generation count is calculated
The experimentally derived generation count is calculated
Both ratios are mapped together
"""
#   define mathematically expected gens per experiment
#   this is calculated at for every starting allele count (where 0<i<N), not just where the experiments occur
generationsMath = []
experimentRatios = []
for x in range(1, population):
    generationsMath.append(population * (sum_1(population, x) + sum_2(population, x)))
    experimentRatios.append(float(x) / float(population))
#   calc avg gens per experiment
generationsAvg = []
for x in generationsUntilFixationExperiments:
    generationsAvg.append(x / trialCount)
#   plot success rate experiment vs math
make_new_plot("Starting Allele Ratio", "Generations", "Generations vs. Starting Allele Ratio",
              "Gen Count Pop:{} Exp Count:{} Trial Count:{}".format(population, experimentCount, trialCount),
              experimentRatios, generationsMath, 'b-', startingAlleleRatios, generationsAvg, 'ro')

print "Completed at {} in {} seconds.".format(datetime.now(), (datetime.now() - timeToRun).seconds)
