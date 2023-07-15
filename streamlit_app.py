import streamlit as st
import pickle
from statsmodels.tsa.arima.model import ARIMAResults

def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def run_arima(model, p, d, q):
    # Make predictions using the loaded model
    prediction = model.forecast(steps=1)[0]
    return prediction

def main():
    st.title("ARIMA Prediction")

    st.write("User Input:")
    model_path = "https://drive.google.com/uc?id=1zSK5LCTB1NE1UIYyaNFuMnm6CHt9nl7i"
    p = st.text_input("AR Order (p)", "4")
    d = st.text_input("Difference Order (d)", "1")
    q = st.text_input("MA Order (q)", "0")

    if st.button("Run ARIMA"):
        try:
            p = int(p)
            d = int(d)
            q = int(q)

            model = load_model(model_path)
            st.write("Predicted Result:")
            prediction = run_arima(model, p, d, q)
            st.write(f"Prediction: {prediction}")
            
            # Add your buy/sell recommendation logic here based on the prediction

        except ValueError:
            st.write("Invalid input. Please enter integer values for AR Order, Difference Order, and MA Order.")

if __name__ == '__main__':
    main()
