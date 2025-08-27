import os
import time
import datetime
import calendar

class customer:
    def storeCustomerDetails(self):
        print('Hello, you are opneing an account with Amogh Banking. Please enter prelimenery information. \n')
        firstName = input('What is your first name? \n')
        lastName = input('What is your last name? \n')
        gender = input('What is your gender? \n')
        dob = input('When were you born? \n')
        ssn = input('What is your social security number? \n')
        income = input('What is your income per annum? \n')
        cOrS = input('Are you interested in opening an account for checking, savings, or both? \n')

        if cOrS == 'checking':
            checking = input('How much would you like to put in your checking account? \n')
            savings = 0
        elif cOrS == 'savings':
            savings = input('How much would you like to put in your savings account? \n')
            checking = 0
        elif cOrS == 'both':
            checking = input('How much would you like to put in your checking account? \n')
            savings = input('How much would you like to put in your savings account? \n')
        else:
            return 'Please pick type checking, savings, or both'
        
        if 'bankingData.txt' == None:
            customerData = open('bankingData.txt', 'w+')
            bankingData = open('checking&SavingsData.txt', 'w+')
        else:
            customerData = open('bankingData.txt', 'a+')
            bankingData = open('checking&SavingsData.txt', 'a+')

        # customerInfo = str(firstName) + ' | ' + str(lastName) + ' | ' + str(gender) + ' | ' + str(dob) + ' | ' + str(income) + ' | ' + str(ssn) + ' | ' + '\n'

        userIdChecking = 111111
        userIdSavings = 111111
        accountIDInfo = open('accountIDInfo.txt', 'r')
    
        if os.path.getsize('accountIDInfo.txt') == 0:
            lstOfCandS = ' ' + ' | ' + ' '
            tempNewIDs = lstOfCandS.split(' | ')
            tempChecking = tempNewIDs[0]
            tempSavings = tempNewIDs[1]
        else:
            lstOfCandS = accountIDInfo.readline()
            tempNewIDs = lstOfCandS.split(' | ')
            tempChecking = tempNewIDs[0]
            tempSavings = tempNewIDs[1]
            intTempChecking = int(tempChecking)
            intTempSavings = int(tempSavings)

        accountIDInfo.close()
        accountIDInfo = open('accountIDInfo.txt', 'w')
        
        

        if cOrS == 'both':

            if tempChecking == ' ':
                checkingId = 'c' + str(userIdChecking)
                userIdChecking += 1 
            else:
                checkingId = 'c' + str(tempChecking)

            if tempSavings == ' ':
                savingsId = 's' + str(userIdSavings)
                userIdSavings += 1 
                tempNewIDs = str(userIdChecking) + ' | ' + str(userIdSavings)
            else:
                savingsId = 's' + str(tempSavings)

            if tempChecking != ' ':
                intTempChecking += 1
                intTempSavings += 1
                tempNewIDs = str(intTempChecking) + ' | ' + str(intTempSavings) 

            accountIDInfo.write(tempNewIDs)
            accountIDInfo.close()

            customerInfo = str(firstName) + ' | ' + str(lastName) + ' | ' + str(gender) + ' | ' + str(dob) + ' | ' + str(income) + ' | ' + str(ssn) + ' | ' + str(checkingId) + ' | ' + str(savingsId) +  ' | ' + ' \n'
            bankingInfo = str(cOrS) +  ' | ' + str(checking)  + ' | ' + str(savings)  + ' | ' + str(checkingId) + ' | ' + str(savingsId) + ' | ' +' \n'
            
                
        elif cOrS == 'savings':

            if tempSavings == ' ':
                savingsId = 's' + str(userIdSavings)
                tempSavings = userIdChecking
            else:
                savingsId = 's' + str(tempSavings)

            if type(intTempChecking) == int or type(intTempChecking) == float:
                intTempSavings += 1

            tempNewIDs = str(intTempChecking) + ' | ' + str(intTempSavings)
            accountIDInfo.write(tempNewIDs)

            customerInfo = str(firstName) + ' | ' + str(lastName) + ' | ' + str(gender) + ' | ' + str(dob) + ' | ' + str(income) + ' | ' + str(ssn) + ' | ' + str(savingsId) +  ' | ' + ' \n'
            bankingInfo = str(cOrS) + ' | ' + str(savings) + ' | ' + str(savingsId) + ' | ' + ' \n'

        elif cOrS == 'checking':

            if tempChecking == ' ':
                checkingId = 'c' + str(userIdChecking)
                tempChecking = userIdChecking
            else:
                checkingId = 'c' + str(tempChecking)

            if type(intTempChecking) == int or type(intTempChecking) == float:
                intTempChecking += 1

            tempNewIDs = str(intTempChecking) + ' | ' + str(intTempSavings)
            accountIDInfo.write(tempNewIDs)

            customerInfo = str(firstName) + ' | ' + str(lastName) + ' | ' + str(gender) + ' | ' + str(dob) + ' | ' + str(income) + ' | ' + str(ssn) + ' | ' + str(checkingId) + ' | ' + ' \n'
            bankingInfo = str(cOrS) + ' | ' + str(checking)  +  ' | ' +  str(checkingId) + ' | ' + ' \n'
        
        customerData.write(customerInfo)
        bankingData.write(bankingInfo)
        customerData.close()
        bankingData.close()

class Accounts: 


    def showAllData(self):
        bankingCustomerData = open('bankingData.txt', 'r')
        accountDetails = open('checking&SavingsData.txt', 'r')
        allData = bankingCustomerData.read()
        moreData = accountDetails.read()

        return allData, moreData
    
    def depositOrWithdraw(self):
        timeNew = time.asctime()
        print('This is the withdraw / deposit feature. Just an FYI, you can withdraw or deposit one  account at a time')
        userName = input('What is your full name: ')
        nameVar = userName.split()
        firstName = nameVar[0]
        lastName = nameVar[1]

        checkingAndSavingsData = open('checking&SavingsData.txt', 'r')
        bankingCustomerData = open('bankingData.txt', 'r')

        fullDataLst = checkingAndSavingsData.read()

        checkingAndSavingsData = open('checking&SavingsData.txt', 'r')
        lstCustomersDetails = checkingAndSavingsData.readlines()
        lstBankingDetails = bankingCustomerData.readlines()


        wOrD = input('Would you like to withdraw or deposit: ')


        if wOrD == 'withdraw':
            withdrawAmt = input('How much do you want to withdraw: $')
            depositAmt = 0

        elif wOrD == 'deposit':
            depositAmt = input('How much do you want to deposit: $')
            withdrawAmt = 0
        else:
            return('Please type "withdraw" or "deposit"...')

        if 'transactionData.txt':
            transactionData = open('transactionData.txt', 'a+')
        else:
            transactionData = open('transactionData.txt', 'w+')

        for customers in lstBankingDetails:
            lstCust = customers.split(' | ')
            if firstName == lstCust[0] and lastName == lstCust[1]:
                for bankingDeets in lstCustomersDetails:
                    lstBankingDeets = bankingDeets.split(' | ')

                    if lstBankingDeets[0] == 'both' and lstBankingDeets[3] == lstCust[6] and lstBankingDeets[4] == lstCust[7]:
                        cOrS = input('What would you like to access, Checking Or Savings: ')
                        if withdrawAmt:
                            if cOrS == 'checking':
                                newChecking = float(lstBankingDeets[1]) - float(withdrawAmt)
                                newAmtCLst = bankingDeets.replace(lstBankingDeets[1], str(newChecking))
                                transactionData.write(firstName + ' ' + lastName + ' | withdrew ' + (withdrawAmt) + ' and now has only ' + str(newChecking) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                break
                            elif cOrS == 'savings':
                                newSavings = float(lstBankingDeets[2]) - float(withdrawAmt)
                                newAmtSLst = bankingDeets.replace(lstBankingDeets[2], str(newSavings))
                                transactionData.write(firstName + ' ' + lastName + ' | withdrew ' + (withdrawAmt) + ' and now has only ' + str(newSavings) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                newAmtCLst = 0
                                break
                        elif depositAmt:
                            if cOrS == 'checking':
                                newChecking = float(lstBankingDeets[1]) + float(depositAmt)
                                newAmtCLst = bankingDeets.replace(lstBankingDeets[1], str(newChecking))
                                transactionData.write(firstName + ' ' + lastName + ' | deposited ' + (depositAmt) + ' and now has ' + str(newChecking) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                break
                            elif cOrS == 'savings':
                                newSavings = float(lstBankingDeets[2]) + float(depositAmt)
                                newAmtSLst = bankingDeets.replace(lstBankingDeets[2], str(newSavings))
                                transactionData.write(firstName + ' ' + lastName + ' | deposited ' + (depositAmt) + ' and now has ' + str(newSavings) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                newAmtCLst = 0
                                break

                    elif lstBankingDeets[0] == 'checking' and lstBankingDeets[2] == lstCust[6]:
                        cOrS = 'checking'
                        if withdrawAmt:
                            if cOrS == 'checking':
                                newChecking = float(lstBankingDeets[1]) - float(withdrawAmt)
                                newAmtCLst = bankingDeets.replace(lstBankingDeets[1], str(newChecking))
                                transactionData.write(firstName + ' ' + lastName + ' | withdrew ' + withdrawAmt + ' and now has only ' + str(newChecking) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                break
                        if depositAmt:
                            if cOrS == 'checking':
                                newChecking = float(lstBankingDeets[1]) + float(depositAmt)
                                newAmtCLst = bankingDeets.replace(lstBankingDeets[1], str(newChecking))
                                transactionData.write(firstName + ' ' + lastName + ' | deposited ' + depositAmt + ' and now has ' + str(newChecking) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                break

                    elif lstBankingDeets[0] == 'savings' and lstBankingDeets[2] == lstCust[6]:
                        cOrS = 'savings'
                        if withdrawAmt:
                            if cOrS == 'savings':
                                newSavings = float(lstBankingDeets[1]) - float(withdrawAmt)
                                newAmtSLst = bankingDeets.replace(lstBankingDeets[1], str(newSavings))
                                transactionData.write(firstName + ' ' + lastName + ' | withdrew ' + withdrawAmt + ' and now has only ' + str(newSavings) + ' in their ' + cOrS + ' account ' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                newAmtCLst = 0
                                break
                        if depositAmt:
                            if cOrS == 'savings':
                                newSavings = float(lstBankingDeets[1]) + float(depositAmt)
                                newAmtSLst = bankingDeets.replace(lstBankingDeets[1], str(newSavings))
                                transactionData.write(firstName + ' ' + lastName + ' | deposited ' + depositAmt + ' and now has ' + str(newSavings) + ' in their ' + cOrS + ' account' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                                newAmtCLst = 0
                                break


        checkingAndSavingsData.close()
        bankingCustomerData.close()
        checkingAndSavingsData = open('checking&SavingsData.txt', 'w+')

        if newAmtCLst != 0:
            newContent = fullDataLst.replace(bankingDeets, newAmtCLst)
            checkingAndSavingsData.write(newContent + '\n')
        else:
            newContent = fullDataLst.replace(bankingDeets, newAmtSLst)
            checkingAndSavingsData.write(newContent)


    def howMuchMoney(self):
        userName = input('What is your full name: ')
        nameVar = userName.split()
        firstName = nameVar[0]
        lastName = nameVar[1]

        checkingAndSavingsData = open('checking&SavingsData.txt', 'r')
        bankingCustomerData = open('bankingData.txt', 'r')

        lstCustomersDetails = checkingAndSavingsData.readlines()
        lstBankingDetails = bankingCustomerData.readlines()
        
        
        for customer in lstBankingDetails:
            lstCust = customer.split(' | ')
            if firstName == lstCust[0] and lastName == lstCust[1]:
                for bankDeets in lstCustomersDetails:
                    lstOfDeets = bankDeets.split(' | ')
                    accNum = lstOfDeets[0]
                    if accNum == 'both':
                        if lstOfDeets[3] == lstCust[6] and lstOfDeets[4] == lstCust[7]:
                            return('You have $' + str(lstOfDeets[1]) + ' in your checking account and $' + str(lstOfDeets[2]) + ' in your savings account.')
                        
                    elif accNum == 'checking':
                        if lstOfDeets[2] == lstCust[6]:
                            return('You have $' + str(lstOfDeets[1]) + ' in your checking account.')
                        
                    elif accNum == 'savings':
                        if lstOfDeets[2] == lstCust[6]:
                            return('You have $' + str(lstOfDeets[1]) + ' in your savings account.')
                
        return(' This user does not exist!')
                
    def moveToCheckingOrSavings(self):
        timeNew = time.asctime()
        transactionData = open('transactionData.txt', 'a+')
        bankingData = open('bankingData.txt', 'r')
        checkingSavingsData = open('checking&SavingsData.txt', 'r')

        fullName = input('What is your full name: ')

        lstName = fullName.split()
        firstName = lstName[0]
        lastName = lstName[1]
        balanceCheck = checkingSavingsData.readlines()

        checkingSavingsData = open('checking&SavingsData.txt', 'r')
        fullData = checkingSavingsData.read()
        custData = bankingData.readlines()

        bankingData = open('bankingData.txt', 'r')
        dataCheck = bankingData.read()

        for customer in custData:
            bankInfo = customer.split(' | ')
            if bankInfo[0] == firstName and bankInfo[1] == lastName:
                if len(bankInfo) == 9:
                    checkingId = bankInfo[6]
                    savingsId = bankInfo[7]
                    break
                else:
                    return('You cannot proceed with this function if you only have a checking or savings account, you must have both.')
            if firstName not in dataCheck or lastName not in dataCheck:
                return("This user doesn't exist.")

        for singleBalances in balanceCheck:
            accData = singleBalances.split(' | ')
            try:
                checkID = accData[3]
                savingID = accData[4]
            except IndexError:
                pass
            if checkingId == checkID and savingsId == savingID:
                transferPath = input('Type in CtoS or StoC: ')
                checkingBalance = float(accData[1])
                savingsBalance = float(accData[2])
                if transferPath == 'CtoS':
                    checkingToSavingAmt = float(input('How much would you like to transfer from checking to savings: '))
                    newCheckingBalance = checkingBalance - checkingToSavingAmt
                    newSavingsBalance = savingsBalance + checkingToSavingAmt
                    checkingSavingsData = open('checking&SavingsData.txt', 'w+')
                    lineForSingleBalances = singleBalances
                    newContentOne = singleBalances.replace(str(accData[1]), str(newCheckingBalance))
                    newContentTwo = newContentOne.replace(str(accData[2]), str(newSavingsBalance))
                    newData = fullData.replace(lineForSingleBalances, newContentTwo)
                    checkingSavingsData.write(newData)
                    transactionData.write(firstName + ' ' + lastName + ' | transfered ' + str(checkingToSavingAmt) + ' to their savings account and now has ' + str(newCheckingBalance) + ' in their checking account and ' + str(newSavingsBalance) + ' in their savings account' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n')
                    break
                elif transferPath == 'StoC':
                    savingsToCheckingAmt = float(input('How much would you like to transfer from savings to checking: '))
                    newCheckingBalance = checkingBalance + savingsToCheckingAmt
                    newSavingsBalance = savingsBalance - savingsToCheckingAmt
                    checkingSavingsData = open('checking&SavingsData.txt', 'w+')
                    lineForSingleBalances = singleBalances
                    newContentOne = singleBalances.replace(str(checkingBalance), str(newCheckingBalance))
                    newContentTwo = newContentOne.replace(str(savingsBalance), str(newSavingsBalance))
                    newData = fullData.replace(lineForSingleBalances, newContentTwo)
                    checkingSavingsData.write(newData)
                    transactionData.write(firstName + ' ' + lastName + ' | transferred ' + str(savingsToCheckingAmt) + ' to their checking account and now has ' + str(newSavingsBalance) + ' in their savings account and ' + str(newCheckingBalance) + ' in their checking account' +  ' | ' + 'DATE OF TRANSACTION ' + timeNew + '\n') 
                    break
                else:
                    print('Please type in an actual option.')

        bankingData.close()
        checkingSavingsData.close()
        transactionData.close()
        
    def clientToClientTransaction(self):
        timeNew = time.asctime()
        bankingData = open('bankingData.txt', 'r')
        checkingSavingsData = open('checking&SavingsData.txt', 'r')
        transactionData = open('transactionData.txt', 'a+')
        accInfo = bankingData.readlines()
        lstOfCheckingSavings = checkingSavingsData.readlines()

        fullName = input('What is your full name: ')
        lstName = fullName.split()
        firstName = lstName[0]
        lastName = lstName[1]

            #When working on this remember that you need to connect the ids to eachother and then access the other file. 
            #Remember to also copy all of the old Data so you can replace it. (full Data)
            
        for customer in accInfo:
            custLst = customer.split(' | ')
            if custLst[0] == firstName and custLst[1] == lastName:
                recipientOrSender = input('Requesting Cash = 1 OR Sending Cash = 2: ')
                if recipientOrSender == '1':
                    senderName = input('Type in the full name of the person you are requesting money from: ')
                    lstNameSender = senderName.split()
                    firstNameSender = lstNameSender[0]
                    lastNameSender = lstNameSender[1]
                    reqestedAmt = int(input('How much money are you requesting from this person: '))
                    #This can get tricky so im going to save this part for later...
                if recipientOrSender == '2':
                    recipientName = input('Recipient Name: ')
                    lstNameRecipient = recipientName.split()
                    firstNameRecipient = lstNameRecipient[0]
                    lastNameRecipient = lstNameRecipient[1]
                    amtSent = int(input('How much would you like to send to '+ recipientName +': '))
                    for recipientCust in accInfo:
                        recipientCustLst = recipientCust.split(' | ')
                        if recipientCustLst[0] == firstNameRecipient and recipientCustLst[1] == lastNameRecipient:
                            if len(recipientCustLst) == 8:
                                recipientCheckingId = recipientCustLst[6]
                            else:
                                recipientCheckingId = recipientCustLst[6]
                                recipientSavingsId = recipientCustLst[7]
                        for bankingInfo in lstOfCheckingSavings:
                            if bankingInfo[0] == 'both':
                                reciCheckingId = bankingInfo[3]
                                reciSavingsId = bankingInfo[4]
                            elif bankingInfo[0] == 'checking':
                                reciCheckingId = bankingInfo[3]
                            elif bankingInfo[0] == 'savings':
                                reciSavingsId = bankingInfo[3]
                        #INCOMPLETE

    def clientTransactionStatement(self):
        
        custData = open('bankingData.txt', 'r')
        transactionData= open('transactionData.txt', 'r')

        name = input('What is your full name? ')
        lstName = name.split()
        firstName = lstName[0]
        lastName = lstName[1]

        transactionTimeStart = input('From which date would you like this transaction statement to start (Format should be month, day, year WITH COMMAS): ')
        transactionTimeEnd = input('From which date would you like this transaction statement to end (Format should be month, day, year WITH COMMAS): ')

        transactionLstStart = transactionTimeStart.split(', ')
        transactionLstEnd = transactionTimeEnd.split(', ')
        tStartMonth = int(transactionLstStart[0])
        tStartDay = int(transactionLstStart[1])
        tStartYear = int(transactionLstStart[2])
        tEndMonth = int(transactionLstEnd[0])
        tEndDay = int(transactionLstEnd[1])
        tEndYear = int(transactionLstEnd[2])

        transactionStartTime = datetime.datetime(tStartYear, tStartMonth, tStartDay)
        transactionEndTime = datetime.datetime(tEndYear, tEndMonth, tEndDay)
        

        lstOfCustData = custData.readlines()
        lstOfCustTransaction = transactionData.readlines()

        for custInfo in lstOfCustData:
            lstCustInfo = custInfo.split(' | ')
            if firstName == lstCustInfo[0] and lastName == lstCustInfo[1]:
            
                if len(lstCustInfo) == 9:
                    checkingId = input('What is your checking ID: ')
                    savingsId = input('What is your savings ID: ')
                    if checkingId == lstCustInfo[6] and savingsId == lstCustInfo[7]:
                        break
                    else:
                        return('You dont exist...')
                    
                elif lstCustInfo[7][0] == 'c':
                    checkingId = input('What is your checking ID: ')
                    if checkingId == lstCustInfo[6]:
                        break
                    else:
                        return('You dont exist...')
                    
                elif lstCustInfo[7][0] == 's':
                    savingsId = input('What is your savings ID: ')
                    if savingsId == lstCustInfo[6]:
                        break
                    else:
                        return('You dont exist...')
            
            else:
                return('Please type a valid customer in.')

        transactionDataForCust = []   
        for custTransaction in lstOfCustTransaction:
            newCustTransLst = custTransaction.split(' | ')
            nameForTransaction = newCustTransLst[0].split()
            tFirstName = nameForTransaction[0]
            tLastName  = nameForTransaction[1]
            if tFirstName == firstName and tLastName == lastName:
                dateInfo = newCustTransLst[-1]
                lstDateInfo = dateInfo.split()
                month = lstDateInfo[4]
                day = int(lstDateInfo[5])
                year = int(lstDateInfo[7])
                lstMonths = ['blank','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                dateMonth = lstMonths.index(month)
                newDate = datetime.datetime(year,dateMonth,day)
                if newDate > transactionStartTime and newDate < transactionEndTime:
                    transactionDataForCust.append(custTransaction)

        return transactionDataForCust
    
    def closeAccount(self):
        name = input('What is your full name: ')
        lstName = name.split()
        firstName = lstName[0]
        lastName = lstName[1]

        bankingData = open('checking&SavingsData.txt', 'r')
        accData = open('bankingData.txt', 'r')
        transactionData = open('transactionData.txt', 'r')

        lstBankingData = bankingData.readlines()

        lstAccData = accData.readlines()
        lstTransactionData = transactionData.readlines()

        statment = input('You are trying to close your account, in order to do so, we would like you to type out ... "I, ' + name + ', am content with closing my bank account with Amogh Banking."' )
        if statment == ("I " + name + ', am content with closing my bank account with Amogh Banking.'):
            for custAccData in lstAccData:
                lstCustAccData = custAccData.split(' | ')
                if lstCustAccData[0] == firstName and lstCustAccData[1] == lastName:
                    print(firstName)

        else:
            return('You did not type this statement in correctly, Please try again.')
        
cus = customer()
#print(cus.storeCustomerDetails())
acc = Accounts()
# print(acc.depositOrWithdraw())
# print(acc.showAllData())
# print(acc.howMuchMoney())
# print(acc.intRateCalc())
# print(acc.moveToCheckingOrSavings())
#print(acc.clientToClientTransaction())
# print(acc.clientTransactionStatement())
print(acc.closeAccount())


