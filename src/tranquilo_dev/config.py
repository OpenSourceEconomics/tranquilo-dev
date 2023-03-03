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
    # "mw_noisy": {
    #     "name": "more_wild",
    #     "exclude": "brown_almost_linear_medium",
    #     "additive_noise": True,
    #     "additive_noise_options": {"distribution": "normal", "std": 0.1},
    #     "seed": 925408,
    # },
}


def _n_evals(*args, **kwargs):  # noqa: U100
    return 5


COMPETITION = {
    # "nlopt_bobyqa": {"algorithm": "nlopt_bobyqa"},
    "nag_bobyqa": {"algorithm": "nag_pybobyqa"},
    # "nag_bobyqa_noisy": {
    #     "algorithm": "nag_dfols",
    #     "algo_options": {
    #         "noise_additive_level": 0.1,
    #         "noise_n_evals_per_point": _n_evals,
    #     },
    # },
    "nag_dfols": {"algorithm": "nag_dfols"},
    # "nag_dfols_noisy": {
    #     "algorithm": "nag_dfols",
    #     "algo_options": {
    #         "noise_additive_level": 0.1,
    #         "noise_n_evals_per_point": _n_evals,
    #     },
    # },
}


PLOT_CONFIG = {
    "competition_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa",
            # "nag_bobyqa_noisy",
        ],
        "profile_plot_options": {"y_precision": 1e-3, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "competition_ls": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "nag_dfols",
            # "nag_dfols_noisy",
        ],
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
    # "competition_scalar_noisy": {
    #     "problem_name": "mw_noisy",
    #     "scenarios": [
    #         "tranquilo_default",
    #         "tranquilo_experimental",
    #         "nag_bobyqa",
    #         "nag_bobyqa_noisy",
    #     ],
    #     "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
    #     "convergence_plot_options": {"n_cols": 6},
    # },
    # "competition_ls_noisy": {
    #     "problem_name": "mw_noisy",
    #     "scenarios": [
    #         "tranquilo_ls_default",
    #         "tranquilo_ls_experimental",
    #         "nag_dfols",
    #         "nag_dfols_noisy",
    #     ],
    #     "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
    #     "convergence_plot_options": {"n_cols": 6},
    # },
    # "internal_scalar_noisy": {
    #     "problem_name": "mw_noisy",
    #     "scenarios": ["tranquilo_default", "tranquilo_experimental"],
    #     "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
    #     "convergence_plot_options": {"n_cols": 6},
    # },
    # "internal_ls_noisy": {
    #     "problem_name": "mw_noisy",
    #     "scenarios": ["tranquilo_ls_default", "tranquilo_ls_experimental"],
    #     "profile_plot_options": {"y_precision": 1e-2, "normalize_runtime": True},
    #     "convergence_plot_options": {"n_cols": 6},
    # },
}


TRANQUILO_BASE_OPTIONS = {
    "algo_options": {
        "disable_convergence": False,
        "silence_experimental_warning": True,
    },
}
