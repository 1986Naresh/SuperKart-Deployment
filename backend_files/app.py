from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask("Superkart")

# Load the trained model
model = joblib.load('superkart_model.joblib')

# Define the expected features based on the training data
EXPECTED_FEATURES = [
    'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
    'Product_MRP', 'Store_Size', 'Store_Location_City_Type', 'Store_Type'
]

def preprocess_data(df):
    # Select only the features the model was trained on
    df_selected = df[EXPECTED_FEATURES].copy()
    
    # Map Product_Sugar_Content to numeric values just like in the training phase
    sugar_mapping = {'No Sugar': 0, 'Low Sugar': 1, 'Regular': 2, 'reg': 2}
    
    # Apply mapping. If it's already numeric, it will keep its value.
    df_selected['Product_Sugar_Content'] = df_selected['Product_Sugar_Content'].replace(sugar_mapping)
    
    return df_selected

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        df_processed = preprocess_data(df)
        
        prediction = model.predict(df_processed)
        return jsonify({'prediction': float(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['file']
        df = pd.read_csv(file)
        
        df_processed = preprocess_data(df)
        predictions = model.predict(df_processed)
        
        # Return predictions as a dictionary (index -> prediction)
        pred_dict = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(pred_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
