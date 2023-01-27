import estimagic as em
import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS


scenario_name = "tranquilo_default"
optimize_options = TRANQUILO_BASE_OPTIONS
OUT = BLD / "benchmarks"

for problem_name, problem_kwargs in PROBLEM_SETS.items():
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
