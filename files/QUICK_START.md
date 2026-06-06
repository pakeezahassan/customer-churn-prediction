# 🚀 Quick Start Guide - Customer Churn Prediction

Get your project running in 5 minutes!

---

## ⚡ 5-Minute Quick Start

### 1. Download Dataset (2 minutes)
```bash
# Go to Kaggle: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
# Click "Download"
# Extract the ZIP file
# Place telecom_churn.csv in data/ folder
```

**Folder structure after:**
```
customer-churn-prediction/
└── data/
    └── telecom_churn.csv
```

### 2. Install Dependencies (1 minute)
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Train Model (2 minutes)
```bash
python src/train_churn_model.py
```

**Output:**
- ✅ `models/churn_model.pkl` (trained model)
- ✅ `outputs/01_churn_eda.png` (visualizations)
- ✅ `outputs/02_model_comparison.png` (model comparison)
- ✅ `outputs/03_confusion_and_roc.png` (confusion matrix & ROC)
- ✅ `outputs/04_feature_importance.png` (feature importance)

### 4. Deploy API (Optional - 1 minute)
```bash
# In new terminal
python src/app.py
```

Visit: http://localhost:5000

---

## 📁 Complete File Structure

```
customer-churn-prediction/
│
├── README.md                      ← Project overview
├── QUICK_START.md                 ← This file
├── requirements.txt               ← Dependencies
├── .gitignore                     ← Git ignore
│
├── data/
│   └── telecom_churn.csv         ← Download from Kaggle
│
├── src/
│   ├── train_churn_model.py      ← Main ML pipeline
│   └── app.py                     ← Flask API
│
├── models/
│   └── churn_model.pkl           ← Trained model (auto-generated)
│
└── outputs/
    ├── 01_churn_eda.png          ← EDA visualizations
    ├── 02_model_comparison.png   ← Model comparison
    ├── 03_confusion_and_roc.png  ← Confusion matrix & ROC
    └── 04_feature_importance.png ← Feature importance
```

---

## 🔧 Troubleshooting

### Problem: "Module not found" error
```bash
# Solution: Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Then install again:
pip install -r requirements.txt
```

### Problem: "telecom_churn.csv not found"
```bash
# Solution: 
# 1. Download from https://www.kaggle.com/datasets/blastchar/telco-customer-churn
# 2. Place in data/ folder
# 3. Make sure filename is exactly: telecom_churn.csv
```

### Problem: "Port 5000 already in use"
```bash
# Edit app.py, change last line:
app.run(port=5001)  # Use different port

# Or kill existing process:
# Windows:
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Problem: ImportError for scikit-learn
```bash
# Solution: Upgrade scikit-learn
pip install --upgrade scikit-learn
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated
- [ ] `pip list` shows all required packages
- [ ] `data/telecom_churn.csv` exists
- [ ] `python src/train_churn_model.py` runs without errors
- [ ] `models/churn_model.pkl` created
- [ ] 4 PNG files in `outputs/` folder
- [ ] `python src/app.py` starts Flask server
- [ ] http://localhost:5000 shows API page

---

## 🎯 Next Steps

### Option 1: Push to GitHub (Recommended!)
```bash
# Initialize git
git init

# Add files
git add .

# First commit
git commit -m "Initial commit: Customer churn prediction ML pipeline"

# Create repo on GitHub (github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/customer-churn-prediction.git
git branch -M main
git push -u origin main
```

### Option 2: Customize the Project
- Add your name to README
- Modify feature importance analysis
- Add more visualizations
- Create Jupyter notebooks
- Add API authentication

### Option 3: Deploy to Cloud
- **Heroku:** Simple Flask deployment
- **AWS:** Lambda + API Gateway
- **GCP:** Cloud Run
- **Azure:** App Service

---

## 💡 API Testing

### Using cURL
```bash
# Check health
curl http://localhost:5000/health

# Get model info
curl http://localhost:5000/info

# Make prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [65, 2, 34.65, 45, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]}'
```

### Using Python
```python
import requests
import json

url = "http://localhost:5000/predict"
data = {
    "features": [65, 2, 34.65, 45, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

### Expected Response
```json
{
  "prediction": 1,
  "prediction_label": "Will Churn",
  "probability_stay": 0.32,
  "probability_churn": 0.68,
  "confidence": 0.68,
  "timestamp": "2024-12-10T15:30:00",
  "success": true
}
```

---

## 📚 Project Files Explained

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `QUICK_START.md` | This quick start guide |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Files to exclude from Git |
| `src/train_churn_model.py` | Main ML pipeline (training) |
| `src/app.py` | Flask REST API server |
| `data/telecom_churn.csv` | Dataset (download separately) |
| `models/churn_model.pkl` | Saved trained model |
| `outputs/*.png` | Generated visualizations |

---

## 🎓 Learning Resources

- **scikit-learn:** https://scikit-learn.org/stable/
- **Pandas:** https://pandas.pydata.org/
- **Flask:** https://flask.palletsprojects.com/
- **Classification Metrics:** https://scikit-learn.org/stable/modules/model_evaluation.html

---

## 🌟 Show Your Project!

Once deployed to GitHub:

1. **Share the link**
   - LinkedIn: "Excited to share my ML project!"
   - Twitter: Include GitHub link and cool metric
   - Resume: Add to projects section

2. **Add a badge**
   ```markdown
   [![Model Performance](https://img.shields.io/badge/ROC--AUC-0.8512-brightgreen)](README.md)
   ```

3. **Write about it**
   - Medium article: "How I built a churn prediction model"
   - LinkedIn post: Key learnings and insights

---

## ⏱️ Expected Times

| Task | Time |
|------|------|
| Dataset download | 2-3 min |
| Environment setup | 3-5 min |
| Dependency installation | 2-3 min |
| Model training | 45 sec - 2 min |
| API deployment | 1 min |
| **Total** | **~15 minutes** |

---

## 🚀 You're Ready!

Your production-ready ML project is complete. Now:

1. ✅ Run `python src/train_churn_model.py`
2. ✅ Push to GitHub
3. ✅ Share with admissions committees
4. ✅ Stand out! 🌟

---

**Need help?** Check README.md or open an issue on GitHub.

Good luck! 🚀
