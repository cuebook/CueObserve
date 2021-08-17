---
description: >-
  CueObserve helps you monitor your metrics. Know when, where, and why a metric
  isn't right.
---

# Overview

CueObserve uses **timeseries** **anomaly detection** to find **where** and **when** a metric isn't right. It then offers **one-click** **root cause analysis** so that you know **why** a metric isn't right.

CueObserve works with data in your SQL data warehouses and databases. It currently supports Snowflake, BigQuery, Redshift, Druid, Postgres, MySQL, and SQL Server.

![Anomaly](.gitbook/assets/overview_anomaly.png)

![Root Cause Analysis](.gitbook/assets/overview_rca.png)

## How it works

{% embed url="https://youtu.be/VZvgNa65GQU" %}

You write a SQL GROUP BY query, map its columns as dimensions and measures, and save it as a virtual Dataset.

![](.gitbook/assets/dataset_sql_cropped.png)

![](.gitbook/assets/dataset_mapping_cropped.png)

You then define one or more anomaly detection jobs on the dataset.

![](.gitbook/assets/anomalydefinitions.png)

When an anomaly detection job runs, CueObserve does the following:

1. Executes the SQL GROUP BY query on your datawarehouse and stores the result as a Pandas dataframe.
2. Generates one or more timeseries from the dataframe, as defined in your anomaly detection job.
3. Generates a forecast for each timeseries using [Prophet](https://github.com/facebook/prophet).
4. Creates a visual card for each timeseries. Marks the card as an anomaly if the last data point is anomalous.

## Features

* Automated SQL to timeseries transformation.
* Run anomaly detection on the aggregate metric or split it by any dimension. Limit the split to significant dimension values.
* Use Prophet or simple mathematical rules to detect anomalies. 
* In-built Scheduler. CueObserve uses Celery as the executor and celery-beat as the scheduler.
* Slack alerts when anomalies are detected
* Monitoring. Slack alert when a job fails. CueObserve maintains detailed logs.

#### Limitations

* Currently supports Prophet for timeseries forecasting.
* Not being built for real-time anomaly detection on streaming data.

## Support

For general help using CueLake, read the documentation, or go to [Github Discussions](https://github.com/cuebook/CueObserve/discussions). To report a bug or request a feature, open a [Github issue](https://github.com/cuebook/CueObserve/issues).

