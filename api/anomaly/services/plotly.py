
from anomaly.models import Anomaly
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import Image
from PIL import Image
import base64
from io import BytesIO
import io
import logging
import os

class Plotly:

    @staticmethod
    def anomalyChartToImgStr(anomalyId: int = 0):
        """ Generate anomaly chart and convert it to image bytes """
        
        anomaly = Anomaly.objects.get(id=anomalyId)
        granularity = anomaly.anomalyDefinition.dataset.granularity
        data = anomaly.data
        anomalyData = data["anomalyData"]
        actualData = anomalyData["actual"]
        predictedData = anomalyData["predicted"]
        bandData = anomalyData["band"]
        bandDataDf = pd.DataFrame(bandData)
        actualDataDf = pd.DataFrame(actualData)
        predictedDataDf = pd.DataFrame(predictedData)
        band_lower_y = [ band["y"][0] for band in bandData]
        band_upper_y = [ band["y"][1] for band in bandData]
        band_x = [ band["ds"] for band in bandData]
        anomalyDataDf = actualDataDf.loc[actualDataDf['anomaly'] == 15]
        anomaly_x = anomalyDataDf["ds"].to_list()
        anomaly_y = anomalyDataDf["y"].to_list()
        actual_x = actualDataDf["ds"].to_list()
        actual_y = actualDataDf["y"].to_list()
        predicted_y = predictedDataDf["y"].to_list()
        predicted_x = predictedDataDf["ds"].to_list()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=actual_x, y=actual_y,
                    mode='lines',
                    showlegend=False
                        ))
        fig.add_trace(go.Scatter(x=anomaly_x, y=anomaly_y,
                    mode='markers',
                    showlegend=False,
                    marker=dict(color="rgba(255,0,0,0.7)")

                    ))
        fig.add_traces(go.Scatter( x=predicted_x, y=predicted_y,
                    mode="lines",
                    showlegend=False,
                    line=dict(dash='dash', color="blue"))),
                    
        fig.add_traces(go.Scatter(
            name='Upper Bound',
            x=band_x,
            y=band_upper_y,
            mode='lines',
            marker=dict(color="#777"),
            line=dict(width=0),
            showlegend=False
        ))
        fig.add_traces(go.Scatter(
            name='Lower Bound',
            x=band_x,
            y=band_lower_y,
            marker=dict(color="#777"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ))
        fig.update_traces(marker=dict(size=8,
                              line=dict(width=2,
                                    color='Red')),
                  selector=dict(mode='markers'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, zeroline=True, gridcolor="LightGray", zerolinecolor="LightGray", gridwidth=2, zerolinewidth=2)
        fig.update_layout(margin = {'r':10,'t':10,'l':10,'b':10}, plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(
            # dtick="M48",   # display x-ticks every 24 months months
            tickformat="%Y-%m-%d" if granularity == "day" else "%Y-%m-%d 00:00" # date format
        ) 
        # fig.show() # use to see chart locally
        img_bytes = fig.to_image(format="png") # pass img_bytes instead of png file

        return img_bytes
