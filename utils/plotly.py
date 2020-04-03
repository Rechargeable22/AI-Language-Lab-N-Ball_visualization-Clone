import pandas as pd
import plotly.graph_objects as go
import numpy as np

import utils.balls_to_json as util
import json
import plotly

from utils.files_utils import read_word_path
from plotly.validators.scatter.marker import SymbolValidator


def plot_balls(outfolder_path):
    ball = util.balls_to_object(f"{outfolder_path}/reduced_nballs_after.txt")

    fig = go.Figure()

    df = pd.DataFrame([t.__dict__ for t in ball])
    df[['x', 'y']] = pd.DataFrame(df.vector.values.tolist(), index=df.index)
    df['x0'] = df.x - df.radius
    df['x1'] = df.x + df.radius
    df['y0'] = df.y - df.radius
    df['y1'] = df.y + df.radius

    final_df = df.sort_values(by=['radius'], ascending=False)

    fig.add_trace(go.Scatter(
        x=final_df["x"],
        y=final_df["y0"] - (final_df["radius"] * 0.05),
        text=final_df["word"],
        mode="text",
    ))

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

    # Add circles
    fig.update_layout(
        shapes=circles,
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
        xaxis_showgrid=False,
        yaxis_showgrid=False,

    )

    # Set figure size
    # fig.update_layout(width=800, height=800)
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig.show(config={'scrollZoom': True})

    return serialized


def plot_tree_path(input_key):
    paths = read_word_path("out/test1/small.wordSensePath.txt")
    if "*root*" in paths:
        del paths["*root*"]
    data = paths.get(input_key, "")

    proc_data = []
    for i in data:
        if (i != '*root*'):
            proc_data.append(i)

    x_axis = []
    y_axis = []
    symbols = []
    colors = []

    for i in proc_data:
        index = proc_data.index(i)
        y_axis.append((int(index / 3) * -1))
        if int(index / 3) % 2 == 0:
            x_axis.append((int(index % 3)))
            if index == len(proc_data) - 1:
                symbols.append('x')
                colors.append('crimson')
            elif index == 0:
                symbols.append('diamond')
                colors.append('darkslategrey')
            else:
                symbols.append('triangle-right')
                colors.append('steelblue')
        if int(index / 3) % 2 == 1:
            x_axis.append((2 - int(index % 3)))
            if index == len(proc_data) - 1:
                symbols.append('x')
                colors.append('indianred')
            else:
                symbols.append('triangle-left')
                colors.append('steelblue')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_axis,
        y=y_axis,
        mode="lines+markers+text",
        name="Word Path",
        text=proc_data,
        textposition="top center",
        hoverinfo='none',
        marker_symbol=symbols,
        marker_line_color=colors,
        marker_color="lightsteelblue",
        marker_line_width=3,
        marker_size=30,
        textfont_size=16,
        textfont_family='Courier New, monospace',
    ))

    fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    fig.show()

    return 'tree'
