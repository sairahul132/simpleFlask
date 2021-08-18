import os
from flask import Flask, render_template, request
import pandas as pd

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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.1.1', port=5000)
