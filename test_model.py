
import pickle
import numpy as np

try:
    with open('laptop_price_predictor.pkl', 'rb') as f:
        model = pickle.load(f)
    
    features = [
        8, 1.37, 0, 1, 0, 128, 0, 0, 
        1, # Apple
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 
        0,0,0,1,0, # Ultrabook
        0,0, 
        0, 
        1, 0, 
        226.98 
    ]
    
    vector = np.array([features])
    pred = model.predict(vector)
    with open('pred_result.txt', 'w') as f:
        f.write(f"Prediction: {pred[0]}")
    
except Exception as e:
    with open('pred_result.txt', 'w') as f:
        f.write(f"Error: {e}")
