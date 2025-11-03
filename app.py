from flask import Flask, render_template, request, redirect, url_for
from Ark_Banking_Core import * 
import os

app = Flask(__name__)

cus = customer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['gender']
        dob = request.form['dob']
        ssn = request.form['ssn']
        income = request.form['income']
        cOrS = request.form['cOrS']
        checking = request.form.get('checking', 0)
        savings = request.form.get('savings', 0)

        cus.createAccount(firstName, lastName, gender, dob, ssn, income, cOrS, checking, savings)

        return redirect(url_for('success', message="Account successfully created!"))

    return render_template('create_account.html')


@app.route('/success')
def success():
    message = request.args.get('message', "Action completed successfully.")
    return render_template('success.html', message=message)


if __name__ == '__main__':
    # Ensure your data files exist so Python doesn’t crash
    for file in ["bankingData.txt", "checking&SavingsData.txt", "accountIDInfo.txt"]:
        if not os.path.exists(file):
            open(file, 'w').close()

    app.run(debug=True)
