import seaborn as sns

from .logbook import logbook_to_pandas

sns.set_style("whitegrid")


def plot_fitness_evolution(estimator):
    """
    Parameters
    ----------
    estimator: Fitted GASearchCV

    Returns
    plot with the fitness value in each generation
    -------

    """
    fitness_history = estimator.history["fitness"]

    palette = sns.color_palette("rocket")
    sns.set(rc={'figure.figsize': (10, 10)})

    ax = sns.lineplot(x=range(len(estimator)), y=fitness_history,
                      markers=True,
                      palette=palette)
    ax.set_title('Fitness average evolution over generations')

    ax.set(xlabel='generations', ylabel=f'fitness ({estimator.scoring})')
    return ax


def plot_search_space(estimator, height=2, s=25, features: list = None):
    """
    Parameters
    ----------
    height: float, default=2
        Height if each facet
    s: float, default=5
        Size of the markers in scatter plot
    features: list, default=None
        Subset of features to plot, if 'None' it plots all the features by default
    estimator: Fitted GASearchCV

    Returns
    pair plot of the used hyperparameters during the search
    -------

    """
    df = logbook_to_pandas(estimator.logbook)
    if features:
        stats = df[features]
    else:
        variables = [*estimator.space.parameters, 'score']
        stats = df[variables]

    g = sns.PairGrid(stats, diag_sharey=False, height=height)
    g = g.map_upper(sns.scatterplot, s=s)
    g = g.map_lower(sns.kdeplot, shade=True)
    g = g.map_diag(sns.kdeplot, shade=True)
    return g
