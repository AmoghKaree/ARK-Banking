from flask import Flask, render_template, request, redirect, url_for, session, flash
from Ark_Banking_Core import customer, Accounts
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.permanent_session_lifetime = timedelta(minutes=30)

cus = customer()
acc = Accounts()

# Initialize data files
for file in ["bankingData.txt", "checking&SavingsData.txt", "accountIDInfo.txt", "transactionData.txt"]:
    if not os.path.exists(file):
        open(file, 'w').close()

@app.route('/')
def home():
    """Home/Login page"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])  # ← THIS WAS MISSING!
def login():
    """Process login"""
    userName = request.form.get('username')
    passWord = request.form.get('password')
    
    result = cus.check_login(userName, passWord)
    
    if result == "success":
        session.permanent = True
        session['username'] = userName
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'username' not in session:
        return redirect(url_for('home'))
    
    userName = session['username']
    
    # Get user data
    user_data = cus.get_customer_data(userName)
    account_data = acc.get_user_accounts(userName)
    transactions = acc.get_transaction_history(userName)
    
    return render_template('dashboard.html', 
                          user=user_data, 
                          accounts=account_data,
                          transactions=transactions)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """Create new account page"""
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['gender']
        dob = request.form['dob']
        ssn = request.form['ssn']
        income = request.form['income']
        cOrS = request.form['accountType']
        
        checking = request.form.get('checking', 0)
        savings = request.form.get('savings', 0)
        
        try:
            cus.createAccount(userName, password, firstName, lastName, gender, dob, ssn, income, cOrS, checking, savings)
            flash('Account successfully created! Please login.', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
            return redirect(url_for('create_account'))
    
    return render_template('create_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    """Deposit money"""
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        amount = request.form['amount']
        accountType = request.form['accountType']
        userName = session['username']
        
        success, message = acc.process_transaction(userName, 'deposit', amount, accountType)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('dashboard'))
    
    account_data = acc.get_user_accounts(session['username'])
    return render_template('deposit.html', accounts=account_data)

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    """Withdraw money"""
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        amount = request.form['amount']
        accountType = request.form['accountType']
        userName = session['username']
        
        success, message = acc.process_transaction(userName, 'withdraw', amount, accountType)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('dashboard'))
    
    account_data = acc.get_user_accounts(session['username'])
    return render_template('withdraw.html', accounts=account_data)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """Transfer between accounts"""
    if 'username' not in session:
        return redirect(url_for('home'))
    
    userName = session['username']
    account_data = acc.get_user_accounts(userName)
    
    if not account_data or account_data['type'] != 'both':
        flash('You need both checking and savings accounts to transfer', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        amount = request.form['amount']
        fromAccount = request.form['fromAccount']
        toAccount = request.form['toAccount']
        
        success, message = acc.transfer_funds(userName, amount, fromAccount, toAccount)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('transfer.html', accounts=account_data)

@app.route('/transactions')
def transactions():
    """View transaction history"""
    if 'username' not in session:
        return redirect(url_for('home'))
    
    userName = session['username']
    transaction_history = acc.get_transaction_history(userName)
    
    return render_template('transactions.html', transactions=transaction_history)

@app.route('/debug-transactions')
def debug_transactions():
    import os
    
    # Check if file exists
    file_exists = os.path.exists('transactionData.txt')
    
    # Try to read file
    try:
        with open('transactionData.txt', 'r') as f:
            content = f.read()
    except:
        content = "File not found or error reading"
    
    return f"<pre>File exists: {file_exists}\n\nContent:\n{content}</pre>"

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/success')
def success():
    """Success page"""
    message = request.args.get('message', "Action completed successfully.")
    return render_template('success.html', message=message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
