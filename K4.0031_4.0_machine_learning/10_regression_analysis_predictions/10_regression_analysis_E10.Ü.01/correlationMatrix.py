import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(0)

data = {
    "CRIM": np.random.rand(100),
    "ZN": np.random.rand(100) * 100,
    "INDUS": np.random.rand(100) * 25,
    "NOX": np.random.rand(100),
    "RM": np.random.rand(100) * 10,
    "AGE": np.random.rand(100) * 100,
    "DIS": np.random.rand(100) * 10,
    "RAD": np.random.randint(1, 10, 100),
    "TAX": np.random.randint(200, 700, 100),
    "PTRATIO": np.random.rand(100) * 20,
}

df = pd.DataFrame(data)

corr_matrix = df.corr(method="pearson")

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.show()
