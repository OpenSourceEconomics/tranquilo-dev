from copy import deepcopy

import estimagic as em
import pytask
from estimagic.optimization.tranquilo.options import HistorySearchOptions
from tranquilo_dev.config import BLD
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS


OUT = BLD / "benchmarks"

for functype in ["scalar", "ls"]:

    if functype == "scalar":
        algorithm = "tranquilo"
        radius_factor = 1.5
        sample_filter = "clustering"
    else:
        algorithm = "tranquilo_ls"
        radius_factor = 1.5
        sample_filter = "keep_all"

    search_options = HistorySearchOptions(radius_factor=radius_factor)

    scenario_name = f"{algorithm}_experimental"

    for problem_name, problem_kwargs in PROBLEM_SETS.items():
        optimize_options = deepcopy(TRANQUILO_BASE_OPTIONS)
        optimize_options["algorithm"] = algorithm

        optimize_options["algo_options"] = {
            **optimize_options["algo_options"],
            "sample_filter": sample_filter,
            "history_search_options": search_options,
        }

        problems = em.get_benchmark_problems(**problem_kwargs)

        name = f"{problem_name}_{scenario_name}"

        @pytask.mark.produces(OUT / f"{problem_name}_{scenario_name}.pkl")
        @pytask.mark.task(id=name)
        def task_run_tranquilo_default(
            produces,
            scenario_name=scenario_name,
            optimize_options=optimize_options,
            problems=problems,
        ):
            res = em.run_benchmark(
                problems=problems,
                optimize_options={scenario_name: optimize_options},
                n_cores=N_CORES,
            )

            em.utilities.to_pickle(res, produces)
