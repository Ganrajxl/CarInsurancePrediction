# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 22:41:23 2026

@author: USER
"""

import pandas as pd
import numpy as np

# number of rows
rows = 5000

np.random.seed(42)

data = {
    "Age": np.random.randint(18, 70, rows),
    "Credit_Score": np.random.randint(300, 850, rows),
    "Annual_Mileage": np.random.randint(5000, 30000, rows),
    "Vehicle_Ownership": np.random.randint(0, 2, rows),
    "Vehicle_Year": np.random.randint(2000, 2024, rows),
    "Speeding_Violations": np.random.randint(0, 10, rows),
}

df = pd.DataFrame(data)

# Create claim column based on some risk conditions
df["Claim"] = (
    (df["Credit_Score"] < 600) |
    (df["Speeding_Violations"] > 5) |
    (df["Annual_Mileage"] > 20000)
).astype(int)

# Save dataset
df.to_csv("insurance.csv", index=False)

print("Dataset Created Successfully")