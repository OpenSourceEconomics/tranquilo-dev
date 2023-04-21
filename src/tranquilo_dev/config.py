"""This module contains the general configuration of the project."""
from pathlib import Path


SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
PUBLIC = BLD.joinpath("public").resolve()

SPHINX = ROOT.joinpath("docs/source/").resolve()
SPHINX_PAGES_BLD = SPHINX.joinpath("bld").resolve()
SPHINX_STATIC_BLD = SPHINX.joinpath("_static/bld").resolve()

RUN_DETERMINISTIC = True
RUN_NOISY = False
# In compat_mode algorithm_output is removed from the tranquilo results. This avoids
# pickling problems if different versions of tranquilo are compared to each other.
COMPAT_MODE = True


N_CORES = 10

PROBLEM_SETS = {}
if RUN_DETERMINISTIC:
    PROBLEM_SETS["mw"] = {
        "name": "more_wild",
        "exclude": ["brown_almost_linear_medium"],
    }
if RUN_NOISY:
    PROBLEM_SETS["mw_noisy"] = {
        "name": "more_wild",
        "exclude": "brown_almost_linear_medium",
        "additive_noise": True,
        "additive_noise_options": {"distribution": "normal", "std": 0.1},
        "seed": 925408,
    }


def _n_evals(*args, **kwargs):  # noqa: U100
    return 5


_deterministic_competition = {
    "nlopt_bobyqa": {"algorithm": "nlopt_bobyqa"},
    "nag_bobyqa": {"algorithm": "nag_pybobyqa"},
    "nag_dfols": {"algorithm": "nag_dfols"},
}

_noisy_competition = {
    "nag_bobyqa_noisy": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals,
        },
    },
    "nag_dfols_noisy": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals,
        },
    },
}

COMPETITION = {}
if RUN_DETERMINISTIC:
    COMPETITION.update(_deterministic_competition)
if RUN_NOISY:
    COMPETITION.update(_noisy_competition)


_deterministic_plots = {
    "competition_nag_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa",
        ],
        "profile_plot_options": {
            "y_precision": 1e-3,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
        "report_options": {
            "y_precision": 1e-3,
            "stopping_criterion": "y",
            "runtime_measure": "n_evaluations",
            "normalize_runtime": True,
            "include_all_tracebacks": False,
            "include_all_non_converged": False,
        },
    },
    "competition_nlopt_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nlopt_bobyqa",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
        "report_options": {
            "y_precision": 1e-3,
            "stopping_criterion": "y",
            "runtime_measure": "n_evaluations",
            "normalize_runtime": True,
            "include_all_tracebacks": False,
            "include_all_non_converged": False,
        },
    },
    "competition_ls": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "nag_dfols",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
        "report_options": {
            "y_precision": 1e-3,
            "stopping_criterion": "y",
            "runtime_measure": "n_evaluations",
            "normalize_runtime": True,
            "include_all_tracebacks": False,
            "include_all_non_converged": False,
        },
    },
}

_noisy_plots = {
    "competition_scalar_noisy": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa",
            "nag_bobyqa_noisy",
        ],
        "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "competition_ls_noisy": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "nag_dfols",
            "nag_dfols_noisy",
        ],
        "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
}


PLOT_CONFIG = {}
if RUN_DETERMINISTIC:
    PLOT_CONFIG.update(_deterministic_plots)
if RUN_NOISY:
    PLOT_CONFIG.update(_noisy_plots)


TRANQUILO_BASE_OPTIONS = {
    "algo_options": {
        "disable_convergence": False,
        "silence_experimental_warning": True,
    },
}
