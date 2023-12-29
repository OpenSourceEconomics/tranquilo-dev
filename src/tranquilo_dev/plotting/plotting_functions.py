import plotly.graph_objects as go

LABELS = {
    "dfols": "DF-OLS",
    "tranquilo": "Tranquilo-Scalar",
    "tranquilo_default": "Tranquilo-Scalar",
    "tranquilo_ls_default": "Tranquilo-LS",
    "tranquilo_ls": "Tranquilo-LS",
    "nag_bobyqa": "NAG-BOBYQA",
    "nlopt_bobyqa": "NlOpt-BOBYQA",
    "nlopt_neldermead": "NlOpt-Nelder-Mead",
    "scipy_neldermead": "SciPy-Nelder-Mead",
    "tao_pounders": "TAO-Pounders",
    "pounders": "Pounders",
}

# ======================================================================================
# Profile plot updates
# ======================================================================================


def update_scalar_benchmark_profile_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    return fig


def update_ls_benchmark_profile_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 40)
    return fig


def update_parallel_benchmark_profile_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_noisy_benchmark_profile_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_scalar_vs_ls_benchmark_profile_plot(fig):
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    return fig


# ======================================================================================
# Deviation plot updates
# ======================================================================================


def update_scalar_benchmark_deviation_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 300)
    return fig


def update_ls_benchmark_deviation_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 400)
    return fig


def update_parallel_benchmark_deviation_plot(fig):
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 50)
    return fig


def update_noisy_benchmark_deviation_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_scalar_vs_ls_benchmark_deviation_plot(fig):
    fig = _update_legend(fig)
    fig = _update_xrange(fig, 0, 500)
    return fig


# ======================================================================================
# Shared functions
# ======================================================================================


def _update_xrange(fig, lower, upper):
    fig = go.Figure(fig)  # makes a copy of the figure
    fig.update_xaxes(range=[lower, upper])
    return fig


def _update_labels(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    for trace in fig.data:
        trace.update(name=LABELS[trace.name])
    return fig


def _update_legend(fig):
    fig = go.Figure(fig)  # makes a copy of the figure
    fig.update_layout(
        legend_title="Algorithm",
        legend_title_side="top",
    )
    return fig
