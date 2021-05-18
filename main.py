from functions import *
from multiprocessing.pool import ThreadPool

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
trialCount = 1000
graphsSavedPerExperiment = 0

experiment_data = []

alleleStartingPopulation = []
generationsUntilFixationExperiments = []
fixationCountsExperimentally = []
startingAlleleRatios = []

for x in range(experimentCount):
    experiment_data.append((0, 0, 0, 0))

"""
The for loop contains all of the trails from all experiments
allele_counts holds the coordinates of the current trial
Only the first 10 trials are graphed 
"""
thread_pool = ThreadPool(processes=experimentCount)
known_threads = {}
for x in range(experimentCount):
    known_threads[x] = thread_pool.apply_async(trial_runner, args=(
        x, population, trialCount, graphsSavedPerExperiment, experimentCount,))

thread_pool.close()
thread_pool.join()

for thread in known_threads:
    print known_threads[thread].get()
    alleleStartingPopulation.append(known_threads[thread].get()[0])
    generationsUntilFixationExperiments.append(known_threads[thread].get()[1])
    fixationCountsExperimentally.append(known_threads[thread].get()[2])
    startingAlleleRatios.append(known_threads[thread].get()[3])

for x in experiment_data:  # TODO rewrite? https://www.w3schools.com/python/python_tuples_unpack.asp
    alleleStartingPopulation.append(x[0])
    generationsUntilFixationExperiments.append(x[1])
    fixationCountsExperimentally.append(x[2])
    startingAlleleRatios.append(x[3])

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
