
import React, { useState } from 'react';
import './index.css';


function App() {
  const [formData, setFormData] = useState({
    company: 'Apple',
    typename: 'Ultrabook',
    ram: 8,
    weight: 1.5,
    touchscreen: false,
    ips: false,
    inches: 13.3,
    resolution: '1920x1080',
    cpu_brand: 'Intel Core i5',
    hdd: 0,
    ssd: 256,
    flash: 0,
    hybrid: 0,
    gpu_brand: 'Intel',
    opsys: 'macOS'
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currency, setCurrency] = useState('EUR');

  const exchangeRates = {
    EUR: { rate: 1, symbol: '€' },
    USD: { rate: 1.08, symbol: '$' },
    INR: { rate: 90.0, symbol: '₹' },
    GBP: { rate: 0.85, symbol: '£' }
  };

  const companies = ['Apple', 'HP', 'Acer', 'Asus', 'Dell', 'Lenovo', 'Chuwi', 'MSI', 'Microsoft', 'Toshiba', 'Huawei', 'Xiaomi', 'Vero', 'Razer', 'Mediacom', 'Samsung', 'Google', 'Fujitsu', 'LG'];
  const types = ['Ultrabook', 'Notebook', 'Netbook', 'Gaming', '2 in 1 Convertible', 'Workstation'];
  const rams = [2, 4, 6, 8, 12, 16, 24, 32, 64];
  const cpuBrands = ['Intel Core i7', 'Intel Core i5', 'Intel Core i3', 'Other Intel Processor', 'AMD Processor'];
  const gpuBrands = ['Intel', 'Nvidia', 'AMD'];
  const opSys = ['macOS', 'Windows 10', 'No OS', 'Linux', 'Chrome OS', 'Windows 7', 'Android'];
  const resolutions = ['1366x768', '1600x900', '1920x1080', '2560x1440', '2560x1600', '2880x1800', '3200x1800', '3840x2160'];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Use config defined proxy or full URL if needed. 
      // During dev, vite proxy forwards /predict -> localhost:5000/predict
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (data.price) {
        setPrediction(data.price);
      } else {
        alert("Error: " + (data.error || "Unknown error"));
      }
    } catch (error) {
      console.error(error);
      alert("Failed to fetch prediction");
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Laptop Price Predictor</h1>
        <select 
          value={currency} 
          onChange={(e) => setCurrency(e.target.value)}
          style={{ width: 'auto', minWidth: '100px' }}
        >
          {Object.keys(exchangeRates).map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <form onSubmit={handleSubmit} className="form-grid">
        
        <div className="form-group">
          <label>Brand</label>
          <select name="company" value={formData.company} onChange={handleChange}>
            {companies.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Type</label>
          <select name="typename" value={formData.typename} onChange={handleChange}>
            {types.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>RAM (GB)</label>
          <select name="ram" value={formData.ram} onChange={handleChange}>
            {rams.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Weight (kg)</label>
          <input type="number" step="0.1" name="weight" value={formData.weight} onChange={handleChange} />
        </div>

        <div className="form-group toggle-group">
          <label htmlFor="touchscreen">Touchscreen</label>
          <input type="checkbox" id="touchscreen" name="touchscreen" checked={formData.touchscreen} onChange={handleChange} />
        </div>

        <div className="form-group toggle-group">
          <label htmlFor="ips">IPS Panel</label>
          <input type="checkbox" id="ips" name="ips" checked={formData.ips} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label>Screen Size (Inches)</label>
          <input type="number" step="0.1" name="inches" value={formData.inches} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label>Resolution</label>
          <select name="resolution" value={formData.resolution} onChange={handleChange}>
            {resolutions.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>CPU</label>
          <select name="cpu_brand" value={formData.cpu_brand} onChange={handleChange}>
            {cpuBrands.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>GPU Brand</label>
          <select name="gpu_brand" value={formData.gpu_brand} onChange={handleChange}>
            {gpuBrands.map(g => <option key={g} value={g}>{g}</option>)}
          </select>
        </div>
        
        <div className="form-group">
          <label>OS</label>
          <select name="opsys" value={formData.opsys} onChange={handleChange}>
            {opSys.map(o => <option key={o} value={o}>{o}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Storage - HDD (GB)</label>
          <select name="hdd" value={formData.hdd} onChange={handleChange}>
             {[0, 128, 256, 500, 1000, 2000].map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Storage - SSD (GB)</label>
          <select name="ssd" value={formData.ssd} onChange={handleChange}>
             {[0, 8, 128, 256, 512, 1000].map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Price'}
        </button>

        {prediction && (
          <div className="result">
            <span>Estimated Price ({currency})</span>
            <h2>
              {exchangeRates[currency].symbol} 
              {(prediction * exchangeRates[currency].rate).toFixed(2)}
            </h2>
          </div>
        )}
      </form>
    </div>
  );
}


export default App;
