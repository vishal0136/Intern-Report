"""Week 1: illustrative risk scoring. Synthetic scenarios only."""
import pandas as pd

df = pd.read_csv("risk_register.csv")
df["risk_score"] = df["Likelihood_1_5"] * df["Impact_1_5"]
def band(score):
    if score >= 15: return "High"
    if score >= 8: return "Medium"
    return "Low"
df["calculated_band"] = df["risk_score"].map(band)
print(df[["Threat", "risk_score", "calculated_band", "Recommended_Control"]]
      .sort_values("risk_score", ascending=False).to_string(index=False))
df.to_csv("risk_register_scored.csv", index=False)
