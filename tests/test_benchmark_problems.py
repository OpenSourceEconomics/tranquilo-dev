from pybaum import tree_equal
from tranquilo_dev.benchmarks.benchmark_problems import get_extended_benchmark_problems


def test_deterministic_property():
    """Test that the same seed leads to the same newly drawn start values."""
    p1 = get_extended_benchmark_problems(
        n_draws=2, seed=12345, benchmark_kwargs={"name": "more_wild"}
    )

    p2 = get_extended_benchmark_problems(
        n_draws=2, seed=12345, benchmark_kwargs={"name": "more_wild"}
    )

    v1 = {k: v["inputs"]["params"] for k, v in p1.items()}
    v2 = {k: v["inputs"]["params"] for k, v in p2.items()}

    assert tree_equal(v1, v2)


def test_stochastic_property():
    """Test that different seeds lead to the different newly drawn start values."""
    p1 = get_extended_benchmark_problems(
        n_draws=2, seed=12345, benchmark_kwargs={"name": "more_wild"}
    )

    p2 = get_extended_benchmark_problems(
        n_draws=2, seed=54321, benchmark_kwargs={"name": "more_wild"}
    )

    v1 = {k: v["inputs"]["params"] for k, v in p1.items()}
    v2 = {k: v["inputs"]["params"] for k, v in p2.items()}

    assert not tree_equal(v1, v2)
