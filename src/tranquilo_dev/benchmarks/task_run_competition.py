import estimagic as em
import pandas as pd
import pytask
from tranquilo_dev.benchmarks.benchmark_problems import get_extended_benchmark_problems
from tranquilo_dev.config import BLD
from tranquilo_dev.config import COMPETITION
from tranquilo_dev.config import COMPETITION_CASES
from tranquilo_dev.config import get_benchmark_problem_info
from tranquilo_dev.config import get_max_criterion_evaluations
from tranquilo_dev.config import OPTIONS
from tranquilo_dev.config import PROBLEM_SETS


OUT = BLD / "benchmarks"

for problem_name, scenario_name in COMPETITION_CASES:
    noisy = "noisy" in problem_name
    benchmark_info = get_benchmark_problem_info(problem_name)
    problems = get_extended_benchmark_problems(
        benchmark_kwargs=PROBLEM_SETS[problem_name], **benchmark_info
    )
    optimize_options = COMPETITION[scenario_name]

    name = f"{problem_name}_{scenario_name}"

    max_evals = get_max_criterion_evaluations(noisy=noisy)

    @pytask.mark.produces(OUT / f"{name}.pkl")
    @pytask.mark.task(id=name)
    def task_run_competition(
        produces,
        scenario_name=scenario_name,
        optimize_options=optimize_options,
        problems=problems,
    ):
        res = em.run_benchmark(
            problems=problems,
            optimize_options={scenario_name: optimize_options},
            n_cores=OPTIONS.n_cores,
            max_criterion_evaluations=max_evals,  # noqa: B023
            disable_convergence=True,
        )

        pd.to_pickle(res, produces)
