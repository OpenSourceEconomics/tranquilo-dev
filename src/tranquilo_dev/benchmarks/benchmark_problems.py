from collections import ChainMap

import estimagic as em
import numpy as np
from pybaum import tree_update


DEFAULT_SAMPLE_KWARGS = {
    "minimal_radius": 0.1,
    "percentage_deviation_radius": 0.01,
}


def get_extended_benchmark_problems(
    n_draws=0, seed=None, benchmark_kwargs=None, sample_kwargs=None
):
    # Process kwargs that are passed to em.get_benchmark_problems and get base problems
    benchmark_kwargs = {} if benchmark_kwargs is None else benchmark_kwargs
    problems = em.get_benchmark_problems(**benchmark_kwargs)

    # Process kwargs that are used to for the random sampling
    if isinstance(sample_kwargs, dict):
        sample_kwargs = tree_update(DEFAULT_SAMPLE_KWARGS, sample_kwargs)
    else:
        sample_kwargs = DEFAULT_SAMPLE_KWARGS

    # Sample new problems
    if n_draws > 0:
        new_problems = _sample_new_problems(
            problems=problems,
            n_draws=n_draws,
            seed=seed,
            sample_kwargs=sample_kwargs,
        )
    else:
        new_problems = {}

    return {**problems, **new_problems}


def _sample_new_problems(
    problems: dict,
    n_draws: int,
    seed: int,
    sample_kwargs: dict[str, float],
) -> dict:
    rng = np.random.default_rng(seed)

    list_of_new_problems = []

    for problem_name, problem in problems.items():

        _new_problems = _generate_new_problems(
            problem_name=problem_name,
            problem=problem,
            n_draws=n_draws,
            sample_kwargs=sample_kwargs,
            rng=rng,
        )

        list_of_new_problems.append(_new_problems)

    # Merge list of dictionaries into one dictionary and return
    return dict(ChainMap(*list_of_new_problems))


def _generate_new_problems(
    problem_name: str,
    problem: dict,
    n_draws: int,
    sample_kwargs: dict[str, float],
    rng: np.random.Generator,
) -> dict:
    new_start_vectors = _draw_new_start_vectors(
        problem_name=problem_name,
        problem=problem,
        n_draws=n_draws,
        rng=rng,
        **sample_kwargs,
    )

    new_problems = {}
    for k, new_start_vector in enumerate(new_start_vectors):
        new_problem = _update_start_vector_in_problem(problem, new_start_vector)
        new_name = f"{problem_name}__draw_{k}"
        new_problems[new_name] = new_problem

    return new_problems


def _draw_new_start_vectors(
    problem_name: str,
    problem: dict,
    n_draws: int,
    rng: np.random.Generator,
    minimal_radius: float,
    percentage_deviation_radius: float,
) -> list[np.ndarray]:
    new_start_vectors = []

    for _ in range(n_draws):

        new_start_vector = _draw_single_new_start_vector(
            problem_name=problem_name,
            problem=problem,
            rng=rng,
            percentage_deviation_radius=percentage_deviation_radius,
            minimal_radius=minimal_radius,
        )
        new_start_vectors.append(new_start_vector)

    return new_start_vectors


def _draw_single_new_start_vector(
    problem_name: str,
    problem: dict,
    rng: np.random.Generator,
    percentage_deviation_radius: float,
    minimal_radius: float,
) -> np.ndarray:
    """Draw a new start vector for a given problem.

    Args:
        problem_name (str): The name of the problem.
        problem (dict): The problem dictionary.
        rng (np.random.Generator): A random number generator
        percentage_deviation_radius (float): The percentage deviation from x.
        minimal_radius (float): The minimal radius in each direction.

    Returns:
        np.ndarray: The new start vector.

    """
    x = problem["inputs"]["params"]
    criterion = problem["inputs"]["criterion"]

    radius = _calculate_radius(
        x,
        percentage_deviation=percentage_deviation_radius,
        minimal_radius=minimal_radius,
    )

    success = False

    for _ in range(100):
        candidate = rng.uniform(low=x - radius, high=x + radius)

        # Verify that the criterion function is well-defined at the candidate x-value,
        # and otherwise reduce the radius by half.
        try:
            _value = criterion(candidate)
            value = _value["value"] if isinstance(_value, dict) else _value
            assert np.isfinite(value)
        except Exception:
            radius /= 2
        else:
            success = True
            break

    if not success:
        raise RuntimeError(
            f"Could not find a valid new starting vector for {problem_name}."
        )

    return candidate


def _calculate_radius(
    x: np.ndarray,
    percentage_deviation: float,
    minimal_radius: float,
) -> np.ndarray:
    """Calculate the radius of a box around x.

    Args:
        x (np.ndarray): The center of the box.
        percentage_deviation (float): The percentage deviation from x. If x1 is 10 and
            percentage_deviation is 0.1, then the radius is 1 in the first direction.
        minimal_radius (float): The minimal radius in each direction.

    Returns:
        np.ndarray: The radius of the box.

    """
    candidate = percentage_deviation * np.abs(x)
    return np.clip(candidate, a_min=minimal_radius, a_max=None)


def _update_start_vector_in_problem(
    problem: dict, new_start_vector: np.ndarray
) -> dict:
    update_dict = {"inputs": {"params": new_start_vector}}
    return tree_update(problem, update_dict)
