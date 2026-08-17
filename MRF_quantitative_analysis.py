import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# PAPER 2 DATA
# ------------------------------------------------------------

data = {
    "magnetic_induction_T": [0.23, 0.44, 0.65, 0.86],
    "yield_stress_Pa": [1369, 3703, 6491, 8825]
}

df = pd.DataFrame(data)

print("=" * 60)
print("MR FLUID QUANTITATIVE ANALYSIS")
print("=" * 60)

print("\nDataset:")
print(df)

# ------------------------------------------------------------
# LINEAR FIT
# ------------------------------------------------------------

x = df["magnetic_induction_T"]
y = df["yield_stress_Pa"]

slope, intercept = np.polyfit(x, y, 1)

predicted = slope * x + intercept

# R squared
ss_res = np.sum((y - predicted) ** 2)
ss_tot = np.sum((y - y.mean()) ** 2)

r_squared = 1 - (ss_res / ss_tot)

print("\nLinear relationship:")
print("Yield stress =", round(slope, 2), "* B +", round(intercept, 2))

print("\nSlope:")
print(round(slope, 2), "Pa/T")

print("\nIntercept:")
print(round(intercept, 2), "Pa")

print("\nR²:")
print(round(r_squared, 4))

# ------------------------------------------------------------
# PERCENTAGE INCREASE
# ------------------------------------------------------------

percentage_increase = (
    (y.iloc[-1] - y.iloc[0])
    / y.iloc[0]
) * 100

print("\nPercentage increase in yield stress:")
print(round(percentage_increase, 2), "%")

# ------------------------------------------------------------
# GRAPH
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    x,
    y,
    label="Experimental data"
)

plt.plot(
    x,
    predicted,
    label="Linear fit"
)

plt.xlabel("Magnetic induction, B (T)")
plt.ylabel("Yield stress, τy (Pa)")
plt.title("Magnetic Induction vs Yield Stress")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "mrf_magnetic_induction_vs_yield_stress_quantitative.png",
    dpi=300
)

plt.show()

print("\nAnalysis completed.")