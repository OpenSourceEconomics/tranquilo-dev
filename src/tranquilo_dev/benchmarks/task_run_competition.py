import estimagic as em
import pandas as pd
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import COMPETITION
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS


OUT = BLD / "benchmarks"

for problem_name, problem_kwargs in PROBLEM_SETS.items():
    problems = em.get_benchmark_problems(**problem_kwargs)

    for scenario_name, optimize_options in COMPETITION.items():
        name = f"{problem_name}_{scenario_name}"

        MAX_EVALS = 20_000 if "noisy" in problem_name else 2_000

        @pytask.mark.produces(OUT / f"{problem_name}_{scenario_name}.pkl")
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
                n_cores=N_CORES,
                max_criterion_evaluations=MAX_EVALS,  # noqa: B023
                disable_convergence=True,
            )

            pd.to_pickle(res, produces)
