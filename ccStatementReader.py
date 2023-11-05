import pandas as pd
import os.path
import os
from os import listdir
from os.path import isfile, join
import categorisingTransactions
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

iciciStatementPath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\ICICI'
hdfcStatementPath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\HDFC'
processedFilePath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\Processed'
masterCSVpath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\masterStatement.csv'

def readingICICIStatement(newStatement):
    statement = pd.read_csv(newStatement, sep=',', skiprows=2, nrows=1000, header=2)
    statement.drop(0,inplace=True)
    statement.drop(['Intl.Amount','Reward Point Header','Sr.No.'], axis=1, inplace=True)
    statement['BillingAmountSign'].fillna('DR', inplace=True)
    statement['Amount(in Rs)'] = pd.to_numeric(statement['Amount(in Rs)'], errors='ignore', downcast='float')
    statement['Date'] = pd.to_datetime(statement['Date'], errors='ignore', dayfirst=True)
    statement.rename(columns={'Amount(in Rs)':'Amount', 'BillingAmountSign':'Transaction Type'}, inplace = True)
    statement['Card'] = 'ICICI CC'
    return statement

def readingHDFCstatement(newStatement):
    statement = pd.read_csv(newStatement, sep='~',engine='python', skiprows=20, header=1, skipfooter=19, on_bad_lines='skip', keep_default_na=False, na_values="")
    print(statement,"\n\n")
    statement.drop(['Transaction type','Primary / Addon Customer Name'], axis=1, inplace=True)
    statement['Debit / Credit '].replace(r'^\s*$','DR', regex=True, inplace=True)
    statement['Debit / Credit '].replace(r'^Cr.*\s$','CR', regex=True, inplace=True)
    statement.rename(columns={'DATE':'Date', 'Description':'Transaction Details','AMT':'Amount','Debit / Credit ':'Transaction Type'}, inplace = True)
    statement['Amount'] = pd.to_numeric(statement['Amount'], errors='ignore', downcast='float')
    statement['Date'] = pd.to_datetime(statement['Date'], errors='ignore', dayfirst=True)
    statement['Card'] = 'HDFC CC'
    #print(statement)
    return statement

def appendingToMasterStatement(statement):
    temp = categorisingTransactions.readStatement(statement)
    return temp

def writeToMasterStatement(table):
    master_statement = pd.read_csv(masterCSVpath, sep=',', header=0)
    master_statement = pd.concat([master_statement, table], ignore_index = True)
    master_statement.to_csv(masterCSVpath, mode='w', header = True, index=False)

def moveProcessedFiles(path, filename):
    os.rename(join(path, filename), os.path.join(processedFilePath,filename))
    print('Processed and moved: ', filename)

def checkForNewICICIStatement(path):
    if any(isfile(join(path, i)) for i in listdir(path)):
        try:
            for filename in listdir(path):
                print('Reading: ', filename)
                appendingToMasterStatement(readingICICIStatement(join(path, filename)))
                moveProcessedFiles(path, filename)         
        except:
            print("All files processsed!")
    else:
        print('No new ICICI statement found!')

def checkForNewHDFCStatement(path):
    if any(isfile(join(path, i)) for i in listdir(path)):
        try:
            for filename in listdir(path):
                print('Reading ', filename)
                appendingToMasterStatement(readingHDFCstatement(join(path, filename)))
                moveProcessedFiles(path, filename)
        except:
            print("All files processsed!")
    else:
        print('No new HDFC statement found!')

#checkForNewICICIStatement(iciciStatementPath)
#checkForNewHDFCStatement(hdfcStatementPath)
#readingHDFCstatement(r'C:\Users\91635\Desktop\shikhar\Personal Finance\Statements\HDFC\BilledStatements_3259_02-09-23_20.02.csv')


"""     transactions = []
    debit_credit = []
    
    for i in statement['Amount (INR)']:
        i = ''.join(i.split())
        i = ''.join(i.split(','))
        debit_credit.append(i[-3:])
        transactions.append(i[:-3]) """
