"""Week 5: summarize hypothetical security control gaps."""
import pandas as pd

df = pd.read_csv("hypothetical_control_assessment.csv")
# Priority heuristic: lower maturity and higher impact increase the score.
df["priority_score"] = (6 - df["Maturity_1_5"]) * df["Impact_1_5"]
df = df.sort_values(["priority_score", "Impact_1_5"], ascending=False)
print(df[["Control_Area","Maturity_1_5","Impact_1_5","priority_score"]].to_string(index=False))
df.to_csv("prioritized_control_gaps.csv", index=False)
