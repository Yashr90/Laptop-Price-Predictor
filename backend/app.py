
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load model
model_path = os.path.join(os.path.dirname(__file__), '../laptop_price_predictor.pkl')
model = None

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        
        # Initialize feature vector (37 features)
        input_vector = []
        
        # 1. Ram (int)
        input_vector.append(int(data.get('ram', 0)))
        
        # 2. Weight (float)
        input_vector.append(float(data.get('weight', 0)))
        
        # 3. Touchscreen (1/0)
        input_vector.append(1 if data.get('touchscreen') else 0)
        
        # 4. IPS_Panel (1/0)
        input_vector.append(1 if data.get('ips') else 0)
        
        # 5. HDD
        input_vector.append(int(data.get('hdd', 0)))
        
        # 6. SSD
        input_vector.append(int(data.get('ssd', 0)))
        
        # 7. Flash_Storage
        input_vector.append(int(data.get('flash', 0)))
        
        # 8. Hybrid
        input_vector.append(int(data.get('hybrid', 0)))
        
        # 9. Company One-Hot (18 companies)
        # Features: Apple, Asus, Chuwi, Dell, Fujitsu, Google, HP, Huawei, LG, Lenovo, MSI, Mediacom, Microsoft, Razer, Samsung, Toshiba, Vero, Xiaomi
        company = data.get('company')
        companies = ['Apple', 'Asus', 'Chuwi', 'Dell', 'Fujitsu', 'Google', 'HP', 'Huawei', 'LG', 'Lenovo', 'MSI', 'Mediacom', 'Microsoft', 'Razer', 'Samsung', 'Toshiba', 'Vero', 'Xiaomi']
        for c in companies:
            input_vector.append(1 if company == c else 0)
            
        # 10. TypeName One-Hot (5 types)
        # Features: Gaming, Netbook, Notebook, Ultrabook, Workstation
        typename = data.get('typename')
        types = ['Gaming', 'Netbook', 'Notebook', 'Ultrabook', 'Workstation']
        for t in types:
            input_vector.append(1 if typename == t else 0)
            
        # 11. OpSys One-Hot (2 columns)
        # Features: OpSys_Other/No OS, OpSys_Windows
        opsys = data.get('opsys')
        # Logic:
        # Windows -> OpSys_Windows=1, Other=0
        # Linux/NoOS/Android/Chrome -> OpSys_Other/No OS=1, Windows=0
        # Mac -> Both 0
        
        if opsys in ['Linux', 'No OS', 'Android', 'Chrome OS']:
            input_vector.append(1)  # OpSys_Other/No OS
        else:
            input_vector.append(0)
            
        if opsys in ['Windows 10', 'Windows 10 S', 'Windows 7', 'Windows']:
            input_vector.append(1) # OpSys_Windows
        else:
            input_vector.append(0)
        
        # 12. Cpu_Brand (1 column)
        # Feature: Cpu_Brand_Other Intel Processor
        # Logic: 1 if Intel but not Core i3/i5/i7. 0 otherwise.
        cpu_brand = data.get('cpu_brand') # Expected 'Intel Core i5', 'AMD', 'Intel Pentium' etc.
        if 'Intel' in cpu_brand and not any(x in cpu_brand for x in ['Core i7', 'Core i5', 'Core i3']):
            input_vector.append(1)
        else:
            input_vector.append(0)
        
        # 13. Gpu_Brand (2 columns)
        # Features: Gpu_Brand_Intel, Gpu_Brand_Nvidia
        gpu_brand = data.get('gpu_brand')
        input_vector.append(1 if gpu_brand == 'Intel' else 0)
        input_vector.append(1 if gpu_brand == 'Nvidia' else 0)
        # Note: AMD is 0,0.
        
        # 14. PPI
        # Calculated from Inches and Resolution
        res = data.get('resolution') # "1920x1080"
        inches = float(data.get('inches'))
        if inches > 0 and 'x' in res:
            width, height = map(int, res.lower().split('x'))
            ppi = ((width**2 + height**2)**0.5) / inches
        else:
            ppi = 0
        input_vector.append(ppi)
        
        # Predict
        prediction = model.predict([input_vector])
        return jsonify({'price': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
