def print_prog():
    print(
        """
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import fetch_openml
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_auc_score
# Load the pulsar_stars dataset
import pandas as pd
df = pd.read_csv('/kaggle/input/ann-lab-dataset/pulsar_stars.csv')
X, y = df.iloc[:, :-1].values, df.iloc[:, -1].values
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)
# Support Vector Machine
start_time_svm = time.time()
clf_svm = SVC(kernel='linear', probability=True)
clf_svm.fit(X_train, y_train)
y_pred_svm = clf_svm.predict(X_test)
end_time_svm = time.time()
svm_accuracy = accuracy_score(y_test, y_pred_svm)
svm_time = end_time_svm - start_time_svm
# Neural Network
start_time_nn = time.time()
clf_nn = MLPClassifier(hidden_layer_sizes=(50,), max_iter=1000, random_state=42)
clf_nn.fit(X_train, y_train)
y_pred_nn = clf_nn.predict(X_test)
end_time_nn = time.time()
nn_accuracy = accuracy_score(y_test, y_pred_nn)
nn_time = end_time_nn - start_time_nn
# Plotting
labels = ['SVM', 'Neural Network']
accuracies = [svm_accuracy, nn_accuracy]
times = [svm_time, nn_time]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
# Accuracy Comparison
ax1.bar(labels, accuracies, color=['blue', 'orange'])
ax1.set_ylabel('Accuracy')
ax1.set_title('Accuracy Comparison')
# Time Comparison
ax2.bar(labels, times, color=['green', 'red'])
ax2.set_ylabel('Training Time (seconds)')
ax2.set_title('Training Time Comparison')
plt.tight_layout()
# Plot ROC Curve
plt.figure(figsize=(8, 6))
# SVM ROC Curve
y_score_svm = clf_svm.predict_proba(X_test)[:, 1]
fpr_svm, tpr_svm, _ = roc_curve(y_test, y_score_svm)
roc_auc_svm = auc(fpr_svm, tpr_svm)
plt.plot(fpr_svm, tpr_svm, color='blue', lw=2, label=f'SVM (AUC ={roc_auc_svm:.2f})')
# Neural Network ROC Curve
y_score_nn = clf_nn.predict_proba(X_test)[:, 1]
fpr_nn, tpr_nn, _ = roc_curve(y_test, y_score_nn)
roc_auc_nn = auc(fpr_nn, tpr_nn)
plt.plot(fpr_nn, tpr_nn, color='orange', lw=2, label=f'Neural Network (AUC = {roc_auc_nn:.2f})')
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()"""
    )
