
import pandas as pd
import pickle

try:
    # Try reading csv
    try:
        df = pd.read_csv('laptop_price.csv', encoding='latin-1')
        with open('data_info.txt', 'w') as f:
            f.write("CSV Columns:\n")
            f.write(str(list(df.columns)) + "\n")
            f.write("Sample Row:\n")
            f.write(str(df.iloc[0].to_dict()) + "\n")
            
            # Check unique values for likely categorical columns
            f.write("\nUnique Values:\n")
            for col in df.select_dtypes(include=['object']).columns:
                unique_vals = df[col].unique().tolist()
                if len(unique_vals) < 50:
                    f.write(f"{col}: {unique_vals}\n")
    except Exception as e:
        with open('data_info.txt', 'w') as f:
            f.write(f"CSV Read Error: {e}\n")

    # Try loading model
    try:
        with open('laptop_price_predictor.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('model_info.txt', 'w') as f:
            f.write(f"Model Type: {type(model)}\n")
            if hasattr(model, 'feature_names_in_'):
                 f.write(f"Feature Names: {model.feature_names_in_}\n")
    except Exception as e:
        with open('model_info.txt', 'w') as f:
            f.write(f"Model Load Error: {e}\n")

except Exception as e:
    with open('script_error.txt', 'w') as f:
        f.write(str(e))
