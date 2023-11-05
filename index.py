from flask import Flask, render_template, request, redirect, url_for, jsonify
import ccStatementReader
import bankStatementReader



app = Flask(__name__)

@app.route('/update_value', methods=['POST'])
def update_value():
    #print(table)
    row_index = int(request.form.get('row_index'))
    new_value = request.form.get('new_value')
    if statementType == 'Federal Bank Statement':
        table.at[row_index, 'Category'] = new_value
    elif statementType == 'ICICI CC Statement':
        table.at[row_index+1, 'Category'] = new_value
    else:
        table.at[row_index, 'Category'] = new_value
    #print(table)
    success = True
    message = "Value updated!"
    #return render_template("viewtransactions.html", data=table, message=message, success=success)
    return jsonify({'success': success, 'message': message})


@app.route('/final_page')
def final_page():
    try:
        return render_template('finalpage.html')
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return "Error rendering template"

@app.route('/submit_table', methods=['POST'])
def submit_table():
    if statementType == 'ICICI CC Statement' or statementType == 'HDFC CC Statement':
        ccStatementReader.writeToMasterStatement(table)
    elif statementType == 'ICICI Bank Statement' or statementType == 'Federal Bank Statement':
        bankStatementReader.writeToMasterBankStatement(table)
    success = True
    message = 'Table submitted successfully'
    return jsonify({'success': success, 'message': message})


@app.route('/', methods =["GET", "POST"])
def home():
    global table
    global statementType
    if request.method == "POST":
        file = request.files['file']
        statementType = request.form.get("type")
        if statementType == 'ICICI CC Statement':
            table = ccStatementReader.appendingToMasterStatement(ccStatementReader.readingICICIStatement(file))
            data = table.to_dict(orient='records')
            return render_template("viewtransactions.html", data=data)
        elif statementType == 'HDFC CC Statement':
            table = ccStatementReader.appendingToMasterStatement(ccStatementReader.readingHDFCstatement(file))
            data = table.to_dict(orient='records')
            return render_template("viewtransactions.html", data=data)
        elif statementType == 'ICICI Bank Statement':
            table = bankStatementReader.appendingToMasterBankStatement(bankStatementReader.cleaningBankStatement(bankStatementReader.readingBankStatement(file)))
            data = table.to_dict(orient='records')
            return render_template("viewBankTransactions.html", data=data)
        elif statementType == 'Federal Bank Statement':
            table = bankStatementReader.appendingToMasterBankStatement(bankStatementReader.cleaningBankStatement(bankStatementReader.readFederalBankStatement(file)))
            data = table.to_dict(orient='records')
            return render_template("viewBankTransactions.html", data=data)
    return render_template("home.html")

if (__name__ == '__main__'):
    app.run(debug=True)