"""This module contains the general configuration of the project."""
from pathlib import Path


SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()
BLD = ROOT.joinpath("bld").resolve()
PUBLIC = BLD.joinpath("public").resolve()


N_CORES = 8

PROBLEM_SETS = {
    "mw_standard": {
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


PROFILE_PLOTS = {
    "mw_standard_tranquilo_vs_nag": {
        "problem_name": "mw_standard",
        "scenarios": ["nag_dfols", "nag_bobyqa", "tranquilo_default"],
        "y_precision": 1e-3,
        "normalize_runtime": True,
    },
}


TRANQUILO_BASE_OPTIONS = {
    "algorithm": "tranquilo",
    "algo_options": {
        "disable_convergence": True,
        "stopping.max_iteratios": 150,
        "silence_experimental_warning": True,
    },
}

__all__ = ["BLD", "PUBLIC", "SRC", "ROOT"]
