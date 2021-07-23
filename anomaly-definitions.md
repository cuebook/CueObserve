# Anomaly Definitions

You can define one or more anomaly detection jobs on a dataset.

![](.gitbook/assets/anomalydefinitions.png)

## Define Anomaly

`Measure` \[`Dimension` `Top N`\] \[`High/Low`\]

To break down a measure by a dimension, select the dimension and specify the number of unique dimension values you want to break into. CueObserve finds the `Top N` dimension values based on the dimension value's contribution to the measure. For each dimension value, it then generates a timeseries.

![](.gitbook/assets/anomalydefinition_cuel.gif)

Choose optional `High/Low` to detect only one type of anomalies. Choose `High` for an increase in metric or `Low` for a drop in metric.

## Anomaly Objects

For each anomaly definition, CueObserve creates one or more anomaly objects.

If the anomaly definition is broken down by a dimension, it generates upto N anomaly objects, one for each dimension value.

