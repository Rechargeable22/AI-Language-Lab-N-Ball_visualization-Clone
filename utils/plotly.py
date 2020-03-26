import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import utils.balls_to_json as util
import json
import plotly

def plot_balls():
    ball = util.balls_to_object("out/test1/reduced_nballs_after.txt")

    fig = go.Figure()

    # Create scatter trace of text labels
    # fig.add_trace(go.Scatter(
    #     x=[1.5, 3.5],
    #     y=[0.75, 2.5],
    #     text=["Unfilled Circle",
    #           "Filled Circle"],
    #     mode="text",
    # ))

    # Set axes properties
    # fig.update_xaxes(range=[0, 4.5], zeroline=False)
    # fig.update_yaxes(range=[0, 4.5])

    circles = []
    for b in ball:
        circles.append(dict(
            type="circle",
            xref="x",
            yref="y",
            x0=b.vector[0] - b.radius,
            y0=b.vector[1] - b.radius,
            x1=b.vector[0] + b.radius,
            y1=b.vector[1] + b.radius,
            line_color="LightSeaGreen",
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

    # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    # fig.show(config={'scrollZoom': True})

    return serialized