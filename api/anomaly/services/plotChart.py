
import pandas as pd
import plotly.graph_objects as go
from anomaly.models import Anomaly


class PlotChartService:

    @staticmethod
    def anomalyChartToImgStr(anomalyId: int = 0):
        """ Generate anomaly chart and convert it to image """
        
        anomaly = Anomaly.objects.get(id=anomalyId)
        granularity = anomaly.anomalyDefinition.dataset.granularity
        data = anomaly.data
        anomalyData = data["anomalyData"]
        actualData = anomalyData["actual"]
        predictedData = anomalyData["predicted"]
        bandData = anomalyData["band"]
        actualDataDf = pd.DataFrame(actualData)
        predictedDataDf = pd.DataFrame(predictedData)
        bandLowerYaxis = [ band["y"][0] for band in bandData]
        bandUpperYaxis = [ band["y"][1] for band in bandData]
        bandXaxis = [ band["ds"] for band in bandData]
        anomalyDataDf = actualDataDf.loc[actualDataDf['anomaly'] == 15]
        anomalyXaxis = anomalyDataDf["ds"].to_list()
        anomalyYaxis = anomalyDataDf["y"].to_list()
        actualXaxis = actualDataDf["ds"].to_list()
        actualYaxis = actualDataDf["y"].to_list()
        predictedXaxis = predictedDataDf["ds"].to_list()
        predictedYaxis = predictedDataDf["y"].to_list()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=actualXaxis, y=actualYaxis,
                    mode='lines',
                    showlegend=False
                        ))
        fig.add_trace(go.Scatter(x=anomalyXaxis, y=anomalyYaxis,
                    mode='markers',
                    showlegend=False,
                    marker=dict(color="rgba(255,0,0,0.7)")

                    ))
        fig.add_traces(go.Scatter( x=predictedXaxis, y=predictedYaxis,
                    mode="lines",
                    showlegend=False,
                    line=dict(dash='dash', color="blue"))),
                    
        fig.add_traces(go.Scatter(
            name='Upper Bound',
            x=bandXaxis,
            y=bandUpperYaxis,
            mode='lines',
            marker=dict(color="#777"),
            line=dict(width=0),
            showlegend=False
        ))
        fig.add_traces(go.Scatter(
            name='Lower Bound',
            x=bandXaxis,
            y=bandLowerYaxis,
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
