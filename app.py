from io import BytesIO

from flask import Flask, render_template, request, send_file
from openpyxl import Workbook

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form() -> str:
    return render_template('form.html')


@app.route('/download', methods=['POST'])
def download_excel():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    notes = request.form.get('notes', '').strip()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Form Submission'

    sheet.append(['Field', 'Value'])
    sheet.append(['Name', name])
    sheet.append(['Email', email])
    sheet.append(['Phone', phone])
    sheet.append(['Notes', notes])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='form_submission.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
