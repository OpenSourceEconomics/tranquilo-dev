from collections import ChainMap

import estimagic as em
import numpy as np
from pybaum import tree_update
from tranquilo_dev.config import BENCHMARK_PROBLEMS_INFO
from tranquilo_dev.config import PROBLEM_SETS


def get_benchmark_problems(problem_name):
    problem_kwargs = PROBLEM_SETS[problem_name]
    problems = em.get_benchmark_problems(**problem_kwargs)

    if BENCHMARK_PROBLEMS_INFO["n_draws"] > 0:

        new_problems = _draw_new_problems(
            problems=problems,
            n_draws=BENCHMARK_PROBLEMS_INFO["n_draws"],
            seed=BENCHMARK_PROBLEMS_INFO["seed"],
        )

    else:
        new_problems = {}

    return {**problems, **new_problems}


def _draw_new_problems(
    problems: dict,
    n_draws: int,
    seed: int,
) -> dict:
    rng = np.random.default_rng(seed)

    list_of_new_problems = []

    for problem_name, problem in problems.items():

        _new_problems = _generate_new_problems(
            problem_name=problem_name,
            problem=problem,
            n_draws=n_draws,
            rng=rng,
        )

        list_of_new_problems.append(_new_problems)

    # Merge list of dictionaries into one dictionary and return
    return dict(ChainMap(*list_of_new_problems))


def _generate_new_problems(
    problem_name: str, problem: dict, n_draws: int, rng: np.random.Generator
) -> dict:
    new_start_vectors = _generate_new_start_vectors(
        problem=problem,
        n_draws=n_draws,
        rng=rng,
    )

    new_problems = {}
    for k, new_start_vector in enumerate(new_start_vectors):
        new_problem = _update_start_vector_in_problem(problem, new_start_vector)
        new_name = f"{problem_name}__draw_{k}"
        new_problems[new_name] = new_problem

    return new_problems


def _update_start_vector_in_problem(
    problem: dict, new_start_vector: np.ndarray
) -> dict:
    update_dict = {"inputs": {"params": new_start_vector}}
    return tree_update(problem, update_dict)


def _generate_new_start_vectors(
    problem: dict,
    n_draws: int,
    rng: np.random.Generator,
) -> np.ndarray:
    x = problem["inputs"]["params"]

    radius = _calculate_radius(x)
    lower = x - radius
    upper = x + radius

    return rng.uniform(low=lower, high=upper, size=(n_draws, len(x)))


def _calculate_radius(
    x: np.ndarray, percentage_deviation: float = 0.1, minimal_radius: float = 0.1
) -> np.ndarray:
    candidate = percentage_deviation * np.abs(x)
    return np.clip(candidate, a_min=minimal_radius, a_max=None)
