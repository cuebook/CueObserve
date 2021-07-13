import pandas as pd

def aggregateDf(df, timestampCol):
    """
    Utility function to aggregate dataframe on timestamp column
    """
    df.dropna(inplace=True)
    df = df.groupby(timestampCol).sum()
    df.reset_index(inplace=True)
    df.columns = ["ds" if col == timestampCol else "y" for col in df.columns]
    return df

def prepareAnomalyDataframes(datasetDf, timestampCol, metricCol, dimensionCol=None, topN=10):
    """
    Utility function to prepare anomaly dataframes by grouping on dimension
    """
    datasetDf[metricCol] = pd.to_numeric(datasetDf[metricCol])
    dimValsData = []
    if dimensionCol:
        datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
        topValsDf = datasetDf[[dimensionCol, metricCol]].groupby(dimensionCol).sum().sort_values(metricCol, ascending=False)
        dimVals = list(topValsDf[:topN].index)
        total = datasetDf[metricCol].sum()
        for dimVal in dimVals:
            tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
            contriPercent = int(10000 * (tempDf[metricCol].sum() / total)) / 100
            dimValsData.append({"dimVal": dimVal, "contriPercent": contriPercent, "df": aggregateDf(tempDf, timestampCol)})
    else:
        tempDf = datasetDf[[timestampCol, metricCol]]
        dimValsData.append({"dimVal": None, "contriPercent": 100.0, "df": aggregateDf(tempDf, timestampCol)})
    
    return dimValsData


