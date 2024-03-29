import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from joblib import dump
import numpy as np


np.random.seed(42)


base_dir = os.getcwd()
first_innings_data_path = os.path.join(base_dir, 'First_Innings.csv')
second_innings_data_path = os.path.join(base_dir, 'Second_Innings.csv')
model_dir = os.path.join(base_dir, 'models')


os.makedirs(model_dir, exist_ok=True)


def train_models(data_path, innings_type):
   
    df = pd.read_csv(data_path)

    
    df_sampled = df.sample(n=5100)

    
    df_train = df_sampled.head(5000)
    df_validate = df_sampled.tail(1000)

    
    feature_cols = ['Runs', 'Overs', 'Wickets'] + (['Chasing score'] if innings_type == 'Second' else [])
    X_train = df_train[feature_cols]
    y_train = df_train['Total']

    
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    
    poly_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    poly_model.fit(X_train, y_train)

    
    svr_model = SVR(C=1.0, epsilon=0.2)
    svr_model.fit(X_train, y_train)

    
    dump(linear_model, os.path.join(model_dir, f'linear_regression_model_{innings_type}.joblib'))
    dump(poly_model, os.path.join(model_dir, f'polynomial_regression_model_{innings_type}.joblib'))
    dump(svr_model, os.path.join(model_dir, f'svr_model_{innings_type}.joblib'))

    print(f"{innings_type} Innings models trained and saved successfully.")

# Train and save models for First Innings
train_models(first_innings_data_path, 'First')

# Train and save models for Second Innings
train_models(second_innings_data_path, 'Second')
