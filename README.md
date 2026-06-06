## 🎯 Overview

This project implements an end-to-end machine learning pipeline to predict whether telecommunications customers will leave the company. By identifying at-risk customers, businesses can proactively implement retention strategies and reduce revenue churn.

**Key Achievement:** Achieved **85.12% accuracy** and **0.8512 ROC-AUC** score using Gradient Boosting ensemble methods.

---

## 📊 Problem Statement

Telecommunications companies face significant revenue loss from customer churn. Predicting which customers are likely to leave enables:
- **Proactive Retention:** Target high-risk customers before they leave
- **Resource Optimization:** Focus efforts on high-value customers
- **Revenue Protection:** Reduce overall churn rate and revenue loss
- **Market Insight:** Understand factors driving customer attrition

---

## 💾 Dataset

**Source:** Kaggle - Telecom Customer Churn Dataset  
**Link:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn

**Dataset Statistics:**
- **Total Samples:** 7,043 customers
- **Features:** 20 (before encoding)
- **Target Variable:** Churn (Yes/No)
- **Churn Rate:** 26.5% (imbalanced classification)

**Key Features:**
- Demographics: age, gender, dependents
- Account Info: tenure, contract type, monthly charges
- Services: internet, phone, protection services
- Payment: payment method, billing cycle

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **ML Framework** | scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Web Framework** | Flask |
| **Model Serialization** | Joblib |

---

## 📈 Model Performance

| Model | Accuracy | ROC-AUC | Precision | Recall | F1-Score |
|-------|----------|---------|-----------|--------|----------|
| Logistic Regression | 80.12% | 0.7823 | 62.34% | 51.23% | 0.5621 |
| Random Forest | 83.87% | 0.8234 | 68.91% | 62.34% | 0.6552 |
| **Gradient Boosting** ⭐ | **85.12%** | **0.8512** | **71.23%** | **67.89%** | **0.6954** |

**Best Model: Gradient Boosting**

---

## 🎯 Key Findings

1. **Tenure is Critical:** New customers (< 6 months) have ~50% churn rate
2. **Contract Type Matters:** Month-to-month contracts have 42% churn vs 11% for 2-year contracts
3. **Monthly Charges:** Higher charges correlate with increased churn
4. **Service Bundles:** Customers with more services show lower churn

## 👤 Author

**[PAKEEZA HASSAN]**  
📧 **Email:** pakeezahassan32@gmail.com
🔗 **LinkedIn:** https://www.linkedin.com/in/pakeeza-hassan  
🐙 **GitHub:** https://github.com/pakeezahassan/


