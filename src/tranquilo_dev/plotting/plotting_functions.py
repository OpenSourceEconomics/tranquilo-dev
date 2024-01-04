import itertools

import matplotlib
import matplotlib.pyplot as plt
from tranquilo_dev.config import LABELS


# ======================================================================================
# Config
# ======================================================================================

AXIS_LABELS = {
    "profile_plot": {
        "xlabel": "Computational budget (normalized)",
        "ylabel": "Share of solved problems",
    },
    "deviation_plot": {
        "xlabel": "Computational budget",
        "ylabel": "Average distance to optimum (normalized)",
    },
}

FIGURE_WIDTH = 14.69785  # textwidth of paper in cm
FIGURE_HEIGHT = 10.0

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
    # https://www.w3schools.com/colors/colors_picker.asp, and selecting a lighter shade)
    "green-light": "#8ab77b",
    "green-very-light": "#b6d2ad",
    "blue-light": "#7995b9",
    "blue-very-light": "#abbdd3",
    "blue-very-very-light": "#dee4ed",
}

COLORS = {
    # Tranquilo colors
    "Tranquilo-Scalar": TABLEAU_10_COLORS["teal"],
    "Tranquilo-LS": TABLEAU_10_COLORS["blue"],
    "Tranquilo-LS (2 cores)": TABLEAU_10_COLORS["blue-light"],
    "Tranquilo-LS (4 cores)": TABLEAU_10_COLORS["blue-very-light"],
    "Tranquilo-LS (8 cores)": TABLEAU_10_COLORS["blue-very-very-light"],
    # DFO-LS colors
    "DFO-LS": TABLEAU_10_COLORS["green"],
    "DFO-LS (3 evals)": TABLEAU_10_COLORS["green"],
    "DFO-LS (5 evals)": TABLEAU_10_COLORS["green-light"],
    "DFO-LS (10 evals)": TABLEAU_10_COLORS["green-very-light"],
    # Other colors
    "NAG-BOBYQA": TABLEAU_10_COLORS["orange"],
    "NlOpt-BOBYQA": TABLEAU_10_COLORS["red"],
    "NlOpt-Nelder-Mead": TABLEAU_10_COLORS["purple"],
    "SciPy-Nelder-Mead": TABLEAU_10_COLORS["pink"],
    "Pounders": TABLEAU_10_COLORS["gray"],
}


LEGEND_LABEL_ORDER = {
    "scalar_benchmark": [
        "Tranquilo-Scalar",
        "NAG-BOBYQA",
        "NlOpt-BOBYQA",
        "NlOpt-Nelder-Mead",
        "SciPy-Nelder-Mead",
    ],
    "ls_benchmark": [
        "Tranquilo-LS",
        "DFO-LS",
        "Pounders",
    ],
    "parallel_benchmark": [
        "Tranquilo-LS",
        "Tranquilo-LS (2 cores)",
        "Tranquilo-LS (4 cores)",
        "Tranquilo-LS (8 cores)",
        "DFO-LS",
    ],
    "noisy_benchmark": [
        "Tranquilo-LS",
        "DFO-LS (3 evals)",
        "DFO-LS (5 evals)",
        "DFO-LS (10 evals)",
    ],
    "scalar_vs_ls_benchmark": [
        "Tranquilo-LS",
        "DFO-LS",
        "Pounders",
        "Tranquilo-Scalar",
        "NlOpt-BOBYQA",
        "NlOpt-Nelder-Mead",
    ],
}


X_RANGE = {
    "profile_plot": {
        "scalar_benchmark": (1, 50),
        "ls_benchmark": (1, 40),
        "parallel_benchmark": (1,),
        "noisy_benchmark": (1,),
        "scalar_vs_ls_benchmark": (1, 50),
    },
    "deviation_plot": {
        "scalar_benchmark": (0, 300),
        "ls_benchmark": (0, 400),
        "parallel_benchmark": (0, 50),
        "noisy_benchmark": (0,),
        "scalar_vs_ls_benchmark": (0, 500),
    },
}

matplotlib.rcParams["font.size"] = 10
matplotlib.rcParams["font.sans-serif"] = "Fira Sans"
matplotlib.rcParams["font.family"] = "sans-serif"


# ======================================================================================
# Plotting function
# ======================================================================================


def plot_benchmark(data, plot, benchmark):
    """Create the base matplotlib figure.  # noqa: D406, D407, D400

    Args:
        data (dict): Dictionary containing the data to plot. Keys represent a single
            line in the plot. The values are dictionaries with keys "x" and "y".
        plot (str): Name of the plot to create. Must be in {"deviation_plot",
            "profile_plot"}.
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
        figsize=(_cm_to_inch(FIGURE_WIDTH), _cm_to_inch(FIGURE_HEIGHT))
    )
    for name, line in data.items():
        ax.plot(line["x"], line["y"], label=name, color=COLORS[name])

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
