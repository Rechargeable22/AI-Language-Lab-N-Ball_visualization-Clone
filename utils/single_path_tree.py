import plotly.graph_objects as go

from utils.files_utils import read_word_path

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
