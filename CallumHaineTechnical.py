from csv import reader
from csv import writer
import datetime

#Function to create new transaction
def system_transaction(TransactionValue, AccountType, AccountID):
    transaction = []
    transaction.extend((AccountID, AccountType, 'SYSTEM', datetime.datetime.now().isoformat(), TransactionValue))
    return(transaction)

while True:
    try:
        #Get customer number
        customer_number = input('Please enter customer number : ')
        transactions = []
        #Read ledger and get transactions, balances, and account IDs
        file_name = 'customer-'+ customer_number + '-ledger.csv'
        with open(file_name) as csvfile:
            ledger = reader(csvfile, delimiter=',')
            current_balance, savings_balance = 0.00, 0.00
            current_ID, savings_ID = 'NA', 'NA'
            for transaction in ledger:
                transactions.append(transaction)
                if transaction[1] == 'CURRENT':
                    current_balance += float(transaction[4])
                    if current_ID == 'NA':
                        current_ID = transaction[0]
                if transaction[1] == 'SAVINGS':
                    savings_balance += float(transaction[4])
                    if savings_ID == 'NA':
                        savings_ID = transaction[0]
            break
    except FileNotFoundError:
        print('Ledger not found for this customer.')
        continue

print('Current account balance: £'+ str(current_balance)+'\n'
+'Savings account balance: £'+ str(savings_balance))


#Check if current account overdrawn and add new transactions to CSV if so
if current_balance < 0.00:
        overdrawn = -current_balance
        print('Overdrawn by: £'+ str(overdrawn))
        #If not enough in savings to pay overdraft, transfer all savings
        if overdrawn > savings_balance:
            a = -savings_balance
            b = savings_balance
        #Else transfer enough to pay off overdraft
        else:
            a = current_balance
            b = overdrawn
        #Add transactions to array
        transferA = system_transaction(a, 'SAVINGS', savings_ID)
        transferB = system_transaction(b, 'CURRENT', current_ID)

        transactions.extend((transferA, transferB))
        #Write array to new CSV
        with open('customer-'+ customer_number+'-ledger-NEW.csv', 'w', newline='') as file:
            writer = writer(file)
            for transaction in transactions:
                writer.writerow(transaction)
        print('£'+ str(-a) + ' transferred from savings to current account.')
else:
    print('Current account is not overdrawn')
