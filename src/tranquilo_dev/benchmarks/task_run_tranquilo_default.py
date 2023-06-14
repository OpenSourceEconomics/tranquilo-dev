from copy import deepcopy
from functools import partial

import estimagic as em
import pytask
from estimagic.decorators import mark_minimizer
from tranquilo.tranquilo import _tranquilo
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


tranquilo = mark_minimizer(
    func=partial(_tranquilo, functype="scalar"),
    name="tranquilo",
    primary_criterion_entry="value",
    needs_scaling=True,
    is_available=True,
    is_global=False,
)


tranquilo_ls = mark_minimizer(
    func=partial(_tranquilo, functype="least_squares"),
    primary_criterion_entry="root_contributions",
    name="tranquilo_ls",
    needs_scaling=True,
    is_available=True,
    is_global=False,
)

ALGORITHMS = {
    "tranquilo": tranquilo,
    "tranquilo_ls": tranquilo_ls,
}


OUT = BLD / "benchmarks"

for functype in ["scalar", "ls"]:
    for problem_name, problem_kwargs in PROBLEM_SETS.items():
        algorithm_name = get_tranquilo_version(functype)
        algorithm = ALGORITHMS[algorithm_name]
        scenario_name = f"{algorithm_name}_default"
        noisy = "noisy" in problem_name
        max_iterations = get_max_iterations(noisy=noisy, functype=functype)
        max_evals = get_max_criterion_evaluations(noisy=noisy)

        if (problem_name, scenario_name) in TRANQUILO_CASES:

            optimize_options = deepcopy(TRANQUILO_BASE_OPTIONS)
            optimize_options["algorithm"] = algorithm
            optimize_options["algo_options"] = {
                **optimize_options["algo_options"],
                "stopping_max_iterations": max_iterations,
                "stopping_max_criterion_evaluations": max_evals,
            }
            if noisy:
                optimize_options["algo_options"].update(
                    {
                        "noisy": True,
                    }
                )

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
                    max_criterion_evaluations=max_evals,  # noqa: B023
                    disable_convergence=False,
                )

                if COMPAT_MODE:
                    res = filter_tranquilo_benchmark(res)

                em.utilities.to_pickle(res, produces)
