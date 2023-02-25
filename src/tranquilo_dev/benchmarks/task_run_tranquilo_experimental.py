from copy import deepcopy

import estimagic as em
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS
from estimagic.optimization.tranquilo.options import StagnationOptions, HistorySearchOptions, RadiusOptions


OUT = BLD / "benchmarks"

for functype in ["scalar", "ls"]:

    if functype == "scalar":
        algorithm = "tranquilo"
    else:
        algorithm = "tranquilo_ls"

    scenario_name = f"{algorithm}_experimental"

    for problem_name, problem_kwargs in PROBLEM_SETS.items():
        optimize_options = deepcopy(TRANQUILO_BASE_OPTIONS)
        optimize_options["algorithm"] = algorithm

        optimize_options["algo_options"] = {
            **optimize_options["algo_options"],
            # "noisy": True,
            # "sample_size_factor": 3,
            # "surrogate_model": "diagonal" if functype == "scalar" else None,
            # "fitter": "tranquilo" if functype == "scalar" else "ols",
            "stagnation_options": StagnationOptions(
                drop=True,
                max_trials=5,
                min_relative_step=0.025,
            ),
            "sample_filter": "keep_inside",
            "history_search_options": HistorySearchOptions(
                radius_factor=2 if functype == "scalar" else 5,
                radius_type="inscribed",
            ),
            "experimental": True,
            "radius_options": RadiusOptions(
                min_radius=1e-8,
            )
        }

        problems = em.get_benchmark_problems(**problem_kwargs)

        name = f"{problem_name}_{scenario_name}"

        @pytask.mark.produces(OUT / f"{problem_name}_{scenario_name}.pkl")
        @pytask.mark.task(id=name)
        def task_run_tranquilo_experiental(
            produces,
            scenario_name=scenario_name,
            optimize_options=optimize_options,
            problems=problems,
        ):
            res = em.run_benchmark(
                problems=problems,
                optimize_options={scenario_name: optimize_options},
                n_cores=N_CORES,
                max_criterion_evaluations=3_000,
            )

            em.utilities.to_pickle(res, produces)
