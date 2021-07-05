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
    dataframes = []
    dimVals= []
    if dimensionCol:
        datasetDf = datasetDf[[timestampCol, dimensionCol, metricCol]]
        topValsDf = datasetDf[[dimensionCol, metricCol]].groupby(dimensionCol).sum().sort_values(metricCol, ascending=False)
        dimVals = list(topValsDf[:topN].index)
        for dimVal in dimVals:
            tempDf = datasetDf[datasetDf[dimensionCol] == dimVal][[timestampCol, metricCol]]
            dataframes.append(aggregateDf(tempDf, timestampCol))
    else:
        tempDf = datasetDf[[timestampCol, metricCol]]
        dimVals = [None]
        dataframes.append(aggregateDf(tempDf, timestampCol))
    
    return dimVals, dataframes


