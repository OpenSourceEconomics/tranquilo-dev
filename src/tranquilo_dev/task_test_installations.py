import pytask
from tranquilo_dev.auxiliary import is_installed


for executable in ["marp"]:

    @pytask.mark.task
    def task_test_executable_is_installed(executable=executable):
        if not is_installed(executable=executable):
            raise ValueError(f"{executable} is not installed.")
