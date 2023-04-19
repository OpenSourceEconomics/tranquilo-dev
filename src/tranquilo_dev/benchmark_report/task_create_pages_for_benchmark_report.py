import pytask
import snakemd
from tranquilo_dev.config import PLOT_CONFIG
from tranquilo_dev.config import SPHINX_PAGES_BLD
from tranquilo_dev.config import SPHINX_STATIC_BLD


for name, _ in PLOT_CONFIG.items():

    DEPS = {}
    for plot_type in ["profile", "deviation"]:
        DEPS[plot_type] = (
            SPHINX_STATIC_BLD / "figures" / f"{plot_type}_plots" / f"{name}.svg"
        )

    @pytask.mark.depends_on(DEPS)
    @pytask.mark.produces(SPHINX_PAGES_BLD / f"{name}.md")
    @pytask.mark.task(id=f"{name}")
    def task_create_benchmark_reports(name=name):
        doc = snakemd.new_doc()

        doc.add_heading(f"{name}")

        for plot_type in ["profile", "deviation"]:
            doc.add_paragraph(
                f"""
                ## {plot_type.capitalize()} Plot
                """
            )
            doc.add_paragraph(
                f"""
                ![{plot_type}](../_static/bld/figures/{plot_type}_plots/{name}.svg)
                """
            )

        doc.dump(SPHINX_PAGES_BLD / name)
