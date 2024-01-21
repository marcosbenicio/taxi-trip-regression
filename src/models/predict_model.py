from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd
import numpy as np

# Load the trained XGBoost model
model = xgb.Booster()
model.load_model('models/xgb_taxi_trip.json')

def single_prediction(features, model):
    # Convert the dictionary of features into a DataFrame
    X = pd.DataFrame([features])
    
    # Create DMatrix for XGBoost
    dmatrix = xgb.DMatrix(X)
    
    prediction_log = model.predict(dmatrix)
    # Convert log prediction back to original scale
    prediction = np.expm1(prediction_log)
    
    return float(prediction)

# Initialize Flask app
app = Flask('taxi_trip_duration_prediction')

# Define the predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data with trip features
        trip_features = request.get_json(force=True)

        # Make single prediction with JSON data
        prediction = single_prediction(trip_features, model)
        
        # Convert to hours, minutes and seconds
        hours, remainder = divmod(prediction, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Return prediction as JSON
        response = {
            'Trip Duration (hours:minutes:seconds)': f'{int(hours)}:{int(minutes)}:{int(seconds)}'
        }
        return jsonify(response)
    
    except Exception as e:
        # If an error occurs, return the error message
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
    
