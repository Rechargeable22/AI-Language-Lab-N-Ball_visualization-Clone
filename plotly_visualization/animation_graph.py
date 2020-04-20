import plotly.graph_objects as go
import numpy as np


def frame_args(duration):
    return {
        "frame": {"duration": duration + 300},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "quadratic-in-out"},
    }


def animation_graph_plot(list):
    print("list")
    print(list)
    frames = []
    step_names = []
    last_circles = None
    last_x = None
    last_y = None
    last_label = None

    for index, step in enumerate(list):
        step_names.append(index)
        last_circles, last_x, last_y, last_label = generate_frame(step, frames, index)

    fig = go.Figure(
        frames=frames,
        data=[go.Scatter(
                        x=last_x,
                         y=last_y,
                         text=last_label,
                         mode="text",
                         )],
        layout=go.Layout(
            shapes= [],
            autosize=True,
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
        ),
    )

    print(frames)
    for k, f in enumerate(fig.frames):
        print(f.name)
        print(str(k))

    sliders = [
        {
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[f.name], frame_args(500)],
                    "label": str(k),
                    "method": "animate",
                }
                for k, f in enumerate(fig.frames)
            ],
        }
    ]

    fig.update_layout(
        sliders=sliders,
        shapes=[],
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, frame_args(500)],
                        "label": "&#9654;",  # play symbol
                        "method": "animate",
                    },
                    {
                        "args": [[None], frame_args(0)],
                        "label": "&#9724;",  # pause symbol
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "type": "buttons",
                "x": 0.1,
                "y": 0,
            }
        ],
        autosize=True,
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
    fig.show(config={'scrollZoom': True})

    return fig


def generate_frame(step, frames, frame_name):
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

    frames.append(go.Frame(data=[go.Scatter(
        x=x,
        y=y,
        text=labels,
        mode="text",
    )],
        name=str(frame_name),
        layout=go.Layout(
            shapes=circles,
            # autosize=True,
        )
    ))

    return circles, x, y, labels
