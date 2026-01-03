import os
import time
import datetime

class customer:
    def __init__(self, userName=None, passWord=None):
        self.userName = userName
        self.passWord = passWord
        
    def check_login(self, userName, passWord):
        """Validate user login credentials"""
        if not os.path.exists('bankingData.txt'):
            return "fail"
            
        bankingCustomerData = open('bankingData.txt', 'r')
        lstBankingDetails = bankingCustomerData.readlines()
        bankingCustomerData.close()

        for customer in lstBankingDetails:
            listCust = customer.split(" | ")
            if len(listCust) >= 2:
                username = listCust[0]
                password = listCust[1]
                if username == userName and password == passWord:
                    return "success"
        return "fail"
    
    def get_customer_data(self, userName):
        """Get customer information by username"""
        if not os.path.exists('bankingData.txt'):
            return None
            
        with open('bankingData.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(' | ')
                if len(parts) >= 8 and parts[0] == userName:
                    return {
                        'username': parts[0],
                        'firstName': parts[2],
                        'lastName': parts[3],
                        'gender': parts[4],
                        'dob': parts[5],
                        'income': parts[6],
                        'ssn': parts[7]
                    }
        return None
        
    def createAccount(self, userName, password, firstName, lastName, gender, dob, ssn, income, cOrS, checking=0, savings=0):
        """Create a new customer account"""
        
        # Initialize files if they don't exist
        if not os.path.exists('bankingData.txt'):
            open('bankingData.txt', 'w').close()
        if not os.path.exists('checking&SavingsData.txt'):
            open('checking&SavingsData.txt', 'w').close()
        if not os.path.exists('accountIDInfo.txt'):
            open('accountIDInfo.txt', 'w').close()
        
        customerData = open('bankingData.txt', 'a+')
        bankingData = open('checking&SavingsData.txt', 'a+')

        userIdChecking = 111111
        userIdSavings = 111111
        
        # Read current ID counters
        if os.path.getsize('accountIDInfo.txt') == 0:
            intTempChecking = userIdChecking
            intTempSavings = userIdSavings
        else:
            accountIDInfo = open('accountIDInfo.txt', 'r')
            lstOfCandS = accountIDInfo.readline()
            accountIDInfo.close()
            
            if lstOfCandS.strip():
                tempNewIDs = lstOfCandS.split(' | ')
                intTempChecking = int(tempNewIDs[0])
                intTempSavings = int(tempNewIDs[1])
            else:
                intTempChecking = userIdChecking
                intTempSavings = userIdSavings
        
        # Generate account IDs based on account type
        if cOrS == 'both':
            checkingId = 'c' + str(intTempChecking)
            savingsId = 's' + str(intTempSavings)
            intTempChecking += 1
            intTempSavings += 1
            
            customerInfo = f"{userName} | {password} | {firstName} | {lastName} | {gender} | {dob} | {income} | {ssn} | {checkingId} | {savingsId} | \n"
            bankingInfo = f"both | {checking} | {savings} | {checkingId} | {savingsId} | \n"
                
        elif cOrS == 'savings':
            savingsId = 's' + str(intTempSavings)
            intTempSavings += 1
            
            customerInfo = f"{userName} | {password} | {firstName} | {lastName} | {gender} | {dob} | {income} | {ssn} | {savingsId} | \n"
            bankingInfo = f"savings | {savings} | {savingsId} | \n"

        elif cOrS == 'checking':
            checkingId = 'c' + str(intTempChecking)
            intTempChecking += 1
            
            customerInfo = f"{userName} | {password} | {firstName} | {lastName} | {gender} | {dob} | {income} | {ssn} | {checkingId} | \n"
            bankingInfo = f"checking | {checking} | {checkingId} | \n"
        
        # Write customer and account data
        customerData.write(customerInfo)
        bankingData.write(bankingInfo)
        customerData.close()
        bankingData.close()
        
        # Update ID counters
        accountIDInfo = open('accountIDInfo.txt', 'w')
        accountIDInfo.write(f'{intTempChecking} | {intTempSavings}')
        accountIDInfo.close()
        
        return True


class Accounts:
    
    def get_user_accounts(self, userName):
        """Get account information for a specific user"""
        if not os.path.exists('bankingData.txt') or not os.path.exists('checking&SavingsData.txt'):
            return None
        
        # Find user's account IDs from bankingData.txt
        with open('bankingData.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(' | ')
                if len(parts) >= 2 and parts[0] == userName:
                    # Extract account IDs
                    account_ids = []
                    for i in range(8, len(parts)):
                        if parts[i].strip() and parts[i].strip() != '':
                            account_ids.append(parts[i].strip())
                    
                    # Now find balances in checking&SavingsData.txt
                    with open('checking&SavingsData.txt', 'r') as acc_file:
                        for acc_line in acc_file:
                            acc_parts = acc_line.strip().split(' | ')
                            
                            if acc_parts[0] == 'both' and len(acc_parts) >= 5:
                                if acc_parts[3] in account_ids and acc_parts[4] in account_ids:
                                    return {
                                        'type': 'both',
                                        'checkingBalance': float(acc_parts[1]),
                                        'savingsBalance': float(acc_parts[2]),
                                        'checkingId': acc_parts[3],
                                        'savingsId': acc_parts[4]
                                    }
                            elif acc_parts[0] == 'checking' and len(acc_parts) >= 3:
                                if acc_parts[2] in account_ids:
                                    return {
                                        'type': 'checking',
                                        'checkingBalance': float(acc_parts[1]),
                                        'savingsBalance': 0,
                                        'checkingId': acc_parts[2],
                                        'savingsId': None
                                    }
                            elif acc_parts[0] == 'savings' and len(acc_parts) >= 3:
                                if acc_parts[2] in account_ids:
                                    return {
                                        'type': 'savings',
                                        'checkingBalance': 0,
                                        'savingsBalance': float(acc_parts[1]),
                                        'checkingId': None,
                                        'savingsId': acc_parts[2]
                                    }
        return None

    def showAllData(self):
        """Display all customer and account data"""
        bankingCustomerData = open('bankingData.txt', 'r')
        accountDetails = open('checking&SavingsData.txt', 'r')
        allData = bankingCustomerData.read()
        moreData = accountDetails.read()
        bankingCustomerData.close()
        accountDetails.close()
        return allData, moreData
    
    def process_transaction(self, userName, transType, amount, accountType):
        """Process deposit or withdrawal"""
        timeNew = time.asctime()
        
        if not os.path.exists('transactionData.txt'):
            open('transactionData.txt', 'w').close()
        
        # Get user's account info
        user_accounts = self.get_user_accounts(userName)
        if not user_accounts:
            return False, "User not found"
        
        # Read all account data
        with open('checking&SavingsData.txt', 'r') as f:
            account_lines = f.readlines()
        
        updated_lines = []
        transaction_made = False
        
        for line in account_lines:
            parts = line.strip().split(' | ')
            
            if parts[0] == 'both' and len(parts) >= 5:
                if parts[3] == user_accounts.get('checkingId') and parts[4] == user_accounts.get('savingsId'):
                    checking_bal = float(parts[1])
                    savings_bal = float(parts[2])
                    
                    if accountType == 'checking':
                        if transType == 'deposit':
                            checking_bal += float(amount)
                        elif transType == 'withdraw':
                            checking_bal -= float(amount)
                        updated_lines.append(f"both | {checking_bal} | {savings_bal} | {parts[3]} | {parts[4]} | \n")
                    elif accountType == 'savings':
                        if transType == 'deposit':
                            savings_bal += float(amount)
                        elif transType == 'withdraw':
                            savings_bal -= float(amount)
                        updated_lines.append(f"both | {checking_bal} | {savings_bal} | {parts[3]} | {parts[4]} | \n")
                    
                    transaction_made = True
                else:
                    updated_lines.append(line)
                    
            elif parts[0] == 'checking' and len(parts) >= 3:
                if parts[2] == user_accounts.get('checkingId'):
                    balance = float(parts[1])
                    if transType == 'deposit':
                        balance += float(amount)
                    elif transType == 'withdraw':
                        balance -= float(amount)
                    updated_lines.append(f"checking | {balance} | {parts[2]} | \n")
                    transaction_made = True
                else:
                    updated_lines.append(line)
                    
            elif parts[0] == 'savings' and len(parts) >= 3:
                if parts[2] == user_accounts.get('savingsId'):
                    balance = float(parts[1])
                    if transType == 'deposit':
                        balance += float(amount)
                    elif transType == 'withdraw':
                        balance -= float(amount)
                    updated_lines.append(f"savings | {balance} | {parts[2]} | \n")
                    transaction_made = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        if transaction_made:
            # Write updated balances
            with open('checking&SavingsData.txt', 'w') as f:
                f.writelines(updated_lines)
            
            # Log transaction
            with open('transactionData.txt', 'a') as f:
                f.write(f"{userName} | {transType} {amount} to {accountType} account | DATE OF TRANSACTION {timeNew}\n")
            
            return True, f"{transType.capitalize()} of ${amount} successful"
        
        return False, "Transaction failed"
    
    def transfer_funds(self, userName, amount, fromAccount, toAccount):
        """Transfer money between checking and savings"""
        timeNew = time.asctime()
        
        user_accounts = self.get_user_accounts(userName)
        if not user_accounts or user_accounts['type'] != 'both':
            return False, "Transfer requires both checking and savings accounts"
        
        # Read all account data
        with open('checking&SavingsData.txt', 'r') as f:
            account_lines = f.readlines()
        
        updated_lines = []
        transfer_made = False
        
        for line in account_lines:
            parts = line.strip().split(' | ')
            
            if parts[0] == 'both' and len(parts) >= 5:
                if parts[3] == user_accounts['checkingId'] and parts[4] == user_accounts['savingsId']:
                    checking_bal = float(parts[1])
                    savings_bal = float(parts[2])
                    
                    if fromAccount == 'checking' and toAccount == 'savings':
                        checking_bal -= float(amount)
                        savings_bal += float(amount)
                    elif fromAccount == 'savings' and toAccount == 'checking':
                        savings_bal -= float(amount)
                        checking_bal += float(amount)
                    
                    updated_lines.append(f"both | {checking_bal} | {savings_bal} | {parts[3]} | {parts[4]} | \n")
                    transfer_made = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        if transfer_made:
            # Write updated balances
            with open('checking&SavingsData.txt', 'w') as f:
                f.writelines(updated_lines)
            
            # Log transaction
            with open('transactionData.txt', 'a') as f:
                f.write(f"{userName} | transferred {amount} from {fromAccount} to {toAccount} | DATE OF TRANSACTION {timeNew}\n")
            
            return True, f"Transferred ${amount} from {fromAccount} to {toAccount}"
        
        return False, "Transfer failed"
    
    def get_transaction_history(self, userName):
        """Get transaction history for a user"""
        if not os.path.exists('transactionData.txt'):
            return []
        
        transactions = []
        with open('transactionData.txt', 'r') as f:
            for line in f:
                if userName in line:
                    transactions.append(line.strip())
        
        return transactions[-10:]  # Return last 10 transactions
