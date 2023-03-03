from copy import deepcopy

import estimagic as em
import pytask
from estimagic.optimization.tranquilo.options import HistorySearchOptions
from tranquilo_dev.config import BLD
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS


OUT = BLD / "benchmarks"

for functype in ["scalar"]:  # , "ls"]:

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
            "fitter": "tranquilo" if functype == "scalar" else None,
            "fit_options": {"residualize": True} if functype == "scalar" else None,
            # "subsolver": "slsqp_sphere",
            # "solver_options": {"experimental": "True"}
            "disable_convergence": False,
            "stopping.max_iterations": 2000 if functype == "scalar" else 500,
            "stopping.max_criterion_evaluations": 2000,
            # "noisy": True,
            # "n_evals_per_point": 3,
            "experimental": True,
            "history_search_options": HistorySearchOptions(
                radius_factor=4.25 if functype == "scalar" else 5,
            ),
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
