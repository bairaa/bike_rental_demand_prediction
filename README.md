# 🚲 Bike Rental Demand Prediction

## 📋 Project Overview

Capital Bikeshare operates more than **8,000 bicycles across over 800 stations**, creating a complex operational challenge. Without accurate demand prediction, the company faces:

- **Bike shortages** during high-demand periods → customer dissatisfaction & revenue loss
- **Excess idle bikes** during low-demand periods → wasted maintenance costs & inefficiencies

This project develops a machine learning model to predict hourly bike rental demand, enabling data-driven decisions for inventory optimization and cost reduction.

---

## 🎯 Business Objectives

| Objective | Description |
|-----------|-------------|
| **Predict demand patterns** | Forecast hourly bike rentals to support station management |
| **Improve bike availability** | Reduce unmet demand during peak hours |
| **Optimize redistribution** | Schedule maintenance and redistribution efficiently |
| **Drive data-driven decisions** | Provide actionable insights for operations and expansion |

---

## 📊 Dataset Overview

**Source**: Capital Bikeshare historical data (2011–2012)  
**Records**: 12,165 hourly observations  
**Target variable**: `cnt` (total hourly bike rentals)

### Key Features:

| Feature | Description |
|---------|-------------|
| `hr` | Hour of day (0–23) |
| `temp` | Normalized temperature |
| `hum` | Normalized humidity |
| `weathersit` | Weather condition (1:Clear, 2:Mist, 3:Light rain/snow, 4:Heavy rain) |
| `season` | Season (1:Spring, 2:Summer, 3:Fall, 4:Winter) |
| `day_of_week` | Day (0:Monday – 6:Sunday) |
| `holiday` | Holiday indicator |

---

## 🔍 Exploratory Data Analysis

### Key Insights:

**1. Demand Patterns**
- **Peak hours**: 8 AM (morning commute) and 5–7 PM (evening commute)
- **Peak season**: Fall (highest demand), followed by Summer
- **Lowest demand**: Winter and early Spring

**2. Weather Impact**
- **Clear weather**: Highest rental counts
- **Heavy rain**: Drastically reduces demand
- **Temperature**: Strong positive correlation with rentals

**3. User Behavior**
- **Registered users**: Primary drivers of weekday demand (commuters)
- **Casual users**: Peak on weekends (recreational)

---

## 🧠 Modeling Approach

### Models Evaluated

| Model | RMSE | MAE | R² |
|-------|------|-----|-----|
| KNN | 114.68 | 76.03 | 0.603 |
| Decision Tree | 98.95 | 62.17 | 0.704 |
| Random Forest | 73.78 | 48.43 | 0.835 |
| Extra Trees | 75.93 | 49.56 | 0.826 |
| AdaBoost | 121.23 | 95.84 | 0.556 |
| Gradient Boosting | 93.11 | 63.54 | 0.739 |
| **XGBoost** | **70.55** | **47.65** | **0.850** |
| LightGBM | 70.16 | 47.31 | 0.851 |

### ✅ Model Selection: **XGBoost**
- Selected for best balance of accuracy and interpretability
- Hyperparameter tuning via RandomizedSearchCV with 5-fold cross-validation

---

## 📈 Final Model Performance

### Test Set Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **RMSE** | 67.85 | Average prediction error (higher weight on large errors) |
| **MAE** | **45.21** | Average hourly error of ~45 bikes |
| **MAPE** | 54.82% | Percentage error (higher at low-demand hours) |
| **R²** | **0.852** | Model explains 85.2% of demand variance |

### Error Analysis

- **44.8% underestimations**, **55.2% overestimations** → well-balanced
- Most errors cluster near zero (normally distributed)
- Model performs best during mid-range demand hours
- Some limitations during extreme high-demand spikes

### Feature Importance (SHAP Analysis)

| Feature | Importance |
|---------|------------|
| **hr** (hour) | ⭐⭐⭐ Highest impact |
| **temp** | ⭐⭐ Strong impact |
| **day_of_week** | ⭐⭐ Moderate impact |
| **hum** | ⭐ Minor impact |
| **weathersit** | ⭐ Minor impact |
| **season** | ⭐ Minor impact |

**Conclusion**: Rental demand is primarily driven by **time-based patterns** (hour, day) and **temperature**, confirming that commuting behavior and weather comfort are the strongest predictors.

---

## 💰 Business Impact & Cost-Benefit Analysis

### Cost Assumptions

| Scenario | Cost per Bike | Description |
|----------|---------------|-------------|
| **Underestimation** | $4.00 | Lost revenue + customer dissatisfaction |
| **Overestimation** | $1.50 | Extra redistribution & maintenance costs |

### Financial Projections

| Metric | XGBoost Model | Baseline (MAE = 60) |
|--------|---------------|---------------------|
| Hourly expected loss | **$117.90** | $157.20 |
| Monthly loss | **$84,900** | $113,190 |
| **Monthly savings** | **$28,290** | — |
| **Annual savings** | **$339,480** | — |

> 💡 **Business Value**: Deploying the XGBoost model is projected to save **~$340,000 annually** compared to a non-ML baseline approach.

---

## 📋 Actionable Recommendations

### 1. Dynamic Inventory Management

| Time Period | Demand Category | Operational Action |
|-------------|-----------------|---------------------|
| 07:00–09:00 | **Rush Hour** | Max bike availability at commuter hubs |
| 08:00 | **Peak Rush** | Highest priority staffing |
| 11:00–12:00 | Lunch Break | Monitor short-distance trips |
| 15:00–17:00 | **Evening Rush** | Prepare for return commute |
| 18:00–23:00 | Off-Peak | Schedule maintenance & redistribution |

### 2. Predictive Planning Using Demand Thresholds

| Demand Level | Predicted Rentals | Operational Response |
|--------------|-------------------|----------------------|
| **Low** | ≤ 40 | Minimal redistribution; focus on maintenance |
| **Moderate** | 41–242 | Standard operations |
| **High** | 243–645 | Increase redistribution frequency |
| **Very High** | > 645 | Activate surge protocols; deploy all available bikes |

### 3. Targeted Marketing Strategies

| User Segment | Strategy |
|--------------|----------|
| **Registered Users** (retention) | Offer loyalty programs & annual subscription discounts, especially before winter |
| **Casual Users** (acquisition) | Launch summer/fall campaigns with weekend rental packages & tourist route discounts |

---

## 🛠️ Technical Implementation

### Model Artifact

```python
artifact = {
    "model": tuned_xgboost_model,
    "threshold_config": {
        "low_percentile": 0.25,
        "mid_percentile": 0.50,
        "high_percentile": 0.75
    },
    "training_stats": {
        "q1": 40,
        "median": 142,
        "q3": 242
    },
    "features": ["hr", "temp", "hum", "weathersit", "day_of_week", "season", "holiday"]
}
```
---

## 📊 Conclusion

The XGBoost model delivers **strong predictive performance** with **85.2% accuracy** (R²) and a **Mean Absolute Error of 45 bikes per hour**. This translates to an estimated **$340,000 in annual savings** through improved demand forecasting.

Key business takeaways:
- **Rush hour demand** requires proactive bike positioning
- **Weather-aware planning** reduces operational waste
- **Dynamic thresholds** ensure relevance as demand patterns evolve
- **Segmented marketing** maximizes user retention and acquisition

With proper deployment and periodic retraining, this model serves as a **robust decision-support tool** for optimizing bike rental operations and enhancing customer satisfaction.

---


## 🙏 Acknowledgments

- Capital Bikeshare for providing public dataset
- Scikit-learn & XGBoost communities for excellent documentation
```
