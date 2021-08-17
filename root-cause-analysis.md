---
description: One-click root cause analysis for anomalies
---

# Root Cause Analysis

To do root cause analysis on an anomaly card, click the `Analyze` button. 

CueObserve considers the latest anomalous data point as the parent anomaly. It then starts looking for child anomalies across all other dimensions in the dataset.

Under the hood, CueObserve does the following:

It takes the latest anomalous data point from the card. The anomalous data point is defined by its \(X, Y\) values:

* X value: time period
* Y value: measure for a dimension value. e.g. Orders where state = CA

It applies the dimension value filter on the original dataset.

It then runs anomaly detection jobs on each dimension in this filtered dataset. It splits each dimension. It inherits the split limit from the original anomaly definition. If the original anomaly definition doesn't have a split, it limits the split to dimension values that have a minimum contribution of 1% to the filtered measure value.

It then collates all dimension values that had an anomaly in the same time period as the parent anomaly.

