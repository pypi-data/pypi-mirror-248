import numpy as np
import pandas as pd


# ----------------------Data Reading----------------------------------#
def read_csv(file_path):
    return pd.read_csv(file_path)


def read_excel(file_path):
    return pd.read_excel(file_path)


def read_json(file_path):
    return pd.read_json(file_path)


# ----------------------Data Summary---------------------------------#
def generate_summary(data):
    summary = {
        'average': data.mean(),
        'most_frequent': data.mode().iloc[0]
    }
    return summary


# ---------------------Handling Missing Values---------------------#
def handle_missing_values(data, strategy='remove'):
    if strategy == 'remove':
        return data.dropna()
    elif strategy == 'impute_mean':
        return data.fillna(data.mean())
    elif strategy == 'impute_median':
        return data.fillna(data.median())
    else:
        raise ValueError("Invalid missing values handling strategy")


# --------------------Categorical Data Encoding---------------------#
def encode_categorical(data, columns_to_encode):
    return pd.get_dummies(data, columns=columns_to_encode)