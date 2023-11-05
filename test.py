import pandas as pd
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

record = {
'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya' ],
'Age': [21, 19, 20, 18, 17, 21],
'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'],
'Percentage': [88, 92, 95, 70, 65, 78]}

# create a dataframe
masterStatement = pd.DataFrame(record, columns = ['Name', 'Age', 'Stream', 'Percentage'])

record11 = {
'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya' ]}
statement = pd.DataFrame(record11, columns = ['Name'])
#temp = dataframe[['Percentage','Name']].to_dict('split')
transcDetails = masterStatement['Name'].to_list()
#print(masterStatement)
print(statement)
#print(temp['data'].value)
for i, name in statement.iterrows():
    best_match = process.extractOne(name[0], transcDetails, scorer=fuzz.partial_ratio)
    for j, row in statement.iterrows():
        
        #print(str(best_match[0]))
        a = fuzz.token_set_ratio(str(row[0]),str(best_match[0]))
        
        if a == 100:
            print(str(row[0]))
            print(a)
            print(str(best_match[0]))
            #print('ata')
            statement.at[j, 'Category'] = masterStatement.at[i, 'Percentage']
print(statement)

# selecting rows based on condition
#rslt_df = dataframe.loc[dataframe['Percentage'] == 88]
#a=rslt_df['Name'].to_string()
#print(a)
#b = re.sub(r'^\d\s\s\s\s', '', a)
#print(b)
#print('\nResult dataframe :\n', rslt_df)