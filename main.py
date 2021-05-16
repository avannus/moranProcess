from datetime import *
from functions import *
import thread


"""
Population will be fixed for the entirety of the program
Experiment count will adjust the number of experiments preformed
Each experiment will have a unique starting population, equally spaced between 0 and N, the fixed population
    excluding 0 and N
Each experiment will consist of multiple trials to gain an average. Each trial will be seeded with its trail number in
    order to make these experiments repeatable
Because there are a large number of trials, only the first 5 of each are saved as graphs to reduce file count

The following list variables will keep track of results throughout trials for graphing and analysis
Each index is conceptually mapped to each experiment
"""
timeToRun = datetime.now()

population = 20
experimentCount = 19
trialCount = 100000
graphsSavedPerExperiment = 10

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
    generationsMath.append(population * sums(population, x))
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
