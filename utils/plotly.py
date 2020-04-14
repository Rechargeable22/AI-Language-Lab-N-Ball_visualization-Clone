import pandas as pd
import plotly.graph_objects as go
import numpy as np

import utils.balls_to_json as util
import json
import plotly

from utils.combined_paths_tree import combined_tree_paths_fig
from utils.single_path_tree import tree_path_fig

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
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=final_df["x"],
        y=final_df["y0"] - (final_df["radius"] * 0.05),
        text=final_df["word"],
        mode="text",
        # size=final_df["radius"]
        # textfont_size=final_df["radius"].astype(float),
    ))

    # fig = go.Figure(data=[go.Scatter(
    #     x=final_df["x"],
    #     y=final_df["y0"] - (final_df["radius"] * 0.05),
    #     mode='markers + text',
    #     marker_size=final_df["radius"]
    # )])

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
    # Set figure size
    # fig.update_layout(width=800, height=800)
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig.show(config={'scrollZoom': True})

    return serialized

def plot_tree_path(input_key):
    fig = tree_path_fig(input_key, "out/test1/small.wordSensePath.txt")
    fig.show()
    return ""


def tree_path_json(input_key, path):
    fig = tree_path_fig(input_key, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized

def plot_combined_tree_path(input_list):
    fig = combined_tree_paths_fig(input_list, "out/test1/small.wordSensePath.txt")
    fig.show()
    return ""

def plot_combined_tree_json(input_list, path):
    # change input list from paths to old format
    print(input_list)
    input_list = [element.split()[0] for element in input_list][1:]
    print(input_list)

    fig = combined_tree_paths_fig(input_list, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized