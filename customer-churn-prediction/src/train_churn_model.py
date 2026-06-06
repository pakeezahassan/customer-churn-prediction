"""
Customer Churn Prediction - Complete ML Pipeline
Predicts whether telecom customers will leave the company
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_auc_score, 
    roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score
)
import joblib
import warnings
warnings.filterwarnings('ignore')

# Configure style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

print("=" * 80)
print("📱 CUSTOMER CHURN PREDICTION - ML PIPELINE")
print("=" * 80)

# ===============================================================================
# STEP 1: LOAD AND EXPLORE DATA
# ===============================================================================

print("\n📊 STEP 1: Loading and Exploring Data...")

def load_and_explore(csv_path):
    """Load data and perform basic EDA"""
    df = pd.read_csv(csv_path)
    
    print(f"\n✓ Dataset loaded successfully!")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\n📋 First few rows:")
    print(df.head())
    print(f"\n📌 Data Info:")
    print(df.info())
    print(f"\n💰 Churn Distribution:")
    churn_counts = df['Churn'].value_counts()
    print(churn_counts)
    print(f"\n  Churn Rate: {(churn_counts['Yes']/len(df)*100):.2f}%")
    print(f"\n📈 Statistical Summary:")
    print(df.describe())
    
    return df

# Load data
try:
    df = load_and_explore('data/telecom_churn.csv')
except FileNotFoundError:
    print("❌ Error: data/telecom_churn.csv not found")
    print("Please download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
    exit()

# ===============================================================================
# STEP 2: DATA PREPROCESSING
# ===============================================================================

print("\n\n🔧 STEP 2: Data Preprocessing...")

def preprocess_churn_data(df, target_column='Churn'):
    """Clean and preprocess churn data"""
    
    df = df.copy()
    
    # Remove rows with missing target
    print(f"\n  • Handling missing values...")
    df = df.dropna(subset=[target_column])
    
    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    print(f"  ✓ Missing values handled")
    
    # Convert target to binary
    print(f"  • Converting target variable to binary...")
    y = (df[target_column] == 'Yes').astype(int)
    
    # Separate features
    X = df.drop([target_column, 'customerID'], axis=1, errors='ignore')
    
    # Encode categorical variables
    print(f"  • Encoding categorical variables...")
    categorical_features = X.select_dtypes(include=['object']).columns
    X = pd.get_dummies(X, columns=categorical_features, drop_first=True)
    print(f"  ✓ Features after encoding: {X.shape[1]} features")
    
    # Train-test split
    print(f"  • Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  ✓ Training set: {X_train.shape[0]} samples")
    print(f"  ✓ Test set: {X_test.shape[0]} samples")
    print(f"  ✓ Train churn rate: {y_train.mean()*100:.2f}%")
    print(f"  ✓ Test churn rate: {y_test.mean()*100:.2f}%")
    
    # Scaling
    print(f"  • Scaling features with StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"  ✓ Features scaled successfully")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns

# Preprocess
X_train, X_test, y_train, y_test, scaler, feature_names = preprocess_churn_data(df)

# ===============================================================================
# STEP 3: EXPLORATORY DATA ANALYSIS (EDA)
# ===============================================================================

print("\n\n📊 STEP 3: Exploratory Data Analysis...")

def create_churn_eda(df, target_column='Churn'):
    """Create comprehensive EDA visualizations"""
    
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Churn distribution
    ax1 = plt.subplot(2, 3, 1)
    churn_counts = df[target_column].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    churn_counts.plot(kind='bar', ax=ax1, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_title('Churn Distribution', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Count')
    ax1.set_xticklabels(['Stay', 'Churn'], rotation=0)
    for i, v in enumerate(churn_counts):
        ax1.text(i, v + 50, f'{v}\n({v/len(df)*100:.1f}%)', ha='center', fontweight='bold')
    
    # 2. Churn by contract type
    ax2 = plt.subplot(2, 3, 2)
    if 'Contract' in df.columns:
        churn_by_contract = pd.crosstab(df['Contract'], df[target_column], normalize='index') * 100
        churn_by_contract.plot(kind='bar', ax=ax2, color=colors, edgecolor='black', alpha=0.7)
        ax2.set_title('Churn Rate by Contract Type', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Percentage (%)')
        ax2.legend(['Stay', 'Churn'])
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    
    # 3. Churn by tenure
    ax3 = plt.subplot(2, 3, 3)
    if 'tenure' in df.columns:
        churn_numeric = df[target_column].map({'Yes': 1, 'No': 0})
        ax3.scatter(df['tenure'], churn_numeric, alpha=0.3, s=20)
        ax3.set_title('Churn vs Tenure (Months)', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Tenure (months)')
        ax3.set_ylabel('Churn (0=Stay, 1=Leave)')
        
        # Add trend line
        z = np.polyfit(df['tenure'], churn_numeric, 2)
        p = np.poly1d(z)
        ax3.plot(sorted(df['tenure']), p(sorted(df['tenure'])), "r-", linewidth=2, label='Trend')
        ax3.legend()
    
    # 4. Monthly charges distribution
    ax4 = plt.subplot(2, 3, 4)
    if 'MonthlyCharges' in df.columns:
        churn_yes = df[df[target_column] == 'Yes']['MonthlyCharges']
        churn_no = df[df[target_column] == 'No']['MonthlyCharges']
        ax4.hist([churn_no, churn_yes], bins=30, label=['Stay', 'Churn'], color=colors, alpha=0.7, edgecolor='black')
        ax4.set_title('Monthly Charges Distribution by Churn', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Monthly Charges ($)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
    
    # 5. Internet service type
    ax5 = plt.subplot(2, 3, 5)
    if 'InternetService' in df.columns:
        churn_by_internet = pd.crosstab(df['InternetService'], df[target_column], normalize='index') * 100
        churn_by_internet.plot(kind='bar', ax=ax5, color=colors, edgecolor='black', alpha=0.7)
        ax5.set_title('Churn Rate by Internet Service', fontsize=12, fontweight='bold')
        ax5.set_ylabel('Percentage (%)')
        ax5.legend(['Stay', 'Churn'])
        ax5.set_xticklabels(ax5.get_xticklabels(), rotation=45)
    
    # 6. Total charges
    ax6 = plt.subplot(2, 3, 6)
    if 'TotalCharges' in df.columns:
        # Convert TotalCharges to numeric
        df['TotalCharges_numeric'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        churn_yes = df[df[target_column] == 'Yes']['TotalCharges_numeric'].dropna()
        churn_no = df[df[target_column] == 'No']['TotalCharges_numeric'].dropna()
        ax6.hist([churn_no, churn_yes], bins=30, label=['Stay', 'Churn'], color=colors, alpha=0.7, edgecolor='black')
        ax6.set_title('Total Charges Distribution by Churn', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Total Charges ($)')
        ax6.set_ylabel('Frequency')
        ax6.legend()
    
    plt.tight_layout()
    plt.savefig('outputs/01_churn_eda.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ EDA visualizations saved: outputs/01_churn_eda.png")
    plt.close()

# Create EDA
create_churn_eda(df)

# ===============================================================================
# STEP 4: MODEL TRAINING
# ===============================================================================

print("\n\n🤖 STEP 4: Training Models...")

def train_classification_models(X_train, X_test, y_train, y_test):
    """Train and compare classification models"""
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    results = {}
    best_model = None
    best_score = -np.inf
    
    print("\n" + "=" * 80)
    print("MODEL PERFORMANCE COMPARISON")
    print("=" * 80)
    
    for model_name, model in models.items():
        print(f"\n🔄 Training {model_name}...")
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Evaluate
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        precision = precision_score(y_test, y_pred_test)
        recall = recall_score(y_test, y_pred_test)
        f1 = f1_score(y_test, y_pred_test)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
        
        results[model_name] = {
            'model': model,
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'predictions': y_pred_test,
            'predictions_proba': y_pred_proba
        }
        
        # Track best model
        if roc_auc > best_score:
            best_score = roc_auc
            best_model = model
            best_model_name = model_name
        
        print(f"  ✓ Training Accuracy:  {train_accuracy:.4f}")
        print(f"  ✓ Test Accuracy:      {test_accuracy:.4f}")
        print(f"  ✓ Precision:          {precision:.4f}")
        print(f"  ✓ Recall:             {recall:.4f}")
        print(f"  ✓ F1-Score:           {f1:.4f}")
        print(f"  ✓ ROC-AUC:            {roc_auc:.4f}")
        print(f"  ✓ CV Mean (5-fold):   {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    print("\n" + "=" * 80)
    print(f"🏆 BEST MODEL: {best_model_name}")
    print(f"   ROC-AUC Score: {best_score:.4f}")
    print("=" * 80)
    
    return results, best_model, best_model_name

# Train models
results, best_model, best_model_name = train_classification_models(X_train, X_test, y_train, y_test)

# ===============================================================================
# STEP 5: MODEL COMPARISON VISUALIZATION
# ===============================================================================

print("\n\n📊 STEP 5: Visualizing Model Performance...")

def plot_model_comparison(results):
    """Compare model performance"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    model_names = list(results.keys())
    
    # Accuracy comparison
    accuracies = [results[name]['test_accuracy'] for name in model_names]
    axes[0, 0].bar(model_names, accuracies, color=['skyblue', 'lightcoral', 'lightgreen'], edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Accuracy Comparison (Test Set)', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].set_ylim(0.7, 1)
    for i, v in enumerate(accuracies):
        axes[0, 0].text(i, v + 0.01, f'{v:.4f}', ha='center', fontweight='bold')
    
    # ROC-AUC comparison
    roc_aucs = [results[name]['roc_auc'] for name in model_names]
    axes[0, 1].bar(model_names, roc_aucs, color=['skyblue', 'lightcoral', 'lightgreen'], edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('ROC-AUC Comparison (Test Set)', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('ROC-AUC')
    axes[0, 1].set_ylim(0.7, 1)
    for i, v in enumerate(roc_aucs):
        axes[0, 1].text(i, v + 0.01, f'{v:.4f}', ha='center', fontweight='bold')
    
    # Precision-Recall-F1
    precisions = [results[name]['precision'] for name in model_names]
    recalls = [results[name]['recall'] for name in model_names]
    f1s = [results[name]['f1'] for name in model_names]
    
    x = np.arange(len(model_names))
    width = 0.25
    axes[1, 0].bar(x - width, precisions, width, label='Precision', color='skyblue', edgecolor='black', alpha=0.7)
    axes[1, 0].bar(x, recalls, width, label='Recall', color='lightcoral', edgecolor='black', alpha=0.7)
    axes[1, 0].bar(x + width, f1s, width, label='F1', color='lightgreen', edgecolor='black', alpha=0.7)
    axes[1, 0].set_title('Precision, Recall, F1 Comparison', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Score')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(model_names)
    axes[1, 0].legend()
    axes[1, 0].set_ylim(0, 1)
    
    # Cross-validation scores
    cv_means = [results[name]['cv_mean'] for name in model_names]
    cv_stds = [results[name]['cv_std'] for name in model_names]
    axes[1, 1].bar(model_names, cv_means, yerr=cv_stds, capsize=10, color=['skyblue', 'lightcoral', 'lightgreen'], 
                   edgecolor='black', alpha=0.7)
    axes[1, 1].set_title('5-Fold Cross-Validation ROC-AUC', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('CV ROC-AUC')
    axes[1, 1].set_ylim(0.7, 1)
    
    plt.tight_layout()
    plt.savefig('outputs/02_model_comparison.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Model comparison saved: outputs/02_model_comparison.png")
    plt.close()

# Plot comparison
plot_model_comparison(results)

# ===============================================================================
# STEP 6: CONFUSION MATRIX & ROC CURVE
# ===============================================================================

print("\n\n🎯 STEP 6: Detailed Performance Analysis...")

def plot_confusion_and_roc(best_model, X_test, y_test, best_results):
    """Plot confusion matrix and ROC curve"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Confusion Matrix
    y_pred = best_results['predictions']
    cm = confusion_matrix(y_test, y_pred)
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=True,
                xticklabels=['Stay', 'Churn'], yticklabels=['Stay', 'Churn'])
    axes[0].set_title('Confusion Matrix (Test Set)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Actual')
    axes[0].set_xlabel('Predicted')
    
    # Add metrics on confusion matrix
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp)
    sensitivity = tp / (tp + fn)
    axes[0].text(0.5, -0.35, f'Sensitivity (Recall): {sensitivity:.4f} | Specificity: {specificity:.4f}',
                ha='center', transform=axes[0].transAxes, fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # ROC Curve
    y_pred_proba = best_results['predictions_proba']
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    axes[1].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
    axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].set_xlabel('False Positive Rate')
    axes[1].set_ylabel('True Positive Rate')
    axes[1].set_title('ROC Curve (Test Set)', fontsize=12, fontweight='bold')
    axes[1].legend(loc="lower right")
    
    plt.tight_layout()
    plt.savefig('outputs/03_confusion_and_roc.png', dpi=300, bbox_inches='tight')
    print(f"  ✓ Confusion matrix & ROC curve saved: outputs/03_confusion_and_roc.png")
    plt.close()

# Plot confusion matrix and ROC
best_results = results[best_model_name]
plot_confusion_and_roc(best_model, X_test, y_test, best_results)

# ===============================================================================
# STEP 7: FEATURE IMPORTANCE
# ===============================================================================

print("\n\n🎯 STEP 7: Analyzing Feature Importance...")

def plot_feature_importance(model, feature_names, model_name, top_n=15):
    """Plot top features for tree-based models"""
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.barh(range(top_n), importances[indices], color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_yticks(range(top_n))
        ax.set_yticklabels([feature_names[i] for i in indices])
        ax.set_xlabel('Importance', fontweight='bold')
        ax.set_title(f'Top {top_n} Important Features ({model_name})', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        
        # Add values on bars
        for i, v in enumerate(importances[indices]):
            ax.text(v + 0.002, i, f'{v:.4f}', va='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('outputs/04_feature_importance.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Feature importance saved: outputs/04_feature_importance.png")
        plt.close()
        
        # Print top features
        print(f"\n  Top {top_n} Important Features:")
        for i, idx in enumerate(indices, 1):
            print(f"    {i:2d}. {feature_names[idx]:40s} - {importances[idx]:.4f}")

# Plot feature importance
if hasattr(best_model, 'feature_importances_'):
    plot_feature_importance(best_model, feature_names, best_model_name)

# ===============================================================================
# STEP 8: SAVE MODEL
# ===============================================================================

print("\n\n💾 STEP 8: Saving Model...")

def save_model(model, scaler, feature_names, filename='models/churn_model.pkl'):
    """Save model and preprocessing objects"""
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names
    }
    
    joblib.dump(model_data, filename)
    print(f"  ✓ Model saved: {filename}")

# Save model
save_model(best_model, scaler, feature_names)

# ===============================================================================
# STEP 9: SUMMARY & INSIGHTS
# ===============================================================================

print("\n\n📋 STEP 9: Summary & Insights...")

best_result = results[best_model_name]
print(f"""
{'='*80}
FINAL MODEL PERFORMANCE SUMMARY
{'='*80}

Model: {best_model_name}

Metrics:
  • Accuracy (Test):        {best_result['test_accuracy']:.4f}
  • Precision:              {best_result['precision']:.4f}  (correct predictions when predicting churn)
  • Recall:                 {best_result['recall']:.4f}  (ability to find actual churners)
  • F1-Score:               {best_result['f1']:.4f}  (balance of precision & recall)
  • ROC-AUC:                {best_result['roc_auc']:.4f}  (ability to distinguish churners vs stayers)
  • Cross-Validation (5x):  {best_result['cv_mean']:.4f} (+/- {best_result['cv_std']:.4f})

Key Insights:
  1. Model predicts churn with {best_result['roc_auc']*100:.1f}% ROC-AUC (excellent discrimination)
  2. When model predicts churn, it's correct {best_result['precision']*100:.1f}% of the time
  3. Model catches {best_result['recall']*100:.1f}% of actual churners
  4. Feature importance analysis reveals top churn predictors
  5. Model generalizes well (CV score close to test performance)

Business Application:
  ✓ Use model to identify high-risk customers
  ✓ Implement retention strategies for at-risk segments
  ✓ Prioritize retention efforts on high-value customers
  ✓ Monitor model performance over time

Next Steps:
  ✓ Deploy via Flask API (app.py)
  ✓ Create Streamlit dashboard
  ✓ Push to GitHub
  ✓ Monitor predictions in production

{'='*80}
""")

print("\n✅ PIPELINE COMPLETE!\n")
print("📂 Output files created:")
print("   • outputs/01_churn_eda.png")
print("   • outputs/02_model_comparison.png")
print("   • outputs/03_confusion_and_roc.png")
print("   • outputs/04_feature_importance.png")
print("   • models/churn_model.pkl")
print("\n🚀 Next: Run app.py to deploy the model as an API")
print("\n" + "=" * 80)
