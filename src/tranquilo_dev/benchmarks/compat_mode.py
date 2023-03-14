from estimagic.optimization.optimize_result import OptimizeResult


def filter_tranquilo_benchmark(res):
    """Replace things that can lead to pickle errors."""
    for value in res.values():
        if isinstance(value["solution"], OptimizeResult):
            value["solution"].algorithm_output = {}

    return res
