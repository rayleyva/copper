# coding=utf-8
import re
import numpy as np
import pandas as pd
from sklearn import preprocessing

_numberRE = re.compile('[0-9.]+')

def _numberREFun(x):
    try:
        return float(_numberRE.search(x).group())
    except:
        return 0

def to_number(series):
    return series.apply(_numberREFun)

def _money2number( series):
    '''
    Converts a Series with money format to a numbers

    Parameters
    ----------
        series: pandas.Series, target to convert

    Returns
    -------
        pandas.Series with the converted data
    '''
    ans = pd.Series(index=series.index, name=series.name, dtype=float)
    splits = ''.join(money_symbols) + ','

    for index, value in zip(frame.index, series):
        if type(value) == str:
            # number = re.match(r"[0-9]{1,3}(?:\,[0-9]{3})+(?:\.[0-9]{1,10})", value)
            for split in splits:
                value = ''.join(value.split(split))
            ans[index] = float(value)
    return ans

def category2ml(series):
    '''
    Converts a Series with category format to a format for machine learning
    Represents the same information on different columns of ones and zeros

    Parameters
    ----------
        series: pandas.Series, target to convert

    Returns
    -------
        pandas.DataFrame with the converted data
    '''
    ans = pd.DataFrame(index=series.index)
    categories = list(set(series))
    categories.sort()
    for category in categories:
        n_col = pd.Series(np.zeros(len(series)), index=series.index, dtype=int)
        n_col.name = '%s [%s]' % (series.name, category)
        n_col[series == category] = 1
        ans = ans.join(n_col)
    return ans

def category2number( series):
    '''
    Convert a Series with categorical information to a Series of numbers
    using the scikit-learn LabelEncoder

    Parameters
    ----------
        series: pandas.Series, target to convert

    Returns
    -------
        pandas.Series with the converted data
    '''
    le = preprocessing.LabelEncoder()
    le.fit(series.values)
    vals = le.transform(series.values)
    return pd.Series(vals, index=series.index, name=series.name, dtype=float)

def category_labels( series):
    '''
    Return the labels for a Series with categorical values

    Parameters
    ----------
        series: pandas.Series, target to convert

    Returns
    -------
        list, labels of the series
    '''
    le = preprocessing.LabelEncoder()
    le.fit(series.values)
    return le.classes_
