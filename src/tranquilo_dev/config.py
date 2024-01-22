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
import socket
from pathlib import Path
from typing import NamedTuple

# ======================================================================================
# Paths
# ======================================================================================
SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
PUBLIC = BLD.joinpath("public").resolve()


# ======================================================================================
# Global Options
# ======================================================================================
class ProjectOptions(NamedTuple):
    """This class contains the global options of the project.

    The options are:
        - RUN_DETERMINISTIC (bool): Whether to run the deterministic benchmarks.
        - RUN_NOISY (bool): Whether to run the noisy benchmarks.

        - RUN_PUBLICATION_CASES (bool): Whether to run the benchmarks required for the
        publication figures.
        - RUN_DEVELOPMENT_CASES (bool): Whether to run the benchmarks required for the
        development figures.

        - DETERMINISTIC_Y_TOL (float): The tolerance for the deterministic benchmarks.
        - NOISY_Y_TOL (float): The tolerance for the noisy benchmarks.

        - PLOT_TYPES (tuple): The plot types that are being created. Must be an iterable
        with entries from {"profile_plot", "convergence_plot", "deviation_plot"}.

        - PROBLEM_SETS (tuple): The problem sets that are being used. Must be an
        iterable with entries from {"more_wild", "cartis_roberts"}.

    """

    # Do not alter the default values of this class for development purposes. Instead
    # set the options in the class instantiation below.

    RUN_DETERMINISTIC: bool = True
    RUN_NOISY: bool = True

    RUN_PUBLICATION_CASES: bool = True
    RUN_DEVELOPMENT_CASES: bool = True

    DETERMINISTIC_Y_TOL: float = 1e-3
    NOISY_Y_TOL: float = 0.01

    PLOT_TYPES: tuple[str] = ("profile_plot", "convergence_plot", "deviation_plot")
    PROBLEM_SETS: tuple[str] = ("more_wild", "cartis_roberts")

    N_CORES_DEFAULT: int = 1

    @property
    def n_cores(self):
        """Set the number of cores depending on the hostname."""
        hostnames_to_requested_cores = {
            # Tim's thinkpad
            "thinky": 16,
            # Janos' thinkpad
            "IZA-LAP479": 10,
        }
        hostname = socket.gethostname()
        return hostnames_to_requested_cores.get(hostname, self.N_CORES_DEFAULT)


# Set development options HERE and not in the class above
# ======================================================================================
OPTIONS = ProjectOptions(
    PLOT_TYPES=("profile_plot", "deviation_plot"),
    PROBLEM_SETS=("more_wild",),
)


def get_max_criterion_evaluations(noisy):
    return 5_000 if noisy else 2_000


def get_max_iterations(noisy, functype):  # noqa: U100
    return 500 if functype == "ls" else 2000


def get_tranquilo_version(functype):
    return "tranquilo" if functype == "scalar" else "tranquilo_ls"


TRANQUILO_BASE_OPTIONS = {
    "algo_options": {
        "disable_convergence": False,
        "silence_experimental_warning": True,
    },
}


def get_benchmark_problem_info(problem_set):
    info = {
        "more_wild": {
            # Number of additional draws per problem that are used to generate more
            # problems. For each problems n_draws new start vectors are drawn in the
            # vicinity of the original start vector, each defining a new problem.
            "n_additional_draws": 4,
            # Random number generator seed used to control the random draws.
            "seed": 440219,
        },
        "cartis_roberts": {
            "n_additional_draws": 0,
            "seed": None,
        },
    }

    if "mw" in problem_set:
        out = info["more_wild"]
    elif "cr" in problem_set:
        out = info["cartis_roberts"]
    return out


# ======================================================================================
# Benchmark sets and configurations
# ======================================================================================

# Exclude the following problems from the cartis_roberts set because their solution
# is undefined. See the cartis_roberts.py module in estimagic for reference.
_exlude_from_cartis_roberts = [
    "artif",
    "chandheq",
    "chemrcta",
    "drcavty1",
    "flosp2hh",
    "flosp2hl",
    "flosp2hm",
    "flosp2th",
    "flosp2tl",
    "flosp2tm",
    "luksan12",
    "luksan17",
    "penalty_1",
]

PROBLEM_SETS = {
    "mw": {
        "name": "more_wild",
        "exclude": ["brown_almost_linear_medium"],
    },
    "mw_noisy": {
        "name": "more_wild",
        "exclude": ["brown_almost_linear_medium"],
        "additive_noise": True,
        "additive_noise_options": {"distribution": "normal", "std": 1.2},
        "seed": 925408,
    },
    "cr": {
        "name": "cartis_roberts",
        "exclude": _exlude_from_cartis_roberts,
    },
    "cr_noisy": {
        "name": "cartis_roberts",
        "exclude": _exlude_from_cartis_roberts,
        "additive_noise": True,
        "additive_noise_options": {"distribution": "normal", "std": 1.2},
        "seed": 925408,
    },
}

# ======================================================================================
# Define competition. These are the optimizers against which tranquilo is compared.
# ======================================================================================


# Create evaluation functions for DFO-LS noisy cases
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

# ======================================================================================
# Plotting configuration
# --------------------------------------------------------------------------------------
# Note that keys for each plot configuration must adhere to the convention that they
# either start with "publication_" or "development_". Developments plots are stored
# in bld/figures while publication plots are stored in bld/bld_paper. Running
# experiments should be done with development plots.
# ======================================================================================

_deterministic_plots = {
    # Development / Experimental cases
    # ==================================================================================
    "development": {
        "scalar_benchmark": {
            "scenarios": [
                "tranquilo_default",
                "tranquilo_experimental",
                "nlopt_bobyqa",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
        "ls_benchmark": {
            "scenarios": [
                "tranquilo_ls_default",
                "tranquilo_ls_experimental",
                "dfols",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
        "parallel_benchmark": {
            "scenarios": [
                "tranquilo_ls_parallel_2",
                "tranquilo_ls_parallel_4",
                "tranquilo_ls_parallel_8",
                "tranquilo_ls_experimental_parallel_2",
                "tranquilo_ls_experimental_parallel_4",
                "tranquilo_ls_experimental_parallel_8",
                "dfols",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
                "runtime_measure": "n_batches",
            },
            "convergence_plot_options": {"n_cols": 6, "runtime_measure": "n_batches"},
            "deviation_plot_options": {"runtime_measure": "n_batches"},
        },
    },
    # Publication / Presentation cases
    # ==================================================================================
    "publication": {
        "scalar_benchmark": {
            "scenarios": [
                "tranquilo_default",
                "nag_bobyqa",
                "nlopt_bobyqa",
                "nlopt_neldermead",
                "scipy_neldermead",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
        "ls_benchmark": {
            "scenarios": [
                "tranquilo_ls_default",
                "dfols",
                "pounders",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
        "parallel_benchmark": {
            "scenarios": [
                "tranquilo_ls_default",
                "tranquilo_ls_parallel_2",
                "tranquilo_ls_parallel_4",
                "tranquilo_ls_parallel_8",
                "dfols",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
                "runtime_measure": "n_batches",
            },
            "convergence_plot_options": {"n_cols": 6, "runtime_measure": "n_batches"},
            "deviation_plot_options": {"runtime_measure": "n_batches"},
        },
        "scalar_vs_ls_benchmark": {
            "scenarios": [
                "dfols",
                "tranquilo_default",
                "tranquilo_ls_default",
                "nlopt_bobyqa",
                "nlopt_neldermead",
                "pounders",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.DETERMINISTIC_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
    },
}

_noisy_plots = {
    # Development / Experimental cases
    # ==================================================================================
    "development": {
        "noisy_benchmark": {
            "scenarios": [
                "dfols_noisy_3",
                "dfols_noisy_5",
                "dfols_noisy_10",
                "tranquilo_ls_default",
                "tranquilo_ls_experimental",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.NOISY_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
    },
    # Publication / Presentation cases
    # ==================================================================================
    "publication": {
        "noisy_benchmark": {
            "scenarios": [
                "dfols_noisy_3",
                "dfols_noisy_5",
                "dfols_noisy_10",
                "tranquilo_ls_default",
            ],
            "profile_plot_options": {
                "y_precision": OPTIONS.NOISY_Y_TOL,
                "normalize_runtime": True,
            },
            "convergence_plot_options": {"n_cols": 6},
        },
    },
}


# ======================================================================================
# Consolidate configuration
# ======================================================================================
def _add_problem_name_to_configs(plot_config, problem_name, development_or_publication):
    """Add id of the problem set to the plot configuration.

    New name of a plot configuration would look like:

    - "development_scalar_benchmark_mw"
    - "publication_ls_benchmark_mw"
    - "development_scalar_benchmark_mw_noisy"
    - ...

    """
    updated = {}
    for plot_name, info in plot_config.items():
        name = f"{development_or_publication}_{plot_name}_{problem_name}"
        updated[name] = {**info, "problem_name": problem_name}
    return updated


def _get_problem_name(problem_set, noisy):
    mapping = {
        "more_wild": "mw",
        "cartis_roberts": "cr",
    }
    name = mapping[problem_set]
    return f"{name}_noisy" if noisy else name


# Collect all plots that we actually want to run
# ======================================================================================
PLOT_CONFIG = {}

for problem_set in OPTIONS.PROBLEM_SETS:

    if OPTIONS.RUN_DETERMINISTIC:

        if OPTIONS.RUN_PUBLICATION_CASES:
            _updated_configs = _add_problem_name_to_configs(
                _deterministic_plots["publication"],
                problem_name=_get_problem_name(problem_set, noisy=False),
                development_or_publication="publication",
            )
            PLOT_CONFIG.update(_updated_configs)

        if OPTIONS.RUN_DEVELOPMENT_CASES:
            _updated_configs = _add_problem_name_to_configs(
                _deterministic_plots["development"],
                problem_name=_get_problem_name(problem_set, noisy=False),
                development_or_publication="development",
            )
            PLOT_CONFIG.update(_updated_configs)

    if OPTIONS.RUN_NOISY:

        if OPTIONS.RUN_PUBLICATION_CASES:
            _updated_configs = _add_problem_name_to_configs(
                _noisy_plots["publication"],
                problem_name=_get_problem_name(problem_set, noisy=True),
                development_or_publication="publication",
            )
            PLOT_CONFIG.update(_updated_configs)

        if OPTIONS.RUN_DEVELOPMENT_CASES:
            _updated_configs = _add_problem_name_to_configs(
                _noisy_plots["development"],
                problem_name=_get_problem_name(problem_set, noisy=True),
                development_or_publication="development",
            )
            PLOT_CONFIG.update(_updated_configs)


BENCHMARK_CASES = []
for info in PLOT_CONFIG.values():
    for scenario in info["scenarios"]:
        BENCHMARK_CASES.append((info["problem_name"], scenario))


COMPETITION_CASES = [case for case in BENCHMARK_CASES if "tranquilo" not in case[1]]

TRANQUILO_CASES = [case for case in BENCHMARK_CASES if "tranquilo" in case[1]]
