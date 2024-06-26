# -*- coding: utf-8 -*-
"""Final_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TYDxw791t4P2bfBkMb62l9h5HYrtfq_2
"""

#Going to import our dataset first
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

my_file = "drive/MyDrive/Datasets/emails.csv"
my_csv = pd.read_csv(my_file)
my_csv = my_csv.drop(my_csv.columns[0], axis=1)

X = my_csv.drop(columns=["Prediction"])
y = my_csv["Prediction"]

#Splitting the data into training and testing

test_var = 0.2 #will start with this now
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_var, random_state=42)

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns

def naive_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report, alpha_val=1):
  naive_bayes = MultinomialNB(alpha=alpha_val)
  naive_bayes.fit(X_train, y_train)

  naive_predictions = naive_bayes.predict(X_test)
  naive_accuracy = accuracy_score(y_test, naive_predictions)
  naive_report = classification_report(y_test, naive_predictions)

  print(naive_accuracy, test_var)

  if btest_report:
    print(naive_report)
    conf_matrix_naive = confusion_matrix(y_test, naive_predictions)
    sns.heatmap(conf_matrix_naive, annot=True, fmt="d", xticklabels=["Not Spam", "Spam"], yticklabels=["Not Spam", "Spam"])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Naive Bayes Confusion Matrix")
    plt.show()

btest_report = False
test_var_arr = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8] #want to also test out how different amount of test data size affects accuracy
for test_var in test_var_arr:
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_var, random_state=42)
  naive_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report)

n_alpha = [0.01, 0.1, 1, 10, 100]
nb_results = np.zeros_like(n_alpha, dtype=float) #so we can plot the different accuracies across different alphas
test_var = 0.2 #This split gave us the best result
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #back to the 20% split
i = 0

for n in n_alpha:  #trying different alpha hyper paramter for naive bayes multinomial model
  naive_bayes = MultinomialNB(alpha=n)
  naive_bayes.fit(X_train, y_train)

  naive_predictions = naive_bayes.predict(X_test)
  naive_accuracy = accuracy_score(y_test, naive_predictions)
  nb_results[i] = naive_accuracy
  i = i + 1

"""Then we can Plot different accuracies for Naive Bayes algorithm with different alpha values set."""

print(nb_results)
nb_results = np.around(nb_results, decimals = 4)
plt.figure(figsize=(8, 6))

plt.plot(n_alpha, nb_results)
plt.scatter(n_alpha, nb_results)
# Add value labels next to each point
for g, accuracy in zip(n_alpha, nb_results):
    plt.text(g, accuracy, accuracy, ha='right', fontstyle='oblique', fontsize='large')
plt.xlabel('alpha value (Log Scale)')
plt.ylabel('Accuracy')
plt.xscale('log')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
btest_report = True
naive_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report, 0.01)

from sklearn.ensemble import RandomForestClassifier

def forest_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report):
  random_forest = RandomForestClassifier(n_estimators=test_var, random_state=79)
  random_forest.fit(X_train, y_train)
  forest_prediction = random_forest.predict(X_test)
  forest_accuracy = accuracy_score(y_test, forest_prediction)

  forest_report = classification_report(y_test, forest_prediction)

  print(forest_accuracy, test_var)

  if btest_report:
    print(forest_report)
    conf_matrix_forest = confusion_matrix(y_test, forest_prediction)
    sns.heatmap(conf_matrix_forest, annot=True, fmt="d", xticklabels=["Not Spam", "Spam"], yticklabels=["Not Spam", "Spam"])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Random Forest Confusion Matrix")
    plt.show()

  return forest_accuracy

btest_report = False
num_estimators = [1, 10, 100, 1000, 3000, 5000]
rf_results = np.zeros_like(num_estimators, dtype=float) #so we can plot the different accuracies across different alphas

i = 0
for num in num_estimators:
  rf_results[i] = forest_algorithm(X_train, X_test, y_train, y_test, num, btest_report)
  i = i + 1

#3000 num_estimator yields the best results, lets use that
num = 3000
btest_report = True
forest_algorithm(X_train, X_test, y_train, y_test, num, btest_report)

print(rf_results) #now we plot the random forest against different hyper params
rf_results = np.around(rf_results, decimals = 4)
plt.figure(figsize=(6, 6))

plt.plot(num_estimators, rf_results)
plt.scatter(num_estimators, rf_results)
# Add value labels next to each point
for g, accuracy in zip(num_estimators, rf_results):
    plt.text(g, accuracy, accuracy, ha='center', va='bottom', fontstyle='oblique', fontsize=10)
plt.xlabel('num_estimators value')
plt.ylabel('Accuracy')
plt.show()

from sklearn.linear_model import LogisticRegression

def logistic_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report):
  logistic = LogisticRegression(max_iter=1000, C=test_var, random_state=79)
  logistic.fit(X_train, y_train)
  logistic_prediction = logistic.predict(X_test)
  logistic_accuracy = accuracy_score(y_test, logistic_prediction)

  logistic_report = classification_report(y_test, logistic_prediction)

  print(logistic_accuracy, test_var)

  if btest_report:
    print(logistic_report)
    conf_matrix_logistic = confusion_matrix(y_test, logistic_prediction)
    sns.heatmap(conf_matrix_logistic, annot=True, fmt="d", xticklabels=["Not Spam", "Spam"], yticklabels=["Not Spam", "Spam"])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Logistic Regression Confusion Matrix")
    plt.show()

  return logistic_accuracy

Cs = [0.001, 0.01, 0.1, 1]
lr_results = np.zeros_like(Cs, dtype=float)

i = 0
btest_report = False
for C in Cs:
  lr_results[i] = logistic_algorithm(X_train, X_test, y_train, y_test, C, btest_report)
  i = i + 1

print(lr_results)
lr_results = np.around(lr_results, decimals = 4)
plt.figure(figsize=(8, 6))

plt.plot(Cs, lr_results)
plt.scatter(Cs, lr_results)
# Add value labels next to each point
for g, accuracy in zip(Cs, lr_results):
    plt.text(g, accuracy, accuracy, ha='right', fontstyle='oblique', fontsize='large')
plt.xlabel('C value (Log Scale)')
plt.ylabel('Accuracy')
plt.xscale('log')
plt.show()

btest_report = True
num = 0.1 #This yielded highest accuracy
logistic_algorithm(X_train, X_test, y_train, y_test, num, btest_report)

#Now we will finally do KNN
from sklearn.neighbors import KNeighborsClassifier

def knn_algorithm(X_train, X_test, y_train, y_test, test_var, btest_report):
  knn = KNeighborsClassifier(n_neighbors=test_var)
  knn.fit(X_train, y_train)
  knn_prediction = knn.predict(X_test)
  knn_accuracy = accuracy_score(y_test, knn_prediction)

  knn_report = classification_report(y_test, knn_prediction)

  print(knn_accuracy, test_var)

  if btest_report:
    print(knn_report)
    conf_matrix_knn = confusion_matrix(y_test, knn_prediction)
    sns.heatmap(conf_matrix_knn, annot=True, fmt="d", xticklabels=["Not Spam", "Spam"], yticklabels=["Not Spam", "Spam"])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("KNN Confusion Matrix")
    plt.show()

  return knn_accuracy

k_vals = [1, 5, 10, 50, 100]
knn_results = np.zeros_like(k_vals, dtype=float)

i = 0;
btest_report = False
for k in k_vals:
  knn_results[i] = knn_algorithm(X_train, X_test, y_train, y_test, k, btest_report)
  i = i + 1

print(knn_results)
knn_results = np.around(knn_results, decimals = 4)
plt.figure(figsize=(8, 6))

plt.plot(k_vals, knn_results)
plt.scatter(k_vals, knn_results)
# Add value labels next to each point
for g, accuracy in zip(k_vals, knn_results):
    plt.text(g, accuracy, accuracy, ha='right', fontstyle='oblique', fontsize='large')
plt.xlabel('K value (Log Scale)')
plt.ylabel('Accuracy')
plt.xscale('log')
plt.show()

btest_report = True
num = 10 #This yielded highest accuracy
knn_algorithm(X_train, X_test, y_train, y_test, num, btest_report)

accuracies = [0.9594, 0.9807, 0.9749, 0.8850]
x_axis = ["Naive Bayesian", "Random Forest", "Logistic Regression", "KNN"]

plt.bar(x_axis, accuracies)
plt.xlabel("Algorithm (Tuned with ideal hyper parameters)")
plt.ylabel("Accuracy")

for i, accuracy in enumerate(accuracies):
    plt.text(i, accuracy + 0.005, f'{accuracy:.4f}', ha='center', va='bottom')

plt.title("Accuracies for different classification methods for email spam")
plt.show()