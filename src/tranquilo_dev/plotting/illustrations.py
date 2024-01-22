from copy import deepcopy

import estimagic as em
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tranquilo.visualize import _clean_legend_duplicates
from tranquilo.visualize import _get_sample_points


def create_noise_plots():

    HEIGHT = 500
    WIDTH = 600

    out = []

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
    fig.update_layout(
        height=HEIGHT, width=WIDTH, template="plotly_white", showlegend=True
    )
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
    out.append(fig)  # fig.write_image("noise_plot_0.svg")

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
    out.append(fig1)  # fig1.write_image("noise_plot_1.svg")

    plotting_data = []
    for _, trustregion in enumerate([(-1.75, -0.5), (-0.75, 0.5)]):
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
        fig2.update_layout(width=WIDTH)

        plotting_data.append(fig2.data)
        out.append(fig2)  # fig2.write_image(f'noise_plot_{i+2}.svg')

    len(plotting_data)
    fig3 = make_subplots(cols=2, rows=1)
    for i in [1, 2]:
        fig3.add_traces(plotting_data[i - 1], cols=i, rows=1)
    fig3 = _clean_legend_duplicates(fig3)
    fig3.update_layout(
        legend={"yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5}
    )
    fig3.update_layout(height=HEIGHT, width=1.8 * WIDTH, template="plotly_white")
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
    out.append(fig3)

    # Remove axis titles for all plots
    out = [fig.update_layout(yaxis_title="", xaxis_title="") for fig in out]
    # Remove legend
    out = [fig.update_layout(showlegend=False) for fig in out]
    return out


def create_other_illustration_plots():
    out = {}

    def sphere(x):
        return {"root_contributions": x}

    res = em.minimize(
        sphere,
        params=np.array([1, 1]),
        algorithm="tranquilo_ls",
    )
    params_history = np.array(res.history["params"])
    states = res.algorithm_output["states"]
    color_dict = {
        "existing": "rgb(0,0,255)",
        "new": "rgb(230,0,0)",
        "discarded": "rgb(148, 148, 148)",
    }

    for k in range(6):
        out[f"animation_{k}.svg"] = _plot_sample_points(
            params_history, states, k, color_dict
        )

    base_fig = _plot_sample_points(params_history, states, 1, color_dict)
    fig = deepcopy(base_fig)
    center = np.array([fig.data[0].x[0], fig.data[0].y[0]])
    candidate = np.array([fig.data[-1].x[0], fig.data[-1].y[0]])
    direction = candidate - center
    line_points = []
    for i in [2, 4, 8]:
        line_points.append(center + i * direction)
    line_points = np.array(line_points)
    fig.data[1].marker.color = fig.data[0].marker.color
    fig.data[1].showlegend = False
    fig.add_trace(
        go.Scatter(
            x=line_points[:, 0],
            y=line_points[:, 1],
            mode="markers",
            marker_color="#805B87",
            marker_size=9,
            name="line search",
        )
    )
    fig.update_xaxes(range=[0, 1.2])
    fig.update_yaxes(range=[0, 1.2])
    out["line_points_3.svg"] = deepcopy(fig)  # fig.write_image("line_points_3.svg")

    fig.data[3].x = fig.data[3].x[:-1]
    fig.data[3].y = fig.data[3].y[:-1]
    out["line_points_2.svg"] = deepcopy(fig)  # fig.write_image("line_points_2.svg")

    fig.data[3].x = fig.data[3].x[:-1]
    fig.data[3].y = fig.data[3].y[:-1]
    out["line_points_1.svg"] = deepcopy(fig)  # fig.write_image("line_points_1.svg")

    fig.data = fig.data[:-1]
    out["origin_plot.svg"] = deepcopy(fig)  # fig.write_image("origin_plot.svg")

    center = candidate
    radius = states[1].trustregion.radius
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=center[0] - radius,
        y0=center[1] - radius,
        x1=center[0] + radius,
        y1=center[1] + radius,
        line_width=0.5,
        line_color="black",
        line_dash="dash",
    )
    out["empty_speculative_trustregion_small_scale.svg"] = deepcopy(fig)

    fig.update_yaxes(range=[0.5, 1.2])
    fig.update_xaxes(range=[0.5, 1.2])
    out["empty_speculative_trustregion_large_scale.svg"] = deepcopy(fig)

    fig.update_yaxes(range=[0, 1.2])
    fig.update_xaxes(range=[0, 1.2])

    angle1 = 30
    angle2 = 55
    speculative1 = np.zeros((2, 2))
    speculative1[0, 0] = candidate[0] - np.cos(angle1 * np.pi / 180) * radius
    speculative1[0, 1] = candidate[1] - np.sin(angle1 * np.pi / 180) * radius
    speculative1[1, 0] = candidate[0] + np.sin(angle2 * np.pi / 180) * radius
    speculative1[1, 1] = candidate[1] - np.cos(angle2 * np.pi / 180) * radius
    fig.data = fig.data[:3]
    fig.add_trace(
        go.Scatter(
            x=speculative1[:, 0],
            y=speculative1[:, 1],
            mode="markers",
            marker_color="#F98900",
            marker_size=9,
            name="speculative",
        )
    )
    out["sampled_speculative_trustregion_small_scale.svg"] = deepcopy(fig)

    fig.update_yaxes(range=[0.5, 1.2])
    fig.update_xaxes(range=[0.5, 1.2])
    out["sampled_speculative_trustregion_large_scale.svg"] = deepcopy(fig)

    fig.update_yaxes(range=[0, 1.2])
    fig.update_xaxes(range=[0, 1.2])
    angle1 = 15
    angle2 = 78
    speculative1[0, 0] = candidate[0] + np.sin(angle1 * np.pi / 180) * radius
    speculative1[0, 1] = candidate[1] - np.cos(angle1 * np.pi / 180) * radius
    speculative1[1, 0] = candidate[0] + np.sin(angle2 * np.pi / 180) * radius
    speculative1[1, 1] = candidate[1] - np.cos(angle2 * np.pi / 180) * radius

    fig.data = fig.data[:3]
    fig.add_trace(
        go.Scatter(
            x=speculative1[:, 0],
            y=speculative1[:, 1],
            mode="markers",
            marker_color="#F98900",
            marker_size=9,
            name="speculative",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=line_points[:, 0],
            y=line_points[:, 1],
            mode="markers",
            marker_color="#805B87",
            marker_size=9,
            name="line search",
        )
    )

    out["line_and_speculative_points.svg"] = deepcopy(fig)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(scaleanchor="y", scaleratio=1)

    fig.update_layout(height=700, width=800, template="plotly_white")
    out["checklayout.svg"] = deepcopy(fig)

    return out


# ======================================================================================
# Shared functions
# ======================================================================================


def _plot_sample_points(history, states, iteration, color_dict):

    state = states[iteration]
    sample_points = _get_sample_points(state, history)
    trustregion = state.trustregion
    radius = trustregion.radius
    center = trustregion.center
    fig = go.Figure()
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=center[0] - radius,
        y0=center[1] - radius,
        x1=center[0] + radius,
        y1=center[1] + radius,
        line_width=0.5,
        line_color="grey",
    )

    fig.add_traces(
        px.scatter(
            sample_points,
            x=0,
            y=1,
            color="case",
            color_discrete_map=color_dict,
            opacity=0.7,
        ).data,
    )
    if iteration >= 1:
        fig.add_trace(
            go.Scatter(
                x=[state.candidate_x[0]],
                y=[state.candidate_x[1]],
                mode="markers",
                marker_symbol="star",
                marker_color="#228b22",
                name="candidate",
            ),
        )
    fig.update_traces(
        marker_size=9,
    )

    fig = _clean_legend_duplicates(fig)
    fig.update_layout(height=700, width=800, template="plotly_white")
    fig.update_yaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
        range=[-1.6, 1.6],
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor="black",
        zeroline=False,
        range=[-1.6, 1.6],
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.update_xaxes(scaleanchor="y", scaleratio=1)

    layout = go.Layout(
        margin=go.layout.Margin(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=10,  # top margin
        )
    )
    fig = fig.update_layout(layout)
    return fig
