import os
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import missingno as msno
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder, LabelEncoder,ensemble
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

arr_dataset = []

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def mypage():
    return render_template('index.html')


@app.route('/read-excel', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.files['upload-file']
        file.save(file.filename)
        extension_data = os.path.splitext(file.filename)
        if extension_data[1] == ".csv":
            data = pd.read_csv(file.filename)
        elif extension_data[1] == ".xlsx":
            data = pd.read_excel(file.filename)
        elif extension_data[1] == ".xls":
            data = pd.read_excel(file.filename)
        headings = data.columns.values
        for index, rows in data.iterrows():
            arr_dataset.append(rows.tolist())

        data_set = arr_dataset
        os.remove(file.filename)
        return render_template('index.html', headings=headings, data=data_set)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        dataset = pd.read_csv("C:\\Users\\Lenovo\\Downloads\\a.csv")
        le = LabelEncoder()
        dataset.Product = le.fit_transform(dataset.Product)
        dataset.Component = le.fit_transform(dataset.Component)
        dataset.Status = le.fit_transform(dataset.Status)
        dataset.Assignee = le.fit_transform(dataset.Assignee)
        dataset.Release = le.fit_transform(dataset.Release)
        dataset.isnull().sum()
        columns_of_sheet = dataset[['Product', 'Component', 'Status', 'Release', 'Severity']]
        X = np.asarray(columns_of_sheet)
        Y = np.asarray(dataset['Assignee'])
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.25, random_state=0)
        sc_X = StandardScaler()
        X_Train = sc_X.fit_transform(X_Train)
        X_Test = sc_X.transform(X_Test)

        g_classifier = ensemble.GradientBoostingClassifier(n_estimators=100)
        g_classifier.fit(X_Train, Y_Train)
        score2 = g_classifier.score(X_Test, Y_Test)
        print(score2 * 100)

        predict = g_classifier.predict(X_Test)
        ab = classification_report(Y_Test, predict)
        print(ab)
        print(ab)

        return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.1.1', port=5000)
