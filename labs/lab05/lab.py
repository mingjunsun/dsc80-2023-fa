# lab.py


import os
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR', 'MD', 'MAR', 'NMAR', 'MAR'] 


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR', 'MAR', 'MD', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------

from scipy.stats import ks_2samp


def first_round():
    return [0.082, 'NR']


def second_round():
    return [0.03445, 'R', 'D']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    res={}
    for col in heights.columns:
        if 'child_' in col:
            df=heights.copy()
            df[col] = df[col].isna()
            res[col]=ks_2samp(df.loc[df[col] == True, 'father'],
                                df.loc[df[col] == False, 'father'])[1]
    return pd.Series(res)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    def mean_impute(ser):
        return ser.fillna(ser.mean())
    df = new_heights.copy()
    df['father'] = pd.qcut(df['father'], 4)
    res = (df
        .groupby('father')['child']
        .transform(mean_impute))
    return res


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    dist, intervals = np.histogram(child.dropna())
    proportion=dist/dist.sum()
    bin_width = np.diff(intervals)[0]
    pick_bin=np.random.choice(intervals[:-1],p = proportion,size=N)
    pick_num=[]
    for val in pick_bin:
        pick_num.append(np.random.uniform(val, val + bin_width))
    return np.array(pick_num)


def impute_height_quant(child):
    nulls=child.isna().sum()
    filled=np.random.choice(quantitative_distribution(child, N=nulls),nulls)
    child[child.isna()]=filled
    return child


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    multiple=[1, 2, 2, 1]
    webs=['https://canvas.ucsd.edu/robots.txt','https://www.yelp.com/robots.txt']
    return multiple, webs




