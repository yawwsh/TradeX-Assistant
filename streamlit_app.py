import streamlit as st
import requests
import pickle
from statsmodels.tsa.arima.model import ARIMAResults

def download_file_from_url(url, destination):
    response = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def run_arima(model, p, d, q):
    # Make predictions using the loaded model
    prediction = model.forecast(steps=1)[0]
    return prediction

def main():
    st.title("BTC Prediction Bot")

    st.write("User Input:")
    model_url = "https://drive.google.com/uc?id=1zSK5LCTB1NE1UIYyaNFuMnm6CHt9nl7i"
    model_path = "arima_model.pkl"
    p = st.text_input("AR Order (p) - No. of previous observations to consider", "4")
    d = st.text_input("Difference Order (d)- No of differencing operations", "1")
    q = st.text_input("MA Order (q)- Moving Average", "0")
    latest_price = st.number_input("Latest Price", value=50000)  # Set a default value if needed

    if st.button("Run ARIMA"):
        try:
            p = int(p)
            d = int(d)
            q = int(q)

            download_file_from_url(model_url, model_path)
            model = load_model(model_path)
            st.write("Predicted Result:")
            prediction = run_arima(model, p, d, q)
            st.write(f"Future Price Prediction: {prediction}")

            if prediction < latest_price:
                st.write("Recommendation: Buy")
            else:
                st.write("Recommendation: Sell")

        except ValueError:
            st.write("Invalid input. Please enter integer values for AR Order, Difference Order, and MA Order.")

if __name__ == '__main__':
    main()
