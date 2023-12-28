import plotly.graph_objects as go

LABELS = {
    "dfols": "DF-OLS",
    "tranquilo": "Tranquilo-Scalar",
    "tranquilo_default": "Tranquilo-Scalar",
    "tranquilo_ls_default": "Tranquilo-LS",
    "tranquilo_ls": "Tranquilo-LS",
    "tranquilo_experimental": "Tranquilo-Scalar-Experimental",
    "tranquilo_ls_experimental": "Tranquilo-Experimental",
    "nag_bobyqa": "BOBYQA",
    "nlopt_bobyqa": "PYBOBYQA",
    "nlopt_neldermead": "Nelder-Mead",
    "scipy_neldermead": "SciPy-Nelder-Mead",
    "tao_pounders": "TAO-Pounders",
    "pounders": "Pounders",
}


def update_scalar_benchmark_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    return fig


def update_ls_benchmark_plot(fig):
    fig = _update_labels(fig)
    fig = _update_legend(fig)
    return fig


def update_parallel_benchmark_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_noisy_benchmark_plot(fig):
    fig = _update_legend(fig)
    return fig


def update_scalar_vs_ls_benchmark_plot(fig):
    fig = _update_legend(fig)
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
