from flask import Flask, render_template, request, Response
import pdfkit
import pandas as pd
# Set the path to the wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
app = Flask(__name__)

def calculate_loan(people, amount, position):
    position = int(position)
    people = int(people)
    amount = int(amount)

    # Calculate the original investment and loan
    invest = (position - 1) * amount
    loan = (people - position) * amount
    loan_received = (people - position) * amount


    # Calculate the profit based on the initial investment
    profit = invest * 0.10
    adjusted_invest = invest + profit
    adjusted_loan = loan - loan * 0.10

    # Calculate the total result
    result = adjusted_invest + adjusted_loan

    # Create a message that indicates the adjusted investment
    invest_message = f' You invested the initial amount : {invest}, and the profit is 10% ({profit}).'

    return result, loan, adjusted_invest, invest_message

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        people = request.form['people']
        amount = request.form['amount']
        position = request.form['position']
        result,loan, invest, invest_message = calculate_loan(people, amount, position)
        message = f'People:{people} Position : {position} : Amount :{amount}  => The total amount to be received is {result}. Your loan will be : {loan}. {invest_message}'
        return render_template('index.html', message=message)
    return render_template('index.html', message=None)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/service")
def service():
    return render_template('service.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/generate_table_pdf", methods=['POST'])
def generate_table_pdf():
    message = request.form['message']

    # Create HTML content for the PDF with only the table
    pdf_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loan Calculator Table PDF</title>
    </head>
    <body>
        <table class="table-auto">
            <tr>
                <th class="px-4 py-2">Result</th>
            </tr>
            <tr>
                <td class="px-4 py-2">{message}</td>
            </tr>
            <tr><a href="{{url_for('index')}}">Go back to home</tr>
        </table>
    </body>
    </html>
    '''

    # Create PDF from HTML content using the specified configuration
    pdf = pdfkit.from_string(pdf_content, False, configuration=config)

    # Send the PDF as a response to the user
    response = Response(pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename="loan_calculator_table.pdf"'
    return response

if __name__ == '__main__':
    app.run(debug=True)