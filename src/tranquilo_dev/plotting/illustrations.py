from copy import deepcopy

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tranquilo.visualize import _clean_legend_duplicates


def create_noise_plots():
    out = {}

    def func(x):
        return x**4 + x**2 - x

    def model(x, beta):
        return beta[0] + beta[1] * x + beta[2] * x**2

    x_grid = np.linspace(-2, 1.5, 100)
    y = func(x_grid)
    rng = np.random.default_rng(4567)
    noise_x_grid = np.linspace(-2, 1.5, 40)
    noise_y = rng.normal(loc=func(noise_x_grid), scale=1.5)
    fig = px.line(x=x_grid, y=y)
    fig.data[0].name = "criterion function"
    fig.data[0].showlegend = True
    layout = go.Layout(
        margin=go.layout.Margin(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=10,  # top margin
        )
    )
    fig.update_layout(layout)
    fig.update_layout(height=500, width=600, template="plotly_white", showlegend=True)
    fig.update_yaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
    )
    fig.update_layout(
        legend={
            "yanchor": "bottom",
            "y": -0.2,
            "xanchor": "center",
            "x": 0.5,
            "orientation": "h",
        }
    )
    out[0] = fig  # fig.write_image("noise_plot_0.svg")

    fig1 = deepcopy(fig)

    fig1.add_trace(
        go.Scatter(
            x=noise_x_grid,
            y=noise_y,
            mode="markers",
            marker_color="rgb(0,0,255)",
            opacity=0.3,
            showlegend=False,
        )
    )
    out[1] = fig1  # fig1.write_image("noise_plot_1.svg")

    plotting_data = []
    for i, trustregion in enumerate([(-1.75, -0.5), (-0.75, 0.5)]):
        in_region = (trustregion[0] <= noise_x_grid) & (noise_x_grid <= trustregion[1])
        xs = noise_x_grid.copy()
        ys = noise_y.copy()
        xs[in_region] = np.nan
        ys[in_region] = np.nan
        sample_xs = np.array([trustregion[0], np.mean(trustregion), trustregion[1]])
        sample_ys = func(sample_xs) + np.array([-3, 0.75, 1.5])
        model_xs = np.column_stack(
            [
                np.ones(3),
                sample_xs,
                sample_xs**2,
            ]
        )
        beta, *_ = np.linalg.lstsq(model_xs, sample_ys, rcond=None)
        model_grid = np.linspace(trustregion[0], trustregion[1], 15)
        model_ys = np.array([model(x, beta) for x in model_grid])
        fig2 = deepcopy(fig)
        fig2.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                marker_color="rgb(0,0,255)",
                showlegend=False,
                opacity=0.3,
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=sample_xs,
                y=sample_ys,
                mode="markers",
                marker_color="rgb(0,0,255)",
                showlegend=False,
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=model_grid,
                y=model_ys,
                mode="lines",
                name="model",
                line_color="#F98900",
            )
        )
        for x in trustregion:
            fig2.add_vline(x=x, line_color="grey", line_width=1)
        fig2.update_layout(width=600)

        plotting_data.append(fig2.data)
        out[2 + i] = fig2  # fig2.write_image(f'noise_plot_{i+2}.svg')

    len(plotting_data)
    fig3 = make_subplots(cols=2, rows=1)
    for i in [1, 2]:
        fig3.add_traces(plotting_data[i - 1], cols=i, rows=1)
    fig3 = _clean_legend_duplicates(fig3)
    fig3.update_layout(
        legend={"yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5}
    )
    fig3.update_layout(height=700, width=800, template="plotly_white")
    fig3.update_yaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
    )
    fig3.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
    )
    out[4] = fig3
    return out
