from flask import Flask, render_template, request, redirect, url_for
from Ark_Banking_Core import *  # import your banking functions

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        ssn = request.form['ssn']
        # Call your backend function here
        create_new_account(name, ssn)
        return redirect(url_for('home'))
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True)
