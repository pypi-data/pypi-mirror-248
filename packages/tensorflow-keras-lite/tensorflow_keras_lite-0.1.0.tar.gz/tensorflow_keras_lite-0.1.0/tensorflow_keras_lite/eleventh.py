def print_prog():
    print(
        """
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import ParameterEstimator, MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import pydot
import matplotlib.pyplot as plt
import networkx as nx

# # Load the Heart Disease dataset
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
names = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
data = pd.read_csv('/kaggle/input/ann-lab-dataset/processed_cleveland.csv', names=names, na_values="?")
# data = pd.read_csv(url, names=names, na_values="?")

# Drop rows with missing values
data = data.dropna()

# Define Bayesian Network Structure with consistent variable names
model = BayesianNetwork([
    ('age', 'trestbps'), ('age', 'fbs'), ('sex', 'trestbps'), ('sex', 'trestbps'),
    ('exang', 'trestbps'), ('trestbps', 'target'), ('fbs', 'target'),
    ('target', 'restecg'), ('target', 'thalach'), ('target', 'chol')
])

# Parameter Estimation
model.fit(data, estimator=MaximumLikelihoodEstimator)
print(model.edges())
# Print CPDs
# for cpd in model.get_cpds():
#     print('CPDs: ')
#     print(cpd)
# Visualize the Bayesian Network
plt.figure(figsize=(12, 8))

pos = nx.circular_layout(model)
nx.draw(model, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, arrowsize=20)

plt.show()

plt.show()

# Perform Inference
inference = VariableElimination(model)
predicted_values = inference.map_query(variables=['target'], evidence={'age': 28, 'sex': 1, 'trestbps': 200})
print("Predicted Heart Disease:", predicted_values['target'])"""
    )
