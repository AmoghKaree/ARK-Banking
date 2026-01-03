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
            
        try:
            with open('bankingData.txt', 'r') as f:
                lstBankingDetails = f.readlines()

            for customer_line in lstBankingDetails:
                listCust = customer_line.split(" | ")
                if len(listCust) >= 2:
                    username = listCust[0].strip()
                    password = listCust[1].strip()
                    if username == userName and password == passWord:
                        return "success"
        except Exception as e:
            print(f"Login error: {e}")
            return "fail"
        
        return "fail"
    
    def get_customer_data(self, userName):
        """Get customer information by username"""
        if not os.path.exists('bankingData.txt'):
            return None
            
        try:
            with open('bankingData.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 8 and parts[0].strip() == userName:
                        return {
                            'username': parts[0].strip(),
                            'firstName': parts[2].strip(),
                            'lastName': parts[3].strip(),
                            'gender': parts[4].strip(),
                            'dob': parts[5].strip(),
                            'income': parts[6].strip(),
                            'ssn': parts[7].strip()
                        }
        except Exception as e:
            print(f"Get customer data error: {e}")
            return None
        
        return None
        
    def createAccount(self, userName, password, firstName, lastName, gender, dob, ssn, income, cOrS, checking=0, savings=0):
        """Create a new customer account"""
        
        try:
            # Initialize files if they don't exist
            for filename in ['bankingData.txt', 'checking&SavingsData.txt', 'accountIDInfo.txt']:
                if not os.path.exists(filename):
                    open(filename, 'w').close()
            
            userIdChecking = 111111
            userIdSavings = 111111
            
            # Read current ID counters
            if os.path.getsize('accountIDInfo.txt') == 0:
                intTempChecking = userIdChecking
                intTempSavings = userIdSavings
            else:
                with open('accountIDInfo.txt', 'r') as f:
                    lstOfCandS = f.readline()
                
                if lstOfCandS.strip():
                    tempNewIDs = lstOfCandS.split(' | ')
                    intTempChecking = int(tempNewIDs[0])
                    intTempSavings = int(tempNewIDs[1])
                else:
                    intTempChecking = userIdChecking
                    intTempSavings = userIdSavings
            
            # Generate account IDs
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
            
            # Write data
            with open('bankingData.txt', 'a') as f:
                f.write(customerInfo)
            
            with open('checking&SavingsData.txt', 'a') as f:
                f.write(bankingInfo)
            
            with open('accountIDInfo.txt', 'w') as f:
                f.write(f'{intTempChecking} | {intTempSavings}')
            
            return True
        
        except Exception as e:
            print(f"Create account error: {e}")
            return False


class Accounts:
    
    def get_user_accounts(self, userName):
        """Get account information for a specific user"""
        if not os.path.exists('bankingData.txt') or not os.path.exists('checking&SavingsData.txt'):
            print(f"DEBUG: Files don't exist")
            return None
        
        try:
            # Find user's account IDs from bankingData.txt
            account_ids = []
            with open('bankingData.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 2 and parts[0].strip() == userName:
                        # Extract all account IDs (they start from index 8)
                        for i in range(8, len(parts)):
                            if parts[i].strip() and parts[i].strip() != '':
                                account_ids.append(parts[i].strip())
                        break
            
            if not account_ids:
                print(f"DEBUG: No account IDs found for user {userName}")
                return None
            
            print(f"DEBUG: Found account IDs: {account_ids}")
            
            # Now find balances in checking&SavingsData.txt
            with open('checking&SavingsData.txt', 'r') as f:
                for acc_line in f:
                    acc_parts = acc_line.strip().split(' | ')
                    
                    print(f"DEBUG: Checking line: {acc_parts}")
                    
                    if acc_parts[0] == 'both' and len(acc_parts) >= 5:
                        checking_id = acc_parts[3].strip()
                        savings_id = acc_parts[4].strip()
                        print(f"DEBUG: Comparing both - checking: {checking_id} in {account_ids}, savings: {savings_id} in {account_ids}")
                        
                        if checking_id in account_ids and savings_id in account_ids:
                            print(f"DEBUG: Match found for both accounts!")
                            return {
                                'type': 'both',
                                'checkingBalance': float(acc_parts[1]),
                                'savingsBalance': float(acc_parts[2]),
                                'checkingId': checking_id,
                                'savingsId': savings_id
                            }
                    
                    elif acc_parts[0] == 'checking' and len(acc_parts) >= 3:
                        checking_id = acc_parts[2].strip()
                        print(f"DEBUG: Comparing checking - {checking_id} in {account_ids}")
                        
                        if checking_id in account_ids:
                            print(f"DEBUG: Match found for checking!")
                            return {
                                'type': 'checking',
                                'checkingBalance': float(acc_parts[1]),
                                'savingsBalance': 0,
                                'checkingId': checking_id,
                                'savingsId': None
                            }
                    
                    elif acc_parts[0] == 'savings' and len(acc_parts) >= 3:
                        savings_id = acc_parts[2].strip()
                        print(f"DEBUG: Comparing savings - {savings_id} in {account_ids}")
                        
                        if savings_id in account_ids:
                            print(f"DEBUG: Match found for savings!")
                            return {
                                'type': 'savings',
                                'checkingBalance': 0,
                                'savingsBalance': float(acc_parts[1]),
                                'checkingId': None,
                                'savingsId': savings_id
                            }
        
        except Exception as e:
            print(f"Get user accounts error: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        print(f"DEBUG: No matching accounts found")
        return None

    def process_transaction(self, userName, transType, amount, accountType):
        """Process deposit or withdrawal"""
        timeNew = time.asctime()
        
        try:
            if not os.path.exists('transactionData.txt'):
                open('transactionData.txt', 'w').close()
            
            user_accounts = self.get_user_accounts(userName)
            if not user_accounts:
                print(f"DEBUG: User accounts not found for {userName}")
                return False, "User account not found"
            
            print(f"DEBUG: User accounts: {user_accounts}")
            
            # Read all accounts
            with open('checking&SavingsData.txt', 'r') as f:
                account_lines = f.readlines()
            
            updated_lines = []
            transaction_made = False
            
            for line in account_lines:
                parts = line.strip().split(' | ')
                
                if parts[0] == 'both' and len(parts) >= 5:
                    checking_id = parts[3].strip()
                    savings_id = parts[4].strip()
                    
                    if checking_id == user_accounts.get('checkingId') and savings_id == user_accounts.get('savingsId'):
                        checking_bal = float(parts[1])
                        savings_bal = float(parts[2])
                        
                        print(f"DEBUG: Found both account match. Current balances - C: {checking_bal}, S: {savings_bal}")
                        
                        if accountType == 'checking':
                            if transType == 'deposit':
                                checking_bal += float(amount)
                            elif transType == 'withdraw':
                                checking_bal -= float(amount)
                        elif accountType == 'savings':
                            if transType == 'deposit':
                                savings_bal += float(amount)
                            elif transType == 'withdraw':
                                savings_bal -= float(amount)
                        
                        print(f"DEBUG: New balances - C: {checking_bal}, S: {savings_bal}")
                        updated_lines.append(f"both | {checking_bal} | {savings_bal} | {checking_id} | {savings_id} | \n")
                        transaction_made = True
                    else:
                        updated_lines.append(line)
                        
                elif parts[0] == 'checking' and len(parts) >= 3:
                    checking_id = parts[2].strip()
                    
                    if checking_id == user_accounts.get('checkingId'):
                        balance = float(parts[1])
                        
                        print(f"DEBUG: Found checking account match. Current balance: {balance}")
                        
                        if transType == 'deposit':
                            balance += float(amount)
                        elif transType == 'withdraw':
                            balance -= float(amount)
                        
                        print(f"DEBUG: New balance: {balance}")
                        updated_lines.append(f"checking | {balance} | {checking_id} | \n")
                        transaction_made = True
                    else:
                        updated_lines.append(line)
                        
                elif parts[0] == 'savings' and len(parts) >= 3:
                    savings_id = parts[2].strip()
                    
                    if savings_id == user_accounts.get('savingsId'):
                        balance = float(parts[1])
                        
                        print(f"DEBUG: Found savings account match. Current balance: {balance}")
                        
                        if transType == 'deposit':
                            balance += float(amount)
                        elif transType == 'withdraw':
                            balance -= float(amount)
                        
                        print(f"DEBUG: New balance: {balance}")
                        updated_lines.append(f"savings | {balance} | {savings_id} | \n")
                        transaction_made = True
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            if transaction_made:
                print(f"DEBUG: Writing updated balances")
                with open('checking&SavingsData.txt', 'w') as f:
                    f.writelines(updated_lines)
                
                with open('transactionData.txt', 'a') as f:
                    f.write(f"{userName} | {transType} ${amount} to {accountType} | DATE OF TRANSACTION {timeNew}\n")
                
                return True, f"{transType.capitalize()} of ${amount} successful"
            
            print(f"DEBUG: No transaction made")
            return False, "Transaction failed - account not matched"
        
        except Exception as e:
            print(f"Transaction error: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error: {str(e)}"
    
    def transfer_funds(self, userName, amount, fromAccount, toAccount):
        """Transfer between accounts"""
        timeNew = time.asctime()
        
        try:
            user_accounts = self.get_user_accounts(userName)
            if not user_accounts or user_accounts['type'] != 'both':
                return False, "Transfer requires both accounts"
            
            with open('checking&SavingsData.txt', 'r') as f:
                account_lines = f.readlines()
            
            updated_lines = []
            transfer_made = False
            
            for line in account_lines:
                parts = line.strip().split(' | ')
                
                if parts[0] == 'both' and len(parts) >= 5:
                    checking_id = parts[3].strip()
                    savings_id = parts[4].strip()
                    
                    if checking_id == user_accounts['checkingId'] and savings_id == user_accounts['savingsId']:
                        checking_bal = float(parts[1])
                        savings_bal = float(parts[2])
                        
                        if fromAccount == 'checking' and toAccount == 'savings':
                            checking_bal -= float(amount)
                            savings_bal += float(amount)
                        elif fromAccount == 'savings' and toAccount == 'checking':
                            savings_bal -= float(amount)
                            checking_bal += float(amount)
                        
                        updated_lines.append(f"both | {checking_bal} | {savings_bal} | {checking_id} | {savings_id} | \n")
                        transfer_made = True
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            if transfer_made:
                with open('checking&SavingsData.txt', 'w') as f:
                    f.writelines(updated_lines)
                
                with open('transactionData.txt', 'a') as f:
                    f.write(f"{userName} | transferred ${amount} from {fromAccount} to {toAccount} | DATE OF TRANSACTION {timeNew}\n")
                
                return True, f"Transferred ${amount}"
            
            return False, "Transfer failed"
        
        except Exception as e:
            print(f"Transfer error: {e}")
            return False, f"Error: {str(e)}"
    
    def get_transaction_history(self, userName):
        """Get transaction history"""
        if not os.path.exists('transactionData.txt'):
            return []
        
        try:
            transactions = []
            with open('transactionData.txt', 'r') as f:
                for line in f:
                    if userName in line:
                        transactions.append(line.strip())
            return transactions[-10:]
        except Exception as e:
            print(f"Transaction history error: {e}")
            return []import os
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
            
        try:
            with open('bankingData.txt', 'r') as f:
                lstBankingDetails = f.readlines()

            for customer_line in lstBankingDetails:
                listCust = customer_line.split(" | ")
                if len(listCust) >= 2:
                    username = listCust[0].strip()
                    password = listCust[1].strip()
                    if username == userName and password == passWord:
                        return "success"
        except Exception as e:
            print(f"Login error: {e}")
            return "fail"
        
        return "fail"
    
    def get_customer_data(self, userName):
        """Get customer information by username"""
        if not os.path.exists('bankingData.txt'):
            return None
            
        try:
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
        except Exception as e:
            print(f"Get customer data error: {e}")
            return None
        
        return None
        
    def createAccount(self, userName, password, firstName, lastName, gender, dob, ssn, income, cOrS, checking=0, savings=0):
        """Create a new customer account"""
        
        try:
            # Initialize files if they don't exist
            for filename in ['bankingData.txt', 'checking&SavingsData.txt', 'accountIDInfo.txt']:
                if not os.path.exists(filename):
                    open(filename, 'w').close()
            
            userIdChecking = 111111
            userIdSavings = 111111
            
            # Read current ID counters
            if os.path.getsize('accountIDInfo.txt') == 0:
                intTempChecking = userIdChecking
                intTempSavings = userIdSavings
            else:
                with open('accountIDInfo.txt', 'r') as f:
                    lstOfCandS = f.readline()
                
                if lstOfCandS.strip():
                    tempNewIDs = lstOfCandS.split(' | ')
                    intTempChecking = int(tempNewIDs[0])
                    intTempSavings = int(tempNewIDs[1])
                else:
                    intTempChecking = userIdChecking
                    intTempSavings = userIdSavings
            
            # Generate account IDs
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
            
            # Write data
            with open('bankingData.txt', 'a') as f:
                f.write(customerInfo)
            
            with open('checking&SavingsData.txt', 'a') as f:
                f.write(bankingInfo)
            
            with open('accountIDInfo.txt', 'w') as f:
                f.write(f'{intTempChecking} | {intTempSavings}')
            
            return True
        
        except Exception as e:
            print(f"Create account error: {e}")
            return False


class Accounts:
    
    def get_user_accounts(self, userName):
        """Get account information for a specific user"""
        if not os.path.exists('bankingData.txt') or not os.path.exists('checking&SavingsData.txt'):
            return None
        
        try:
            # Find user's account IDs
            with open('bankingData.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(' | ')
                    if len(parts) >= 2 and parts[0] == userName:
                        account_ids = []
                        for i in range(8, len(parts)):
                            if parts[i].strip():
                                account_ids.append(parts[i].strip())
                        
                        # Find balances
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
        except Exception as e:
            print(f"Get user accounts error: {e}")
            return None
        
        return None

    def process_transaction(self, userName, transType, amount, accountType):
        """Process deposit or withdrawal"""
        timeNew = time.asctime()
        
        try:
            if not os.path.exists('transactionData.txt'):
                open('transactionData.txt', 'w').close()
            
            user_accounts = self.get_user_accounts(userName)
            if not user_accounts:
                return False, "User not found"
            
            # Read all accounts
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
                with open('checking&SavingsData.txt', 'w') as f:
                    f.writelines(updated_lines)
                
                with open('transactionData.txt', 'a') as f:
                    f.write(f"{userName} | {transType} ${amount} to {accountType} | DATE OF TRANSACTION {timeNew}\n")
                
                return True, f"{transType.capitalize()} of ${amount} successful"
            
            return False, "Transaction failed"
        
        except Exception as e:
            print(f"Transaction error: {e}")
            return False, f"Error: {str(e)}"
    
    def transfer_funds(self, userName, amount, fromAccount, toAccount):
        """Transfer between accounts"""
        timeNew = time.asctime()
        
        try:
            user_accounts = self.get_user_accounts(userName)
            if not user_accounts or user_accounts['type'] != 'both':
                return False, "Transfer requires both accounts"
            
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
                with open('checking&SavingsData.txt', 'w') as f:
                    f.writelines(updated_lines)
                
                with open('transactionData.txt', 'a') as f:
                    f.write(f"{userName} | transferred ${amount} from {fromAccount} to {toAccount} | DATE OF TRANSACTION {timeNew}\n")
                
                return True, f"Transferred ${amount}"
            
            return False, "Transfer failed"
        
        except Exception as e:
            print(f"Transfer error: {e}")
            return False, f"Error: {str(e)}"
    
    def get_transaction_history(self, userName):
        """Get transaction history"""
        if not os.path.exists('transactionData.txt'):
            return []
        
        try:
            transactions = []
            with open('transactionData.txt', 'r') as f:
                for line in f:
                    if userName in line:
                        transactions.append(line.strip())
            return transactions[-10:]
        except Exception as e:
            print(f"Transaction history error: {e}")
            return []
