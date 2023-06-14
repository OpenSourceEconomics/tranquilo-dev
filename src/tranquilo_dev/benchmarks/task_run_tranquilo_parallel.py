from copy import deepcopy

import estimagic as em
import pytask
from tranquilo import tranquilo
from tranquilo import tranquilo_ls
from tranquilo_dev.benchmarks.compat_mode import filter_tranquilo_benchmark
from tranquilo_dev.config import BLD
from tranquilo_dev.config import COMPAT_MODE
from tranquilo_dev.config import get_max_criterion_evaluations
from tranquilo_dev.config import get_max_iterations
from tranquilo_dev.config import get_tranquilo_version
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS
from tranquilo_dev.config import TRANQUILO_CASES


ALGORITHMS = {
    "tranquilo": tranquilo,
    "tranquilo_ls": tranquilo_ls,
}


OUT = BLD / "benchmarks"

for batch_size in [2, 4, 8]:

    for functype in ["scalar", "ls"]:

        for problem_name, problem_kwargs in PROBLEM_SETS.items():
            algorithm_name = get_tranquilo_version(functype)
            algorithm = ALGORITHMS[algorithm_name]
            scenario_name = f"{algorithm_name}_parallel_{batch_size}"
            max_iterations = get_max_iterations(noisy=False, functype=functype)
            max_evals = get_max_criterion_evaluations(noisy=False)

            if (problem_name, scenario_name) in TRANQUILO_CASES:

                optimize_options = deepcopy(TRANQUILO_BASE_OPTIONS)
                optimize_options["algorithm"] = algorithm
                optimize_options["algo_options"] = {
                    **optimize_options["algo_options"],
                    "stopping_max_iterations": max_iterations,
                    "stopping_max_criterion_evaluations": max_evals,
                    "acceptance_decider": "classic_line_search",
                    "batch_size": batch_size,
                }

                problems = em.get_benchmark_problems(**problem_kwargs)

                name = f"{problem_name}_{scenario_name}"

                @pytask.mark.produces(OUT / f"{problem_name}_{scenario_name}.pkl")
                @pytask.mark.task(id=name)
                def task_run_tranquilo_parallel(
                    produces,
                    scenario_name=scenario_name,
                    optimize_options=optimize_options,
                    problems=problems,
                ):
                    res = em.run_benchmark(
                        problems=problems,
                        optimize_options={scenario_name: optimize_options},
                        n_cores=N_CORES,
                        max_criterion_evaluations=max_evals,  # noqa: B023
                        disable_convergence=False,
                    )

                    if COMPAT_MODE:
                        res = filter_tranquilo_benchmark(res)

                    em.utilities.to_pickle(res, produces)
