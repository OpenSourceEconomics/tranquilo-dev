import shutil

import pytask
from pytask_latex import compilation_steps as cs
from tranquilo_dev.config import BLD
from tranquilo_dev.config import ROOT

COMPILATION_OPTIONS = (
    "--pdf",
    "--interaction=nonstopmode",
    "--synctex=1",
    "--cd",
    "--quiet",
    "--shell-escape",
    "-f",
)


@pytask.mark.task
@pytask.mark.latex(
    script="tranquilo.tex",
    document=BLD.joinpath("aux_paper", "tranquilo.pdf"),
    compilation_steps=cs.latexmk(
        options=COMPILATION_OPTIONS,
    ),
)
def task_compile_paper():
    pass


@pytask.mark.depends_on(BLD.joinpath("aux_paper", "tranquilo.pdf"))
@pytask.mark.produces(ROOT / "tranquilo.pdf")
@pytask.mark.task
def task_copy_paper(depends_on, produces):
    shutil.copyfile(depends_on, produces)
