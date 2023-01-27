import pytask
from distutils.spawn import find_executable


def is_installed(executable):
    """Check that executable is available to PATH."""
    return bool(find_executable(executable))


for executable in ["marp"]:

    @pytask.mark.task
    def task_test_executable_is_installed(executable=executable):
        if not is_installed(executable=executable):
            raise ValueError(f"{executable} is not installed.")
