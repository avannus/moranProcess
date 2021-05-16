import matplotlib.pyplot as plt
import numpy as np


def moran_neutral(N, i, seed):
    """
    A moran processes iteration for a given population a given neutral allele
    Return the population counts for the Moran process as an ordered pair of each population
        with neutral drift at each iteration
    """
    population_model = [0 for _ in range(i)] + [1 for _ in range(N - i)]
    population_model_ordered_pairs = [(population_model.count(0), population_model.count(1))]
    np.random.seed(seed)
    while len(set(population_model)) > 1:
        reproduce_index = np.random.randint(N)
        eliminate_index = np.random.randint(N)
        population_model[eliminate_index] = population_model[reproduce_index]
        population_model_ordered_pairs.append((population_model.count(0), population_model.count(1)))
    return population_model_ordered_pairs


def make_new_plot(x_label, y_label, title, file_name, plot1, plot1pair=None, plot1arg=None, plot2=None, plot2pair=None,
                  plot2arg=None):
    plt.clf()
    plt.cla()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plot_flexibly(plot1, plot1pair, plot1arg)
    if plot2 is not None:
        plot_flexibly(plot2, plot2pair, plot2arg)
    plt.savefig(file_name)


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


def sums(N, i):
    """
    used for finding expected generations
    see https://wikimedia.org/api/rest_v1/media/math/render/svg/1357d063b01000efd7f85646e6721385b9245efd
    """
    sum1 = 0
    for j in range(1, i + 1):
        sum1 += float(N - i) / float(N - j)
    for j in range(i + 1, N):
        sum1 += float(i) / float(j)
    return sum1
