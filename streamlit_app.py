import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import gdown

# Function to load the dataset
def load_dataset():
    # Download the dataset from Google Drive
    url = 'https://drive.google.com/uc?id=1JE9nCnPrrS7Y4jTwBov7G0DqGJkk-Go9'
    output_path = 'dataset.csv'
    gdown.download(url, output_path, quiet=False)
    
    # Load the downloaded dataset
    dataset = pd.read_csv(output_path)
    return dataset

# Function to train and make predictions using ARIMA model
def run_arima(dataset, order):
    # Splitting into train and test
    to_row = int(len(dataset) * 0.9)
    training = list(dataset[0:to_row]['Adj Close'])
    testing = list(dataset[to_row:]['Adj Close'])

    # Making model
    model_predictions = []
    n_test_obser = len(testing)

    for i in range(n_test_obser):
        model = ARIMA(training, order=order)
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        model_predictions.append(yhat)
        actual_test_value = testing[i]
        training.append(actual_test_value)

    return model_predictions

def main():
    # Load the dataset
    dataset = load_dataset()

    # Set up the sidebar and user input
    st.sidebar.title("ARIMA Prediction")
    st.sidebar.subheader("Choose ARIMA Order:")
    p = st.sidebar.slider("p (AR Order)", 0, 10, 4)
    d = st.sidebar.slider("d (Difference Order)", 0, 10, 1)
    q = st.sidebar.slider("q (MA Order)", 0, 10, 0)

    order = (p, d, q)

    # Run ARIMA model and get predictions
    predictions = run_arima(dataset, order)

    # Display the predicted results
    st.title("ARIMA Prediction")
    st.subheader("User Input:")
    st.write(f"AR Order (p): {p}")
    st.write(f"Difference Order (d): {d}")
    st.write(f"MA Order (q): {q}")

    st.subheader("Predicted Results:")
    for i, pred in enumerate(predictions):
        st.write(f"Prediction {i+1}: {pred}")

if __name__ == '__main__':
    main()
