# Regression Metrics Summary

| Metric | Full Form / Meaning | Formula Idea | Range | Higher or Lower Better? | Main Use | Important Notes |
|---|---|---|---|---|---|---|
| **MAE** | Mean Absolute Error | Average of absolute errors | 0 to ∞ | Lower | Measures average prediction error | Easy to understand. Less sensitive to outliers. |
| **MSE** | Mean Squared Error | Average of squared errors | 0 to ∞ | Lower | Penalizes large errors heavily | Useful when big mistakes are very bad. |
| **RMSE** | Root Mean Squared Error | Square root of MSE | 0 to ∞ | Lower | Most commonly used regression error metric | Same unit as target variable, easier to interpret than MSE. |
| **R²** | Coefficient of Determination | Variance explained by model | Usually 0 to 1 | Higher | Measures goodness of fit | Increases when predictors are added, even useless ones. |
| **Adjusted R²** | Adjusted Coefficient of Determination | Adjusted version of R² | Usually 0 to 1 | Higher | Evaluates model while considering number of predictors | Penalizes unnecessary predictors. Better for multiple regression comparison. |
| **MAPE** | Mean Absolute Percentage Error | Average percentage error | 0% to ∞ | Lower | Error in percentage form | Cannot handle actual values near zero properly. |
| **Explained Variance Score** | Variance explained by predictions | Similar to R² | ≤ 1 | Higher | Measures variance captured | Less commonly used than R². |
| **Median Absolute Error** | Median of absolute errors | Median instead of average | 0 to ∞ | Lower | Robust error measurement | Very resistant to outliers. |

---

# When to Use Which Metric

| Situation | Best Metric | Why |
|---|---|---|
| Want simple average error | MAE | Easy interpretation |
| Large errors are very dangerous | MSE / RMSE | Squaring punishes large errors |
| Need error in original unit | RMSE | Example: “Average error is 5 rupees” |
| Comparing regression models | Adjusted R² | Considers unnecessary predictors |
| Need percentage-based error | MAPE | Easy for business reporting |
| Dataset has many outliers | MAE / Median Absolute Error | Less affected by extreme values |
| Want goodness-of-fit score | R² | Shows how much variance is explained |

---

# MAE vs MSE vs RMSE

| Metric | Outlier Sensitivity | Interpretation |
|---|---|---|
| MAE | Low | Average absolute mistake |
| MSE | Very High | Strongly punishes large errors |
| RMSE | High | Like MSE but easier to interpret |

### Example

Errors = [2, 3, 100]

- MAE treats all errors linearly.
- MSE/RMSE heavily punish the 100 error.

---

# R² vs Adjusted R²

| Metric | Problem | Solution |
|---|---|---|
| R² | Always increases with more predictors | Can falsely suggest improvement |
| Adjusted R² | Penalizes unnecessary predictors | Better for model selection |

---

# Quick Memory Trick

| Metric Type | Focus |
|---|---|
| MAE | Average mistake |
| MSE | Punish large mistakes |
| RMSE | Practical large-error metric |
| R² | Fit quality |
| Adjusted R² | Fit quality + model simplicity |
| MAPE | Percentage error |

---

# Recommended Practical Usage

| Real-world Scenario | Common Choice |
|---|---|
| ML competitions | RMSE |
| Business dashboards | MAE or MAPE |
| Academic regression analysis | R² + Adjusted R² |
| Financial risk models | RMSE |
| Noisy datasets | MAE |

---

# Important Interview Line

> “MAE is robust to outliers, MSE/RMSE penalize large errors, and Adjusted R² helps prevent overfitting by penalizing unnecessary predictors.”