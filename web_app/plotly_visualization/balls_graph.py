import pandas as pd
import plotly.graph_objects as go
import numpy as np


import json
import plotly

def plot_balls(balls):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[x.vector[0] for x in balls],
        y=[x.vector[1]-x.radius - (x.radius*0.1) for x in balls] ,
        text=[x.word for x in balls],
        mode="text",
    ))
    np.random.seed(0)
    circles = []
    for b in balls:
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
            showline=False,
            showgrid=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,

        ),
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        showlegend=False,
        plot_bgcolor='rgb(240, 240, 240)',
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