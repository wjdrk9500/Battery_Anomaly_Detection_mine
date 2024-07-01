import os
import sys
import pandas as pd
from preprocessing import *
from preprocessing2 import *
from Inference1 import *

def load_data(data_num):
    file_list = os.listdir("./Data")
    file = [file for file in file_list if str(data_num) in file]
    df_dir = "./Data/" + file[0]
    return pd.read_csv(df_dir)

def calculate_score(df_test, data_num):
    preprocess = PreprocessPipe()
    df = preprocess.fit_transform(df_test)
    X, index = time_segments_aggregate(df, interval = 1, time_column = 'date')
    X = simple_minmax(X)
    X, y, X_index, y_index = rolling_window_sequences(X, index, window_size = 10,   target_size = 1, step_size =1, target_column=0)
    y_hat, critic = predict(X)
    final_result = anomaly(X, y_hat, critic, X_index)
    final_result["data_num"] = data_num
    final_result.to_csv("./Dashboard/result.csv")
    # open('./Dashboard/result.csv', 'w').write(final_result.to_csv())

data_num = sys.argv[1]
df_test = load_data(data_num)
calculate_score(df_test, data_num)
