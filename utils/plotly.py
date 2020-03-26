import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import utils.balls_to_json as util


def plot_balls():
        ball = util.balls_to_object("out/test1/reduced_nballs_after.txt")

        df = pd.DataFrame([t.__dict__ for t in ball])
        df[['x', 'y']] = pd.DataFrame(df.vector.values.tolist(), index=df.index)
        print(df.to_string())
        df['x0'] = df.x - df.radius
        df['x1'] = df.x + df.radius
        df['y0'] = df.y - df.radius
        df['y1'] = df.y + df.radius
        print(df.to_string())

        final_df = df.sort_values(by=['radius'], ascending=False)
        print(final_df.to_string())

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=final_df["x"],
            y=final_df["y0"] - (final_df["radius"]*0.05),
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

        return fig.show(config={'scrollZoom': True})
