from flask import Flask, render_template, request, redirect, url_for
from Ark_Banking_Core import * 

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

        create_new_account(firstName, lastName, gender, dob, ssn, income, cOrS, checking, savings)
        return redirect(url_for('home'))
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True)
