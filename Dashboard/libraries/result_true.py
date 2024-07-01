import os, sys
import pandas as pd

path = os.getcwd() + './Dashboard/result.csv'

def result_true():
    return os.path.exists(path)

def load_result():
    return pd.read_csv(path)

def remove_result():
    os.remove(path)