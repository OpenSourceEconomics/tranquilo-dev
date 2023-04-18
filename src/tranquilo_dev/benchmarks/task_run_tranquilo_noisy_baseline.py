from copy import deepcopy

import estimagic as em
import pytask
from tranquilo import tranquilo
from tranquilo import tranquilo_ls
from tranquilo.options import NoiseAdaptationOptions
from tranquilo_dev.benchmarks.compat_mode import filter_tranquilo_benchmark
from tranquilo_dev.config import BLD
from tranquilo_dev.config import COMPAT_MODE
from tranquilo_dev.config import N_CORES
from tranquilo_dev.config import PROBLEM_SETS
from tranquilo_dev.config import TRANQUILO_BASE_OPTIONS


OUT = BLD / "benchmarks"

for functype in ["scalar", "ls"]:

    if functype == "scalar":
        algorithm = tranquilo
        algorithm_name = "tranquilo"
    elif functype == "ls":
        algorithm = tranquilo_ls
        algorithm_name = "tranquilo_ls"
    else:
        raise ValueError(f"Unknown functype {functype}")

    scenario_name = f"{algorithm_name}_noisy_baseline"

    problem_name = "mw_noisy"
    problem_kwargs = PROBLEM_SETS[problem_name]

    optimize_options = deepcopy(TRANQUILO_BASE_OPTIONS)
    optimize_options["algorithm"] = algorithm
    optimize_options["algo_options"] = {
        **optimize_options["algo_options"],
        "disable_convergence": False,
        "stopping_max_iterations": 2000 if functype == "scalar" else 500,
        "stopping_max_criterion_evaluations": 4000,
    }
    if "noisy" in problem_name:
        noise_options = NoiseAdaptationOptions(
            min_n_evals=5,
            max_n_evals=5,
        )
        optimize_options["algo_options"].update(
            {
                "noisy": True,
                "n_evals_per_point": 5,
                "noise_adaptation_options": noise_options,
                "acceptance_decider": "naive_noisy",
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
            max_criterion_evaluations=4_000,
            disable_convergence=False,
        )

        if COMPAT_MODE:
            res = filter_tranquilo_benchmark(res)

        em.utilities.to_pickle(res, produces)
