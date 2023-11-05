import pandas as pd
import re
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

masterCSVpath = 'C:\\Users\\91635\\Desktop\\shikhar\\Personal Finance\\masterStatement.csv'

def cleanTransactionDescriptions(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]|https?://\S+|www\.\S+|https?:/\S+|[^\x00-\x7F]+|\d+', '', str(text).strip())
    text_list = word_tokenize(text)
    result = ' '.join(text_list)
    return result

def transactionMatching(statement):
    masterStatement = pd.read_csv(masterCSVpath, sep=',', header=0)
    transcDetails = masterStatement['Transaction Details'].to_list()
    for i, desc in statement.iterrows():
        best_match = process.extractOne(desc[1], transcDetails, scorer=fuzz.partial_ratio)
        for j, row in masterStatement.iterrows():
            score = fuzz.ratio(str(row[1]),str(best_match[0]))
            #print('Tran detail ', str(row[1]), ' new statement ', str(best_match[0]), " score ", score)
            if score == 100:
                statement.at[i, 'Category'] = masterStatement.at[j, 'Category']
    return statement

def readStatement(statement):
    for i, desc in statement.iterrows():
        statement.at[i, 'Transaction Details'] = cleanTransactionDescriptions(desc[1])
    statement = transactionMatching(statement)
    return statement

