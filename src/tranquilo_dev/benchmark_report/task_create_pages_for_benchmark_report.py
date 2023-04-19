import pytask
import snakemd
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SPHINX_PAGES_BLD
from tranquilo_dev.config import SPHINX_STATIC_BLD


for name, _ in PLOT_CONFIG.items():
    plot_type = "profile"

    @pytask.mark.depends_on(
        SPHINX_STATIC_BLD / "figures" / f"{plot_type}_plots" / f"{name}.svg"
    )
    @pytask.mark.produces(SPHINX_PAGES_BLD / f"{name}.md")
    @pytask.mark.task(id=f"plot_{name}")
    def task_create_profile_plots_markdown(name=name):
        doc = snakemd.new_doc()

        doc.add_heading(f"{name}")
        doc.add_paragraph(
            f"""
            Profile plot for {name}.
            """
        )

        doc.add_paragraph(
            f"""
            ![{name}](../_static/bld/figures/profile_plots/{name}.svg)
            """
        )

        doc.dump(SPHINX_PAGES_BLD / name)
