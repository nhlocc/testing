import os
import csv
import libraries.utils as utils
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_name = request.form['project_name']
        product_name = request.form['product_name']
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        if file:
            response = utils.parse_and_query_vector(file_path)
            data_response = utils.process_data_response(response)
            return jsonify(data_response)

    return render_template('index.html')

@app.route('/check_report', methods=['GET', 'POST'])
def check_report():
    if request.method == 'POST':
        project_name = request.form['project_name']
        product_name = request.form['product_name']
        week = request.form['week']

        file_path = "./data/sbc_web/w16_final_data_input.csv"
        report_data = []

        if os.path.exists(file_path):
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    report_data.append(row)
        else:
            return render_template('check_report.html', error="File not found.", projects=[], products=[], weeks=[], report_data=[])

        return render_template('check_report.html', report_data=report_data, projects=[], products=[], weeks=[])

    return render_template('check_report.html', projects=[], products=[], weeks=[], report_data=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
