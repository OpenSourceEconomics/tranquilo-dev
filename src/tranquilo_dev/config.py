"""This module contains the general configuration of the project."""
from pathlib import Path


SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
PUBLIC = BLD.joinpath("public").resolve()


N_CORES = 10

PROBLEM_SETS = {
    "mw": {
        "name": "more_wild",
        "exclude": "brown_almost_linear_medium",
    },
}


COMPETITION = {
    "nlopt_bobyqa": {"algorithm": "nlopt_bobyqa"},
    "nag_bobyqa": {"algorithm": "nag_pybobyqa"},
    "nag_dfols": {"algorithm": "nag_dfols"},
    "pounders": {"algorithm": "pounders"},
    "nlopt_neldermead": {"algorithm": "nlopt_neldermead"},
    "scipy_neldermead": {"algorithm": "scipy_neldermead"},
}


PLOT_CONFIG = {
    "competition_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa",
            "nlopt_bobyqa",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "competition_ls": {
        "problem_name": "mw",
        "scenarios": ["tranquilo_ls_default", "tranquilo_ls_experimental", "nag_dfols"],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "internal_scalar": {
        "problem_name": "mw",
        "scenarios": ["tranquilo_default", "tranquilo_experimental"],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "internal_ls": {
        "problem_name": "mw",
        "scenarios": ["tranquilo_ls_default", "tranquilo_ls_experimental"],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "baseline_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_baseline",
            "tranquilo_default",
            "tranquilo_experimental",
            "nlopt_bobyqa",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "baseline_ls": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_baseline",
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "nag_dfols",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
}


TRANQUILO_BASE_OPTIONS = {
    "algo_options": {
        "disable_convergence": True,
        "stopping.max_iterations": 200,
        "silence_experimental_warning": True,
    },
}
