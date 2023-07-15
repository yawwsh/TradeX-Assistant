import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

@st.cache
def load_data():
    data_url = 'https://drive.google.com/file/d/1JE9nCnPrrS7Y4jTwBov7G0DqGJkk-Go9/view?usp=sharing'
    file_id = data_url.split('/')[-2]
    csv_url = f'https://drive.google.com/uc?id={file_id}'
    dataset = pd.read_csv(csv_url)
    return dataset

def run_arima(dataset, p, d, q):
    # Splitting into train and test
    to_row = int(len(dataset) * 0.9)
    training = list(dataset[0:to_row]['Adj Close'])
    testing = list(dataset[to_row:]['Adj Close'])

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

def main():
    st.title("ARIMA Prediction")

    dataset = load_data()

    p = st.text_input("AR Order (p)", "4")
    d = st.text_input("Difference Order (d)", "1")
    q = st.text_input("MA Order (q)", "0")

    if st.button("Run ARIMA"):
        p = int(p)
        d = int(d)
        q = int(q)
        run_arima(dataset, p, d, q)

if __name__ == '__main__':
    main()
