import pandas as pd
import os, sys

def load_data(data_num):
    file_list = os.listdir("./Data")
    file = [file for file in file_list if str(data_num) in file]
    df_dir = "./Data/" + file[0]
    return pd.read_csv(df_dir)