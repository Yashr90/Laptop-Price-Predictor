
import pickle
import numpy as np
import sys

# Ensure numpy prints everything
np.set_printoptions(threshold=sys.maxsize)

try:
    with open('laptop_price_predictor.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('model_features.txt', 'w') as f:
        if hasattr(model, 'feature_names_in_'):
            for name in model.feature_names_in_:
                f.write(f"{name}\n")
        else:
            f.write("No feature_names_in_ found.\n")
except Exception as e:
    with open('model_features_error.txt', 'w') as f:
        f.write(str(e))
