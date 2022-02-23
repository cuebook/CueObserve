# Anomaly Detection

When you run an anomaly definition, CueObserve does the following:

### Execute Dataset SQL

As the first step in the anomaly detection process, CueObserve executes the dataset's SQL query and fetches the result as a dataframe. This dataframe acts as the source data for identifying dimension values and the anomaly detection process.

### Generate sub dataframes

Next CueObserve creates new dataframes on which the actual anomaly detection process will run. During this process, CueObserve finds dimension values and creates sub-dataframes by filtering on the dimension. This filtering process is done only if a dimension is specified in the anomaly definition.

### Transform sub dataframe

Once CueObserve has the final dataframes, it ignores all columns except the metric and the timestamp and then aggregates the metric on the timestamp column. That is, the metric is summed after grouping over the timestamp column. CueObserve now has dataframes agnostic of all metadata which is unnecessary for the actual anomaly detection process.

### Generate Timeseries Forecast

CueObserve now feeds the timeseries dataframe into [Prophet](https://github.com/facebook/prophet). Each dataframe is separately trained on Prophet and a forecast is generated. The number of forecast points is 24 if the granularity is hourly, else it is 15 for daily granularity.

Each dataframe must have at least 20 data points after aggregation as anything less than that would be too little training data. For hourly granularity, CueObserve does not consider data older than a week for the training process.

### Detect Anomaly

Next CueObserve combines the actual data with the forecasted data from Prophet along with the uncertainty interval bands. These bands estimate the trend of the data and will be used as the threshold for determining a data point as an anomaly. For each data point in the original dataframe, CueObserve checks if it lies within the predicted bands or not and classifies it as an anomaly accordingly.

### Create Card

CueObserve saves the actual data with the bands and the forecast in its database. If the latest anomalous data point is not older than a certain time threshold, CueObserve publishes it as an anomaly and saves the dimension value and its contribution. The aforementioned time threshold depends on the granularity. It is 5 days if the granularity is daily and 1 day if the granularity is hourly.

Finally, CueObserve stores all the individual results of the process along with the metadata in a format for easy visual representation in the UI.
