import pandas as pd


def aggregateDf(df, timestampCol, tsRollup=True):
    """
    Utility function to aggregate dataframe on timestamp column
    """
    df.dropna(inplace=True)
    if tsRollup:
        df = df.groupby(timestampCol).sum()
        df.reset_index(inplace=True)
    df.columns = ["ds" if col == timestampCol else "y" for col in df.columns]
    return df


def prepareAnomalyDataframes(
    datasetDf, timestampCol, metricCol, dimensionCol=None, operation=None, value=10, nonRollup=False
):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension
    """
    if datasetDf is None:
        raise Exception("Empty dataframe received, forgoing anomaly detection")
    try:
        datasetDf[metricCol] = pd.to_numeric(datasetDf[metricCol])
        datasetDf[metricCol] = datasetDf[metricCol].fillna(0)
    except Exception as ex:
        raise Exception(f"Metric column containing non numeric data: {ex}")

    dimValsData = []

    if nonRollup:
        if dimensionCol:
            if operation == "Min Avg Value":
                dimValsData = minAvgValueOnDimensionalValuesNonRollup(datasetDf, timestampCol, metricCol, dimensionCol, value)
        else:
            tempDf = datasetDf[[timestampCol, metricCol]]
            dimValsData.append(
                {
                    "dimVal": None,
                    "contriPercent": 100.0,
                    "df": aggregateDf(tempDf, timestampCol, tsRollup=False),
                }
            )
    elif dimensionCol:
        if operation == "Top":
            dimValsData = topNDimensionalValues(
                datasetDf, timestampCol, metricCol, dimensionCol, int(value)
            )
        elif operation == "Min % Contribution":
            dimValsData = contributionOnDimensionalValues(
                datasetDf, timestampCol, metricCol, dimensionCol, value
            )

        elif operation == "Min Avg Value":
            dimValsData = minAvgValueOnDimensionalValues(datasetDf, timestampCol, metricCol, dimensionCol, value)
        else:
            dimValsData = topNDimensionalValues(datasetDf, timestampCol, metricCol, dimensionCol, 10)
    else:
        tempDf = datasetDf[[timestampCol, metricCol]]
        dimValsData.append(
            {
                "dimVal": None,
                "contriPercent": 100.0,
                "df": aggregateDf(tempDf, timestampCol),
            }
        )

    return dimValsData


def topNDimensionalValues(
    datasetDf, timestampCol, metricCol, dimensionCol=None, topN=10
):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension for Top N dimensional values
    """
    dimValsData = []
    datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
    topValsDf = (
        datasetDf[[dimensionCol, metricCol]]
        .groupby(dimensionCol)
        .sum()
        .sort_values(metricCol, ascending=False)
    )
    dimVals = list(topValsDf[:topN].index)
    total = datasetDf[metricCol].sum()
    for dimVal in dimVals:
        tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
        contriPercent = int(10000 * (tempDf[metricCol].sum() / total)) / 100
        dimValsData.append(
            {
                "dimVal": dimVal,
                "contriPercent": contriPercent,
                "df": aggregateDf(tempDf, timestampCol),
            }
        )

    return dimValsData


def contributionOnDimensionalValues(
    datasetDf, timestampCol, metricCol, dimensionCol=None, value=1
):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension for dimensional values
    """
    dimValsData = []
    datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
    topValsDf = (
        datasetDf[[dimensionCol, metricCol]]
        .groupby(dimensionCol)
        .sum()
        .sort_values(metricCol, ascending=False)
    )
    dimVals = list(topValsDf[:].index)
    total = datasetDf[metricCol].sum()
    for dimVal in dimVals:
        tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
        contriPercent = int(10000 * (tempDf[metricCol].sum() / total)) / 100
        if contriPercent >= value:
            dimValsData.append(
                {
                    "dimVal": dimVal,
                    "contriPercent": contriPercent,
                    "df": aggregateDf(tempDf, timestampCol),
                }
            )

    return dimValsData


def minAvgValueOnDimensionalValues(
    datasetDf, timestampCol, metricCol, dimensionCol=None, value=1
):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension for dimensional values
    """
    dimValsData = []
    datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
    topValsDf = (
        datasetDf[[dimensionCol, metricCol]]
        .groupby(dimensionCol)
        .sum()
        .sort_values(metricCol, ascending=False)
    )
    dimVals = list(topValsDf[:].index)
    total = datasetDf[metricCol].sum()
    for dimVal in dimVals:
        tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
        totalSum = tempDf[metricCol].sum()
        tempDf = tempDf.groupby(timestampCol).sum() 
        totalRow = (tempDf[metricCol] > 0).sum(axis=0)
        avg = int(totalSum/totalRow)

        if avg >= value:
            contriPercent = int(10000 * (totalSum / total)) / 100
            dimValsData.append(
                {
                    "dimVal": dimVal,
                    "contriPercent": contriPercent,
                    "df": aggregateDf(tempDf, timestampCol),
                }
            )

    return dimValsData

def minAvgValueOnDimensionalValuesNonRollup(
    datasetDf, timestampCol, metricCol, dimensionCol=None, value=1
):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension for dimensional values
    """
    dimValsData = []
    datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
    topValsDf = (
        datasetDf[[dimensionCol, metricCol]]
        .groupby(dimensionCol)
        .mean()
        .sort_values(metricCol, ascending=False)
    )
    dimVals = list(topValsDf[topValsDf[metricCol]>value].index)
    for dimVal in dimVals:
        tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
        dimValsData.append(
            {
                "dimVal": dimVal,
                "contriPercent": "",
                "df": aggregateDf(tempDf, timestampCol, tsRollup=False),
            }
        )

    return dimValsData
