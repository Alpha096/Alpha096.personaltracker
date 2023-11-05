import pandas as pd
import os.path
import os
from os import listdir
from os.path import isfile, join
import categorisingTransactions 
import warnings
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from nltk.tokenize import word_tokenize

warnings.simplefilter(action='ignore', category=FutureWarning)

ICICIbankStatementPath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\Bank\\ICICI'
file = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\Bank\\OpTransactionHistory04-09-2023.xls'
masterBankStatement = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\masterBankStatement.csv'
processedFilePath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\Statements\\Processed'

def readingBankStatement(file):
    bankStatement = pd.read_excel(file, header=0, usecols="D:I", skiprows=12)
    bankStatement['Deposit Amount (INR )'] = pd.to_numeric(bankStatement['Deposit Amount (INR )'], errors='ignore', downcast='float')
    bankStatement['Withdrawal Amount (INR )'] = pd.to_numeric(bankStatement['Withdrawal Amount (INR )'], errors='ignore', downcast='float')
    bankStatement['Amount'] = bankStatement['Deposit Amount (INR )'] + bankStatement['Withdrawal Amount (INR )']
    bankStatement.drop(['Cheque Number','Balance (INR )'],axis=1, inplace=True)
    bankStatement['Deposit Amount (INR )'].replace(0, 'DR', inplace=True)
    bankStatement['Withdrawal Amount (INR )'].replace(0, 'CR', inplace=True)
    bankStatement.rename(columns={'Transaction Date':'Date', 'Transaction Remarks':'Transaction Details'}, inplace = True)

    for i, row in bankStatement.iterrows():
        if row[2] == 'CR':
            bankStatement.at[i, 'Transaction Type'] = 'CR'
        elif row[3] == 'DR':
            bankStatement.at[i, 'Transaction Type'] = 'DR'

    bankStatement.drop(['Withdrawal Amount (INR )','Deposit Amount (INR )'],axis=1, inplace=True)
    bankStatement.dropna(axis=0, how='any', inplace=True)
    bankStatement['Account'] = 'ICICI'
    return bankStatement

def transactionMatching(statement):
    masterStatement = pd.read_csv(masterBankStatement, sep=',', header=0)
    transcDetails = masterStatement['Transaction Details'].to_list()
    for i, desc in statement.iterrows():
        best_match = process.extractOne(desc[1], transcDetails, scorer=fuzz.partial_ratio)
        for j, row in masterStatement.iterrows():
            score = fuzz.ratio(str(row[1]),str(best_match[0]))
            #print('Tran detail ', str(row[1]), ' new statement ', str(best_match[0]), " score ", score)
            if score == 100:
                statement.at[i, 'Category'] = masterStatement.at[j, 'Category']
    return statement

def writeToMasterBankStatement(table):
    master_statement = pd.read_csv(masterBankStatement, sep=',', header=0)
    master_statement = pd.concat([master_statement, table], ignore_index = True)
    master_statement.to_csv(masterBankStatement, mode='w', header = True, index=False)

def appendingToMasterBankStatement(statement):
    temp = transactionMatching(statement)
    return temp
    if os.path.exists(masterBankStatement):
        master_statement = pd.read_csv(masterBankStatement, sep=',', header=0)
        master_statement = pd.concat([master_statement,transactionMatching(cleaningBankStatement(statement))], ignore_index = True)
        master_statement.to_csv(masterBankStatement, mode='w', header = True, index=False)
    else:
        cleaningBankStatement(statement).to_csv(masterBankStatement, mode='w', header = True, index=False)

def cleaningBankStatement(statement):
    for i, desc in statement.iterrows():
        statement.at[i, 'Transaction Details'] = cleanTransactionDescriptions(desc[1])
    #print(statement)
    return statement

def cleanTransactionDescriptions(text):
    #text = text.lower()
    text = re.sub(r'[^\w\s]|https?://\S+|www\.\S+|https?:/\S+|[^\x00-\x7F]+', '', str(text).strip())
    text_list = word_tokenize(text)
    result = ' '.join(text_list)
    return result

def moveProcessedFiles(path, filename):
    os.rename(join(path, filename), os.path.join(processedFilePath,filename))
    print('Processed and moved: ', filename)

def checkForNewICICIBankStatement(path):
    if any(isfile(join(path, i)) for i in listdir(path)):
        try:
            for filename in listdir(path):
                print('Reading ', filename)
                appendingToMasterBankStatement(readingBankStatement(join(path, filename)))
                moveProcessedFiles(path, filename)
                #print('Processed and moved ', filename)
        except:
            print("All files processsed!")
    else:
        print('No new HDFC statement found!')

#checkForNewICICIBankStatement(ICICIbankStatementPath)

def readFederalBankStatement(file):
    bankStatement = pd.read_csv(file, header=0, usecols=[1,2,7,8], skiprows=10, skipfooter=1, engine='python')
    bankStatement['Deposit'] = pd.to_numeric(bankStatement['Deposit'], errors='ignore', downcast='float')
    bankStatement['Withdrawal'] = pd.to_numeric(bankStatement['Withdrawal'], errors='ignore', downcast='float')
    bankStatement['Amount'] = bankStatement['Withdrawal'] + bankStatement['Deposit']
    bankStatement['Deposit'].replace(np.nan, 'DR', inplace=True)
    bankStatement['Withdrawal'].replace(np.nan, 'CR', inplace=True)
    bankStatement.rename(columns={'Tran Date':'Date', 'Particulars':'Transaction Details'}, inplace = True)

    for i, row in bankStatement.iterrows():
        if row[2] == 'CR':
            bankStatement.at[i, 'Transaction Type'] = 'CR'
            bankStatement.at[i,'Amount'] = row[3]
        elif row[3] == 'DR':
            bankStatement.at[i, 'Transaction Type'] = 'DR'
            bankStatement.at[i, 'Amount'] = row[2]

    bankStatement.drop(['Withdrawal','Deposit'],axis=1, inplace=True)
    bankStatement['Account'] = 'Federal'
    return bankStatement
    #print(bankStatement)

#readFederalBankStatement(r'C:\Users\91635\Desktop\shikhar\Personal Finance\fed Aug.csv')