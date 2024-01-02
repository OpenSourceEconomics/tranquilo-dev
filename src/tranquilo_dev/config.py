"""This module contains the general configuration of the project.

Below an overview of the non-trivial concepts:

PROBLEM_SETS: This is a dictionary that defines the problems that can be used in
benchmarks. The keys are names, the values are dictionaries with keyword arguments for
`em.get_benchmark_problems`.

COMPETITION: This is a dictionary that defines the optimizer configurations against
which we want to compare tranquilo. The keys are the names of the optimizer
configurations, the values are dictionaries with keyword arguments for the minimization.

PLOT_CONFIG: This is a dictionary that defines which problem-optimizer combinations are
plotted against each other. Only combinations that are used in some plot will actually
run.

"""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
PUBLIC = BLD.joinpath("public").resolve()

RUN_DETERMINISTIC = True
RUN_NOISY = True
COMPAT_MODE = False

NOISY_Y_TOL = 0.01
DETERMINISTIC_Y_TOL = 1e-3


def get_max_criterion_evaluations(noisy):
    return 5_000 if noisy else 2_000


def get_max_iterations(noisy, functype):  # noqa: U100
    return 500 if functype == "ls" else 2000


def get_tranquilo_version(functype):
    return "tranquilo" if functype == "scalar" else "tranquilo_ls"


N_CORES = 10

PROBLEM_SETS = {
    "mw": {
        "name": "more_wild",
        "exclude": ["brown_almost_linear_medium"],
    },
    "mw_noisy": {
        "name": "more_wild",
        "exclude": "brown_almost_linear_medium",
        "additive_noise": True,
        "additive_noise_options": {"distribution": "normal", "std": 1.2},
        "seed": 925408,
    },
}


def _n_evals_5(*args, **kwargs):  # noqa: U100
    return 5


def _n_evals_3(*args, **kwargs):  # noqa: U100
    return 3


def _n_evals_10(*args, **kwargs):  # noqa: U100
    return 10


COMPETITION = {
    "nlopt_bobyqa": {"algorithm": "nlopt_bobyqa"},
    "nag_bobyqa": {"algorithm": "nag_pybobyqa"},
    "dfols": {"algorithm": "nag_dfols"},
    "pounders": {"algorithm": "pounders"},
    "tao_pounders": {"algorithm": "tao_pounders"},
    "scipy_neldermead": {"algorithm": "scipy_neldermead"},
    "nlopt_neldermead": {"algorithm": "nlopt_neldermead"},
    "nag_bobyqa_noisy_3": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_3,
        },
    },
    "dfols_noisy_3": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_3,
        },
    },
    "nag_bobyqa_noisy_5": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_5,
        },
    },
    "dfols_noisy_5": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_5,
        },
    },
    "nag_bobyqa_noisy_10": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_10,
        },
    },
    "dfols_noisy_10": {
        "algorithm": "nag_dfols",
        "algo_options": {
            "noise_additive_level": 0.1,
            "noise_n_evals_per_point": _n_evals_10,
        },
    },
}

_deterministic_plots = {
    "competition_scalar": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
    "competition_ls": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "dfols",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
    "scalar_and_ls": {
        "problem_name": "mw",
        "scenarios": [
            "dfols",
            "tranquilo_ls_default",
            "nlopt_bobyqa",
            "tranquilo_default",
            "nlopt_neldermead",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
    "parallelization_ls": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_parallel_2",
            "tranquilo_ls_parallel_4",
            "tranquilo_ls_parallel_8",
            "dfols",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
            "runtime_measure": "n_batches",
        },
        "convergence_plot_options": {"n_cols": 6, "runtime_measure": "n_batches"},
        "deviation_plot_options": {"runtime_measure": "n_batches"},
    },
    "publication_scalar_benchmark": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_default",
            "nag_bobyqa",
            "nlopt_bobyqa",
            "nlopt_neldermead",
            "scipy_neldermead",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
    "publication_ls_benchmark": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_default",
            "dfols",
            "pounders",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
    "publication_parallel_benchmark": {
        "problem_name": "mw",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_parallel_2",
            "tranquilo_ls_parallel_4",
            "tranquilo_ls_parallel_8",
            "dfols",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
            "runtime_measure": "n_batches",
        },
        "convergence_plot_options": {"n_cols": 6, "runtime_measure": "n_batches"},
        "deviation_plot_options": {"runtime_measure": "n_batches"},
    },
    "publication_scalar_vs_ls_benchmark": {
        "problem_name": "mw",
        "scenarios": [
            "dfols",
            "tranquilo_default",
            "tranquilo_ls_default",
            "nlopt_bobyqa",
            "nlopt_neldermead",
            "pounders",
        ],
        "profile_plot_options": {
            "y_precision": DETERMINISTIC_Y_TOL,
            "normalize_runtime": True,
        },
        "convergence_plot_options": {"n_cols": 6},
    },
}

_noisy_plots = {
    "competition_scalar_noisy": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "tranquilo_default",
            "tranquilo_experimental",
            "nag_bobyqa_noisy_5",
        ],
        "profile_plot_options": {"y_precision": NOISY_Y_TOL, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "competition_ls_noisy": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "tranquilo_ls_default",
            "tranquilo_ls_experimental",
            "dfols_noisy_5",
        ],
        "profile_plot_options": {"y_precision": NOISY_Y_TOL, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "noisy_ls": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "dfols_noisy_3",
            "dfols_noisy_5",
            "dfols_noisy_10",
            "tranquilo_ls_default",
        ],
        "profile_plot_options": {"y_precision": NOISY_Y_TOL, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
    "publication_noisy_benchmark": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "dfols_noisy_3",
            "dfols_noisy_5",
            "dfols_noisy_10",
            "tranquilo_ls_default",
        ],
        "profile_plot_options": {"y_precision": NOISY_Y_TOL, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
}


PLOT_CONFIG = {}
if RUN_DETERMINISTIC:
    PLOT_CONFIG.update(_deterministic_plots)
if RUN_NOISY:
    PLOT_CONFIG.update(_noisy_plots)


UNUSED_PLOTS = {
    "noisy": {
        "problem_name": "mw_noisy",
        "scenarios": [
            "nag_bobyqa_noisy_3",
            "nag_bobyqa_noisy_5",
            "nag_bobyqa_noisy_10",
            "tranquilo_default",
        ],
        "profile_plot_options": {"y_precision": NOISY_Y_TOL, "normalize_runtime": True},
        "convergence_plot_options": {"n_cols": 6},
    },
}


TRANQUILO_BASE_OPTIONS = {
    "algo_options": {
        "disable_convergence": False,
        "silence_experimental_warning": True,
    },
}


BENCHMARK_CASES = []
for info in PLOT_CONFIG.values():
    for scenario in info["scenarios"]:
        BENCHMARK_CASES.append((info["problem_name"], scenario))


COMPETITION_CASES = [case for case in BENCHMARK_CASES if "tranquilo" not in case[1]]

TRANQUILO_CASES = [case for case in BENCHMARK_CASES if "tranquilo" in case[1]]
