def main():
    st.title("ARIMA Prediction")

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
