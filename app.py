from flask import Flask, app, render_template, request
import pandas as pd

arr_dataset = []

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def mypage():
    return render_template('index.html')


@app.route('/read-excel', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # request.get_json(force=True)
        file = request.form['upload-file']

        # file = request.files['upload-file']
        # file.save(file.filename)

        data = pd.read_csv(file)
        headings = data.columns.values
        data = data
        # print(axes)
        for index, rows in data.iterrows():
            arr_dataset.append(rows.tolist())

        data = arr_dataset

        return render_template('index.html', headings=headings, data=data)
        # return render_template('index.html', data= data.to_html())


if __name__ == '__main__':
    app.run(debug=True, host='127.0.1.1', port=5000)
