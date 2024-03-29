import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from joblib import dump
import numpy as np

# Setting a seed for reproducibility
np.random.seed(42)

# Define paths
base_dir = os.getcwd()
first_innings_data_path = os.path.join(base_dir, 'First_Innings.csv')
second_innings_data_path = os.path.join(base_dir, 'Second_Innings.csv')
model_dir = os.path.join(base_dir, 'models')

# Ensure the model directory exists
os.makedirs(model_dir, exist_ok=True)

# Function to load data, sample, split and train models
def train_models(data_path, innings_type):
    # Load dataset
    df = pd.read_csv(data_path)

    # Randomly sample 51000 entries from the dataset
    df_sampled = df.sample(n=5100)

    # Splitting the sampled dataframe into training and validation sets
    df_train = df_sampled.head(5000)
    df_validate = df_sampled.tail(1000)

    # Features and target variable
    feature_cols = ['Runs', 'Overs', 'Wickets'] + (['Chasing score'] if innings_type == 'Second' else [])
    X_train = df_train[feature_cols]
    y_train = df_train['Total']

    # Train multiple models
    # Linear Regression Model
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    # Polynomial Regression Model (Degree 2 for example)
    poly_model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    poly_model.fit(X_train, y_train)

    # Support Vector Regression Model
    svr_model = SVR(C=1.0, epsilon=0.2)
    svr_model.fit(X_train, y_train)

    # Save the models
    dump(linear_model, os.path.join(model_dir, f'linear_regression_model_{innings_type}.joblib'))
    dump(poly_model, os.path.join(model_dir, f'polynomial_regression_model_{innings_type}.joblib'))
    dump(svr_model, os.path.join(model_dir, f'svr_model_{innings_type}.joblib'))

    print(f"{innings_type} Innings models trained and saved successfully.")

# Train and save models for First Innings
train_models(first_innings_data_path, 'First')

# Train and save models for Second Innings
train_models(second_innings_data_path, 'Second')
