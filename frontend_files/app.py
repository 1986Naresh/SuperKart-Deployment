import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="SuperKart Sales Prediction", layout="wide")

st.title("SuperKart Sales Prediction App 🛒")

# Sidebar for navigation
st.sidebar.header("Navigation")
mode = st.sidebar.radio("Select Inference Mode", ["Online Inference", "Batch Inference"])

# Backend API URL
#backend_url = st.sidebar.text_input("Backend API URL", value="http://backend:7860")
backend_url = os.getenv("BACKEND_URL", "http://localhost:7860")

if mode == "Online Inference":
    st.header("Online Inference")
    st.write("Enter product and store details to predict sales.")

    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=4.0, value=22.0)
        product_sugar_content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
        product_allocated_area = st.number_input("Product Allocated Area", min_value=0.003, max_value=0.30, value=0.05, step=0.001, format="%.3f")
        product_mrp = st.number_input("Product MRP", min_value=31.0, max_value=266.0, value=150.0, step=1.0)

    with col2:
        store_size = st.selectbox("Store Size", ['Small', 'Medium', 'High'])
        store_location_city_type = st.selectbox("Store Location City Type", ['Tier 1', 'Tier 2', 'Tier 3'])
        store_type = st.selectbox("Store Type", ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart'])

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type
        }
        try:
            response = requests.post(f"{backend_url}/v1/predict", json=payload, timeout=10)
            if response.status_code == 200:
                prediction = response.json().get('prediction')
                st.success(f"Predicted Sales: {prediction:.2f}")
            else:
                st.error(f"Error from backend: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

else:
    st.header("Batch Inference")
    st.write("Upload a CSV file containing product and store details.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        if st.button("Predict Batch Sales"):
            try:
                files = {'file': (uploaded_file.name,uploaded_file.getvalue(), "text/csv")}
                response = requests.post(f"{backend_url}/v1/predictbatch", files=files, timeout=300)

                if response.status_code == 200:
                    predictions = response.json()
                    st.success("Predictions successfully generated!")

                    # Read the uploaded file to append predictions
                    df = pd.read_csv(uploaded_file)
                    df['Predicted_Sales'] = [predictions.get(str(i)) for i in range(len(df))]
                    st.dataframe(df.head())

                    # Provide download link
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Predictions as CSV",
                        data=csv,
                        file_name='batch_predictions.csv',
                        mime='text/csv',
                    )
                else:
                    st.error(f"Error from backend: {response.text}")

            except requests.exceptions.Timeout:
                st.error("Backend request timed out. Please try again.")

            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend service.")

            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
            #except Exception as e:
             #   st.error(f"Failed to connect to backend: {e}")
