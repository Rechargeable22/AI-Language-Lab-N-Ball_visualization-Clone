import pandas as pd
import plotly.graph_objects as go
import numpy as np

import utils.balls_to_json as util
import json
import plotly

from utils.files_utils import read_word_path


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
    print(final_df.to_string())

    fig.add_trace(go.Scatter(
        x=final_df["x"],
        y=final_df["y0"] - (final_df["radius"] * 0.05),
        text=final_df["word"],
        # mode="text",
        # textfont_size=final_df["radius"].astype(float),
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


def tree_path_fig(input_key, file_path):
    paths = read_word_path(file_path)
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
    nodes_no = 5

    calculate_node_position(colors, nodes_no, proc_data, symbols, x_axis, y_axis)

    print(y_axis)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_axis,
        y=y_axis,
        mode="markers+text",
        name="Word Path",
        text=proc_data,
        textposition="top center",
        hoverinfo='none',
        marker_symbol=symbols,
        marker_line_color=colors,
        line_color='steelblue',
        marker_color=colors,
        marker_line_width=3,
        marker_size=15,
        textfont_size=12,
        textfont_family='Roboto, sans-serif',
    ))
    arrow_spacing = 0.1
    arrows = []
    for i in range(len(proc_data) - 1):
        if (i + 1) % nodes_no == 0 and i != 0:
            arrow_generation(0, 0.02, arrow_spacing + 0.1, arrows, i, i + 1, x_axis, y_axis)
        elif int(i / nodes_no) % 2 == 0:
            arrow_generation(arrow_spacing, 0, 0, arrows, i, i + 1, x_axis, y_axis)
        elif int(i / nodes_no) % 2 == 1:
            arrow_generation(arrow_spacing * -1, 0, 0, arrows, i, i + 1, x_axis, y_axis)

    fig.update_layout(
        annotations=arrows,
        xaxis=dict(
            range=[-0.40, nodes_no - 1 + 0.40],
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[-1, 0],
            showline=False,
            showgrid=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0,
        ),
    )

    return fig


def arrow_generation(arrow_spacing_x, arrow_spacing_y_top, arrow_spacing_y_bottom, arrows, i, j, x_axis, y_axis):
    arrows.append(dict(
        ax=x_axis[i] + arrow_spacing_x,
        ay=y_axis[i] - arrow_spacing_y_top,
        axref='x',
        ayref='y',
        x=x_axis[j] - arrow_spacing_x,
        y=y_axis[j] + arrow_spacing_y_bottom,
        xref='x',
        yref='y',
        textangle=0,
        arrowcolor="steelblue",
        arrowsize=1,
        arrowwidth=3,
        arrowhead=1,
    )
    )


def tree_path_json(input_key, path):
    fig = tree_path_fig(input_key, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized


def plot_tree_path(input_key):
    fig = tree_path_fig(input_key, "out/test1/small.wordSensePath.txt")
    fig.show()
    return ""


def calculate_node_position(colors, nodes_no, proc_data, symbols, x_axis, y_axis):
    for i in proc_data:
        index = proc_data.index(i)
        y_axis.append(int(index / nodes_no) * -1 / 2)
        if int(index / nodes_no) % 2 == 0:
            x_axis.append((int(index % nodes_no)))
            if index == len(proc_data) - 1:
                symbols.append('circle')
                colors.append('darkslategrey')
            elif index == 0:
                symbols.append('square')
                colors.append('darkslategrey')
            else:
                symbols.append('circle')
                colors.append('steelblue')
        if int(index / nodes_no) % 2 == 1:
            x_axis.append((nodes_no - 1 - int(index % nodes_no)))
            if index == len(proc_data) - 1:
                symbols.append('circle')
                colors.append('darkslategrey')
            else:
                symbols.append('circle')
                colors.append('steelblue')
