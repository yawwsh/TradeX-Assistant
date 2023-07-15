import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

@st.cache
def load_dataset():
    dataset = pd.read_csv("data.csv")
    return dataset

def preprocess_data(dataset):
    # Perform any preprocessing steps here
    # For example, converting the date column to datetime format, sorting the data, etc.
    df = dataset.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    return df

def run_arima(dataset, p, d, q):
    # Preprocess the dataset if required
    df = preprocess_data(dataset)

    # Splitting into train and test
    to_row = int(len(df) * 0.9)
    training = list(df[0:to_row]['Adj Close'])
    testing = list(df[to_row:]['Adj Close'])

    # Making model
    model_predictions = []
    n_test_obser = len(testing)

    for i in range(n_test_obser):
        model = ARIMA(training, order=(p, d, q))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        model_predictions.append(yhat)
        actual_test_value = testing[i]
        training.append(actual_test_value)

    return model_predictions

def main():
    st.title("BTC Prediction Bot")

    dataset = load_dataset()
    df = preprocess_data(dataset)

    st.write("User Input:")
    p = st.text_input("AR Order (p)", "4")
    d = st.text_input("Difference Order (d)", "1")
    q = st.text_input("MA Order (q)", "0")

    if st.button("Run ARIMA"):
        try:
            p = int(p)
            d = int(d)
            q = int(q)

            st.write("Predicted Results:")
            model_predictions = run_arima(df, p, d, q)
            st.write(f"Prediction 1: {model_predictions[0]}")

            if model_predictions[0] > df[-1]:
                st.write("Recommendation: Buy")
            else:
                st.write("Recommendation: Sell")

        except ValueError:
            st.write("Invalid input. Please enter integer values for AR Order, Difference Order, and MA Order.")

if __name__ == '__main__':
    main()
