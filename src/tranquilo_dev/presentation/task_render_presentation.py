import subprocess

import pytask
from tranquilo_dev.config import BLD
from tranquilo_dev.config import PUBLIC
from tranquilo_dev.config import SRC


src_figures = [
    "tranquilo.jpg",
]

bld_figures = []

src_figures = [SRC / "presentation" / "figures" / f for f in src_figures]
bld_figures = [BLD / "presentation" / "figures" / f for f in bld_figures]

dependencies = {f.name: f for f in src_figures + bld_figures}

for output_format in ["pdf", "html"]:

    kwargs = {
        "depends_on": {
            **dependencies,
            **{
                "source": SRC.joinpath("presentation", "main.md").resolve(),
                "scss": SRC.joinpath("presentation", "custom.scss").resolve(),
            },
        },
        "produces": PUBLIC.joinpath(f"slides.{output_format}"),
    }

    @pytask.mark.task(id=f"slides-{output_format}", kwargs=kwargs)
    def task_render_presentation(depends_on, produces):

        commands = [
            "marp",  # executable
            "--html",  # allows html code in markdown files
            "--allow-local-files",
            "--theme-set",
            str(depends_on["scss"]),  # use custom scss file
            "--output",
            str(produces),  # output file
        ]

        commands += ["--", depends_on["source"]]

        subprocess.call(commands)
