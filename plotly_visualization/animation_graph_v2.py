import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time

import plotly_visualization.balls_to_json as util


def plot_balls(outfolder_path):
    ball = util.balls_to_object(f"{outfolder_path}/reduced_nballs_after.txt")

    df = pd.DataFrame([t.__dict__ for t in ball])
    df[['x', 'y']] = pd.DataFrame(df.vector.values.tolist(), index=df.index)
    df['x0'] = df.x - df.radius
    df['x1'] = df.x + df.radius
    df['y0'] = df.y - df.radius
    df['y1'] = df.y + df.radius

    final_df = df.sort_values(by=['radius'], ascending=False)
    print(final_df.to_string())

    circles = []
    for b in ball:
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

    return final_df, circles

def frame_args(duration):
    return {
            "frame": {"duration": duration + 300},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "quadratic-in-out"},
        }


def animation_graph_plot2():
    frames = []

    final_df, circles = plot_balls(f"out/14679")
    final_df2, circles2 = plot_balls(f"out/14850")
    final_df3, circles3 = plot_balls(f"out/17380")
    final_df4, circles4 = plot_balls(f"out/20116")

    fig = go.Figure(
        data=[go.Scatter(
                        x=final_df["x"],
                         y=final_df["y0"] - (final_df["radius"] * 0.05),
                         text=final_df["word"],
                         mode="text",
                         )],
        layout=go.Layout(
            shapes=circles,
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
        frames=frames,
    )

    fig.show()
    time.sleep(1000)
    generate_frame(circles, final_df, fig)
    time.sleep(1000)
    generate_frame(circles2, final_df2, fig)
    time.sleep(1000)
    generate_frame(circles3, final_df3, fig)
    time.sleep(1000)
    generate_frame(circles4, final_df4, fig)
    return "animation"


def generate_frame(circles, final_df, fig):
    fig.data = []
    fig.add_trace(go.Scatter(
        x=final_df["x"],
        y=final_df["y0"] - (final_df["radius"] * 0.05),
        text=final_df["word"],
        mode="text",
    ))

    fig.layout = {}

    fig.update_layout(
        shapes=circles,
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

def next_button(fig):
    fig.data = []
