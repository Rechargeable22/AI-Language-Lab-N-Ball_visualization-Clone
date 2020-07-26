import plotly.graph_objects as go
import numpy as np


def animation_graph_plot2(step, step_index):

    fig = go.Figure()
    fig.update_layout(
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showline=False,
        ),
        xaxis=dict(
            showline=False,
        ),
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        ),
    )

    for index, step in enumerate(list):
        if index is step_index:
            plot_step(step, fig)

    plot_step(step, fig)



    # fig.show(config={'scrollZoom': True})

    return fig


def plot_step(step, fig):
    fig.data = []

    fig.update_layout(shapes=[])
    x = []
    y = []
    labels = []

    circles = []
    for k, b in step.items():
        x.append(b.vector[0])
        y.append(b.vector[1] - b.radius - (b.radius * 0.05))
        labels.append(k)
        color = np.random.choice(range(256), size=3)
        circles.append(dict(
            type="circle",
            xref="x",
            yref="y",
            x0=b.vector[0] - b.radius,
            y0=b.vector[1] - b.radius,
            x1=b.vector[0] + b.radius,
            y1=b.vector[1] + b.radius,
            line_color="rgb(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")",
        ))

        print("x")
        print(x)
        print("y")
        print(y)
        print("circles")
        print(circles)

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            text=labels,
            mode="text",
        ))
        fig.update_layout(
            shapes=circles,
        )
