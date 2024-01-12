"""Plotting function that create the publication ready figures.

Most of the plotting behavior can be configured by changing some global dictionaries:

- `AXIS_LABELS`: Contains the axis labels for each plot type.
- `X_RANGE`: Contains the x-axis range given each benchmark.
- `COLORS`: Contains the colors for each line given each benchmark.
- `LINE_WIDTH_UPDATES`: Contains the line width for each line given each benchmark.
- `LEGEND_LABEL_ORDER`: Contains the order of the legend labels given each benchmark.

"""
import itertools

import matplotlib
import matplotlib.pyplot as plt
from tranquilo_dev.config import LABELS


# ======================================================================================
# Plot Config
# ======================================================================================

FIGURE_WIDTH_IN_CM = 14.69785
FIGURE_HEIGHT_IN_CM = 10.0

AXIS_LABELS = {
    "profile_plot": {
        "xlabel": "Computational budget (normalized)",
        "ylabel": "Share of solved problems",
    },
    "deviation_plot": {
        "xlabel": "Computational budget",
        "ylabel": "Average distance to optimum (normalized)",
    },
    "convergence_plot": {
        "xlabel": "Computational budget",
        "ylabel": "Criterion value",
    },
}

X_RANGE = {
    "profile_plot": {
        # Publication plots
        "publication_scalar_benchmark": (1, 50),
        "publication_ls_benchmark": (1, 40),
        "publication_parallel_benchmark": (1, 6),
        "publication_noisy_benchmark": (1, 50),
        "publication_scalar_vs_ls_benchmark": (1, 50),
        # Development plots
        "development_competition_ls": (1,),
        "development_competition_scalar": (1,),
        "development_parallelization_ls": (1,),
        "development_noisy_ls": (1,),
    },
    "deviation_plot": {
        # Publication plots
        "publication_scalar_benchmark": (0, 300),
        "publication_ls_benchmark": (0, 400),
        "publication_parallel_benchmark": (0, 50),
        "publication_noisy_benchmark": (0, 5000),
        "publication_scalar_vs_ls_benchmark": (0, 500),
        # Development plots
        "development_competition_ls": (0,),
        "development_competition_scalar": (0,),
        "development_parallelization_ls": (0,),
        "development_noisy_ls": (0,),
    },
    "convergence_plot": {
        # Publication plots
        "publication_scalar_benchmark": (0,),
        "publication_ls_benchmark": (0,),
        "publication_parallel_benchmark": (0,),
        "publication_noisy_benchmark": (0,),
        "publication_scalar_vs_ls_benchmark": (0,),
        # Development plots
        "development_competition_ls": (0,),
        "development_competition_scalar": (0,),
        "development_parallelization_ls": (0,),
        "development_noisy_ls": (0,),
    },
}

# Colors
# ======================================================================================

DARK_GRAY = "#534a46"

TABLEAU_10_COLORS = {
    "blue": "#5778a4",
    "green": "#6a9f58",
    "orange": "#e49444",
    "red": "#d1615d",
    "teal": "#85b6b2",
    "yellow": "#e7ca60",
    "purple": "#a87c9f",
    "pink": "#f1a2a9",
    "brown": "#967662",
    "gray": "#b8b0ac",
    # Additional shades. (Taken by plugging in the color code of blue and green at
    # https://www.w3schools.com/colors/colors_picker.asp, and selecting a lighter /
    # darker color given some percentage.)
    "green-25": "#b7d2ad",
    "green-50": "#6ea45b",
    "green-75": "#37522d",
    "blue-75": "#abbed4",
    "blue-55": "#688ab1",
    "blue-35": "#3d5776",
    "blue-15": "#1a2532",
    # Experimental tranquilo colors
    "pink-70": "#ec7985",
    "pink-60": "#e64d5c",
    "pink-50": "#df2033",
    "pink-40": "#b31929",
    "pink-30": "#86131f",
}


BASE_COLORS = {
    "Tranquilo-Scalar": TABLEAU_10_COLORS["teal"],
    "Tranquilo-LS": TABLEAU_10_COLORS["blue"],
    "DFO-LS": TABLEAU_10_COLORS["green"],
    "NAG-BOBYQA": TABLEAU_10_COLORS["orange"],
    "NlOpt-BOBYQA": TABLEAU_10_COLORS["red"],
    "NlOpt-Nelder-Mead": TABLEAU_10_COLORS["purple"],
    "SciPy-Nelder-Mead": TABLEAU_10_COLORS["brown"],
    "Pounders": TABLEAU_10_COLORS["gray"],
    # Experimental tranquilo colors
    "Tranquilo-Scalar (Experimental)": TABLEAU_10_COLORS["pink"],
    "Tranquilo-LS (Experimental)": TABLEAU_10_COLORS["pink"],
}

PARALLEL_COLOR_UPDATES = {
    "Tranquilo-LS": TABLEAU_10_COLORS["blue-75"],
    "Tranquilo-LS (2 cores)": TABLEAU_10_COLORS["blue-55"],
    "Tranquilo-LS (4 cores)": TABLEAU_10_COLORS["blue-35"],
    "Tranquilo-LS (8 cores)": TABLEAU_10_COLORS["blue-15"],
    "Tranquilo-LS (Experimental, 2 cores)": TABLEAU_10_COLORS["pink-70"],
    "Tranquilo-LS (Experimental, 4 cores)": TABLEAU_10_COLORS["pink-50"],
    "Tranquilo-LS (Experimental, 8 cores)": TABLEAU_10_COLORS["pink-30"],
}

NOISY_COLOR_UPDATES = {
    "DFO-LS (3 evals)": TABLEAU_10_COLORS["green-25"],
    "DFO-LS (5 evals)": TABLEAU_10_COLORS["green-50"],
    "DFO-LS (10 evals)": TABLEAU_10_COLORS["green-75"],
}

COLORS = {
    # Publication plots
    "publication_scalar_benchmark": BASE_COLORS,
    "publication_ls_benchmark": BASE_COLORS,
    "publication_parallel_benchmark": {**BASE_COLORS, **PARALLEL_COLOR_UPDATES},
    "publication_noisy_benchmark": {**BASE_COLORS, **NOISY_COLOR_UPDATES},
    "publication_scalar_vs_ls_benchmark": BASE_COLORS,
    # Development plots
    "development_competition_ls": BASE_COLORS,
    "development_competition_scalar": BASE_COLORS,
    "development_parallelization_ls": {**BASE_COLORS, **PARALLEL_COLOR_UPDATES},
    "development_noisy_ls": {**BASE_COLORS, **NOISY_COLOR_UPDATES},
}

# Line width
# ======================================================================================
DEFAULT_LINE_WIDTH = 1.5

LINE_WIDTH_UPDATES = {
    "publication_parallel_benchmark": {
        "Tranquilo-LS (2 cores)": 1.6,
        "Tranquilo-LS (4 cores)": 1.7,
        "Tranquilo-LS (8 cores)": 1.8,
    },
    "publication_noisy_benchmark": {
        "DFO-LS (5 evals)": 1.6,
        "DFO-LS (10 evals)": 1.7,
    },
    "development_noisy_ls": {
        "DFO-LS (5 evals)": 1.6,
        "DFO-LS (10 evals)": 1.7,
    },
    "development_parallelization_ls": {
        "Tranquilo-LS (Experimental, 2 cores)": 1.6,
        "Tranquilo-LS (Experimental, 4 cores)": 1.7,
        "Tranquilo-LS (Experimental, 8 cores)": 1.8,
    },
}

# Legend
# ======================================================================================

LEGEND_LABEL_ORDER = {
    # Publication plots
    "publication_scalar_benchmark": [
        "Tranquilo-Scalar",
        "NAG-BOBYQA",
        "NlOpt-BOBYQA",
        "NlOpt-Nelder-Mead",
        "SciPy-Nelder-Mead",
    ],
    "publication_ls_benchmark": [
        "Tranquilo-LS",
        "DFO-LS",
        "Pounders",
    ],
    "publication_parallel_benchmark": [
        "Tranquilo-LS",
        "Tranquilo-LS (2 cores)",
        "Tranquilo-LS (4 cores)",
        "Tranquilo-LS (8 cores)",
        "DFO-LS",
    ],
    "publication_noisy_benchmark": [
        "DFO-LS (3 evals)",
        "DFO-LS (5 evals)",
        "DFO-LS (10 evals)",
        "Tranquilo-LS",
    ],
    "publication_scalar_vs_ls_benchmark": [
        "Tranquilo-LS",
        "DFO-LS",
        "Pounders",
        "Tranquilo-Scalar",
        "NlOpt-BOBYQA",
        "NlOpt-Nelder-Mead",
    ],
    # Development plots
    "development_competition_ls": [
        "Tranquilo-LS",
        "Tranquilo-LS (Experimental)",
        "DFO-LS",
    ],
    "development_competition_scalar": [
        "Tranquilo-Scalar",
        "Tranquilo-Scalar (Experimental)",
        "NlOpt-BOBYQA",
    ],
    "development_parallelization_ls": [
        "Tranquilo-LS (2 cores)",
        "Tranquilo-LS (4 cores)",
        "Tranquilo-LS (8 cores)",
        "Tranquilo-LS (Experimental, 2 cores)",
        "Tranquilo-LS (Experimental, 4 cores)",
        "Tranquilo-LS (Experimental, 8 cores)",
        "DFO-LS",
    ],
    "development_noisy_ls": [
        "DFO-LS (3 evals)",
        "DFO-LS (5 evals)",
        "DFO-LS (10 evals)",
        "Tranquilo-LS",
        "Tranquilo-LS (Experimental)",
    ],
}

# Font
# ======================================================================================

matplotlib.rcParams["font.size"] = 10
matplotlib.rcParams["font.sans-serif"] = "Fira Sans"
matplotlib.rcParams["font.family"] = "sans-serif"


# ======================================================================================
# Plotting function
# ======================================================================================


def plot_benchmark(data, plot, benchmark):
    """Create the base matplotlib figure.

    Args:
        data (dict): Dictionary containing the data to plot. Keys represent a single
            line in the plot. The values are dictionaries with keys "x" and "y".
        plot (str): Name of the plot to create. Must be in {"deviation_plot",
            "profile_plot", "convergence_plot"}.
        benchmark (str): Name of the benchmark.

    Returns:
        matplotlib.figure.Figure: The matplotlib figure.

    """
    x_range = X_RANGE[plot][benchmark]
    legend_label_order = LEGEND_LABEL_ORDER[benchmark]

    # Update label names
    data = {LABELS[name]: line for name, line in data.items()}

    # Create matplotlib base figure
    fig, ax = plt.subplots(
        figsize=(_cm_to_inch(FIGURE_WIDTH_IN_CM), _cm_to_inch(FIGURE_HEIGHT_IN_CM))
    )
    for name, line in data.items():
        lw = LINE_WIDTH_UPDATES.get(benchmark, {}).get(name, DEFAULT_LINE_WIDTH)
        ax.plot(
            line["x"],
            line["y"],
            label=name,
            color=COLORS[benchmark][name],
            linewidth=lw,
        )

    # Remove top and right border (spine)
    ax.spines[["right", "top"]].set_visible(False)

    # Set color of left and bottom spine
    ax.spines[["left", "bottom"]].set_color(DARK_GRAY)

    # Update ticks
    ax.tick_params(direction="in", width=0.75, colors=DARK_GRAY)

    # Update legend
    handles, labels = _get_sorted_legend_handles_and_labels(ax, legend_label_order)
    ax.legend(
        handles=_row_to_col_ordering(handles, ncol=3),
        labels=_row_to_col_ordering(labels, ncol=3),
        frameon=False,
        loc="upper center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.15),
        labelcolor=DARK_GRAY,
    )

    # Update axes
    ax.set_xlabel(AXIS_LABELS[plot]["xlabel"], color=DARK_GRAY)
    ax.set_ylabel(AXIS_LABELS[plot]["ylabel"], color=DARK_GRAY)
    ax.xaxis.label.set_color(DARK_GRAY)
    ax.yaxis.label.set_color(DARK_GRAY)
    ax.set_xlim(*x_range)
    if plot != "convergence_plot":
        ax.set_ylim(0, 1)

    return fig


def _cm_to_inch(cm):
    return cm * 0.393701


def _get_sorted_legend_handles_and_labels(ax, sorted_labels=None):
    handles, labels = ax.get_legend_handles_labels()
    sorted_labels = labels if sorted_labels is None else sorted_labels
    sorted_handles = [handles[labels.index(label)] for label in sorted_labels]
    return sorted_handles, sorted_labels


def _row_to_col_ordering(items, ncol):
    """Reorder frm row-major to column-major ordering.

    Transforms a list of items that are designed to be filled in a row-major order
    into a list of items that are designed to be filled in a column-major order.

    Taken from: https://stackoverflow.com/a/10101532.

    """
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])
