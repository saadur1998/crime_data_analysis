# -*- coding: utf-8 -*-
"""CRIME_DATA_ANALYSIS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kpaNOJHDNyBZj4nYjDW_QEpRzLbXsRtF
"""

#shifting from cpu to gpu
import torch
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
device

# Commented out IPython magic to ensure Python compatibility.
#installing some extra required libraries
# %pip install statsmodels
# %pip install pmdarima

#importing all required libraries
import csv
import requests
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
import pmdarima as pm

import warnings
warnings.filterwarnings("ignore")

#import dataset
CSV_URL = 'https://data.montgomerycountymd.gov/resource/39y2-cdbh.csv'

# Set parameters since you can only import 1000 rows at a go
offset = 0  # Starting offset
limit = 1000  # Number of records per request

# Initialize an empty list to store CSV data
csv_data = []

# Loop through the API data using offset and limit
while True:
    # Construct API URL with offset and limit parameters
    api_url = f"{CSV_URL}?$offset={offset}&$limit={limit}"

    # Fetch data from API
    with requests.Session() as s:
        download = s.get(api_url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        temp=list(cr)
        csv_data.extend(temp)

    # Check if the number of fetched records is less than the limit
    if len(temp) < limit:
        break

    # Increment offset for the next request
    offset += limit

# Convert CSV data to a DataFrame
raw_data = pd.DataFrame(csv_data)

df=raw_data
# Print the shape of the DataFrame
print(df.shape)
df.head(5)

#make the first row as column names and reset the index
columns = df.iloc[0,:]
df.set_axis(columns, axis=1, inplace=True)
df.drop(df.index[0],inplace=True)

#reset the index
df.reset_index(drop=True,inplace=True)

#drop rows that have column names and reset index
#since the api was restricted to 1000 rows, we had to extract data 177k/100 times, everytime we did that, the column names were also imported 177 times, we need to remove these 177 rows
a=0
c=0
for i in df['PRA']: #can use any column name
  if i =='PRA':
    df.drop(c,inplace=True)
    a=a+1
  c=c+1
print(a)#no of rows dropeed
df.reset_index(drop=True,inplace=True)

print(df.shape)
df.head(5)

i=0
for j in df.columns:
  print(f'{j} HAS {len(df.iloc[:,i].unique())} UNIQUE VALUES')
  i=i+1

df['Crime Name1'].unique()

for j in df['Crime Name1'].unique():
  print(j)
  count=0
  for i in df['Crime Name2'][df['Crime Name1']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

"""# **CRIME NAME RECATEGORIZATION FUNCTION**"""

#fucntion to reorganise the categories
#old,new = crime name 3, onl2,new2 = crime name 2, choose = 1 crime name 3, choose 2 = crime name 2, True = Worn on Crime name 3, false = no work on crime name 3
def recat(old,new,old2,new2,chose,a=True):
  if a:
    if chose==1:
      for i in range(len(old)):
        df['Crime Name3'][df['Crime Name3']==old[i]] = new[i]
    if chose==2:
      for i in range(len(old)):
        df['Crime Name3'][df['Crime Name2']==old[i]] = new[i]
  for i in range(len(old2)):
    df['Crime Name2'][df['Crime Name2']== old2[i]] = new2

"""## **CRIME AGAINST PERSON REORGANIZATION**"""

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Person'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

old= ['Statuory Rape','Forcible Rape','Forcible Fondling','Sexual Assault With An Object','Forcible Sodomy','Incest']
new= ['RAPE','RAPE','FONDLING','WITH WEAPON','FORCIBLE SODOMY','INCEST WITH MINOR']
old2=['Statuory Rape','Forcible Rape','Forcible Fondling','Sexual Assault With An Object','Forcible Sodomy','Incest']
new2='Sex Offence'

recat(old,new,old2,new2,2)

old= ['HUMAN TRAFFICKING - COMMERCIAL SEX ACTS','HUMAN TRAFFICKING - INVOLUNTARY SERITUDE']
new= ['COMMERCIAL SEX ACTS','INVOLUNTARY SERITUDE']
old2=['Human Trafficking, Commercial Sex Acts', 'Human Trafficking, Involuntary Servitude']
new2='Human Trafficking'

recat(old,new,old2,new2,1)

old= ['ASSAULT - SIMPLE', 'ASSAULT - 2ND DEGREE', 'ASSAULT - AGGRAVATED - FAMILY-OTHER WEAPON', 'ASSAULT - AGGRAVATED - NON-FAMILY-OTHER WEAPON', 'ASSAULT - AGGRAVATED - PUB OFF-OTHER WEAPON', 'ASSAULT - AGGRAVATED - POL OFF-OTHER WEAPON', 'ASSAULT - AGGRAVATED - POL OFF-KNIFE', 'ASSAULT - AGGRAVATED - NON-FAMILY-GUN', 'ASSAULT - AGGRAVATED - GUN', 'ASSAULT - AGGRAVATED - FAMILY-GUN', 'ASSAULT - AGGRAVATED - POL OFF-GUN', 'ASSAULT - AGGRAVATED - PUB OFF-GUN', 'ASSAULT - AGGRAVATED - POL OFF-STRONG-ARM', 'ASSAULT - AGGRAVATED - FAMILY-STRONG-ARM', 'ASSAULT - AGGRAVATED - NON-FAMILY-STRONG-ARM', 'ASSAULT - AGGRAVATED - PUB OFF-STRONG-ARM', 'ASSAULT - AGGRAVATED - OTHER']
new= ['SIMPLE', '2ND DEGREE', 'WEAPON', 'WEAPON', 'WEAPON', 'WEAPON', 'WEAPON', 'GUN', 'GUN', 'GUN', 'GUN', 'GUN', 'STRONG ARM', 'STRONG ARM', 'STRONG ARM', 'STRONG ARM', 'OTHER']
old2=['Simple Assault', 'Aggravated Assault']
new2='Assault'

recat(old,new,old2,new2,1)

old= ['ASSAULT - INTIMIDATION (INCLUDES STALKING)','WEAPON - THREAT TO BOMB','WEAPON - THREAT TO BURN']
new= ['INTIMIDATION BY STALKING)','THREAT TO BOMB','THREAT TO BURN']
old2=['Intimidation']
new2='Intimidation'

recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='Kidnapping/Abduction'].unique()
new= ['ADULT','MINOR','UNDESCRIBED','MINOR','MINOR','ABUDCT','ADULT FOR RANSOM','MINOR FOR RANSOM']
old2=['Kidnapping/Abduction']
new2='Kidnapping'

recat(old,new,old2,new2,1)

old= ['HUMAN TRAFFICKING - COMMERCIAL SEX ACTS','HUMAN TRAFFICKING - INVOLUNTARY SERITUDE']
new= ['COMMERCIAL SEX ACTS','INVOLUNTARY SERITUDE']
old2=['Human Trafficking, Commercial Sex Acts','Human Trafficking, Involuntary Servitude']
new2='Human Trafficking'

recat(old,new,old2,new2,1)

old= ['HOMICIDE - JUSTIFIABLE', 'HOMICIDE - BY POLICE - JUSTIFIABLE', 'HOMICIDE - BY NON-POLICE - JUSTIFIABLE', 'HOMICIDE - NEGLIGENT MANSLAUGHTER', 'HOMICIDE - WILLFUL KILL-GUN', 'HOMICIDE - WILLFUL KILL-FAMILY-GUN', 'HOMICIDE - WILLFUL KILL-NON-FAMILY-GUN', 'HOMICIDE (DESCRIBE OFFENSE)', 'HOMICIDE - WILLFUL KILL', 'HOMICIDE - WILLFUL KILL-NON-FAMILY', 'HOMICIDE - JOHN OR JANE DOE - NO WARRANT', 'ASSAULT - AGGRAVATED - POL OFF-STRONG-ARM', 'ASSAULT - AGGRAVATED - FAMILY-STRONG-ARM', 'ASSAULT - AGGRAVATED - NON-FAMILY-STRONG-ARM', 'ASSAULT - AGGRAVATED - PUB OFF-STRONG-ARM', 'ASSAULT - AGGRAVATED - OTHER']
new= ['JUSTIFIABLE', 'JUSTIFIABLE BY POLICE', 'JUSTIFIABLE BY NON-POLICE', 'NEGLIGENT MANSLAUGHTER', 'KILL WITH GUN', 'KILL WITH GUN', 'KILL WITH GUN', 'KILL', 'KILL', 'KILL', 'JOHN OR JANE DOE - NO WARRANT', 'STRONG ARM', 'STRONG ARM', 'STRONG ARM', 'STRONG ARM', 'OTHER']
old2=['Justifiable Homicide', 'Murder and Nonnegligent Manslaughter', 'Negligent Manslaughter']
new2='Homicide'

recat(old,new,old2,new2,1)

old= ['COMM SEX OFF - PROCURE PROSTITUTE - ADULT','COMM SEX OFF - PURCHASE PROSTITUTE - ADULT','COMM SEX OFF - PURCHASE PROSTITUTE - MINOR']
new= ['PROCURE ADULT PROSTITUTE', 'PURCHASE ADULT PROSTITUTE', 'PURCHASE MINOR PROSTITUTE']
old2=['Purchasing Prostitution']
new2='Purchasing Prostitution'

recat(old,new,old2,new2,1)

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Person'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

"""# **CRIME AGAINST PROPERTY REORGANIZATION**"""

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Property'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

old= ['AUTO THEFT - VEHICLE THEFT','STOLEN VEHICLE (DESCRIBE OFFENSE)','AUTO THEFT - THEFT AND SALE VEHICLE','AUTO THEFT - THEFT VEHICLE BY BAILEE','AUTO THEFT - THEFT AND USE VEHICLE OTHER CRIME','AUTO THEFT - THEFT AND STRIP VEHICLE','LARCENY - SHOPLIFTING','LARCENY - FROM AUTO','LARCENY - AUTO PARTS','AUTO THEFT - STRIP STOLEN VEHICLE','LARCENY - STRIP VEHICLE','LARCENY - FROM BLDG','LARCENY - FROM BANKING-TYPE INST','LARCENY - FROM MALLS','LARCENY-FROM MALLS (NOT SHOPLIFTING)','LARCENY - POSTAL','LARCENY (DESCRIBE OFFENSE)','LARCENY - FROM YARDS','LARCENY - THEFT OF US GOVERNMENT PROPERTY','LARCENY - FROM SHIPMENT','LARCENY - FROM INTERSTATE SHIPMENT','LARCENY - POCKET PICKING','LARCENY - PURSE SNATCHING - NO FORCE','LARCENY - FROM COIN MACHINE']
new= ['VEHICLE THEFT','VEHICLE THEFT','THEFT AND SALE VEHICLE','VEHICLE THEFT','THEFT AND USE VEHICLE','THEFT AND STRIP VEHICLE','SHOPLIFTING','FROM AUTO','AUTO PARTS','STRIP VEHICLE','STRIP VEHICLE','FROM BUILDING','FROM BANKING INSTITUTION','FROM MALLS','FROM MALLS','POSTAL','UNDESCRIBED','FROM YARDS','THEFT OF US GOVERNMENT PROPERTY','FROM SHIPMENT','FROM SHIPMENT','POCKET PICKING','PURSE SNATCHING','FROM COIN MACHINE']
old2=['Motor Vehicle Theft','Shoplifting','Theft From Motor Vehicle','Theft of Motor Vehicle Parts or Accessories','Theft from Building','All other Larceny','Pocket/picking','Purse-snatching','From Coin/Operated Machine or Device']
new2='Larceny'

recat(old,new,old2,new2,1)

old= ['DAMAGE PROPERTY - PRIVATE','DAMAGE PROPERTY - BUSINESS','DAMAGE PROPERTY - PUBLIC','DAMAGE PROPERTY (DESCRIBE OFFENSE)','DAMAGE PROPERTY - PRIVATE-WITH EXPLOSIVE','DAMAGE PROPERTY - BUSINESS-WITH EXPLOSIVE']
new= ['PRIVATE','BUSINESS','PUBLIC','UNDESCRIBED','PRIVATE','BUSINESS']
old2=['Destruction/Damage/Vandalism of Property']
new2='Damage of Property'

recat(old,new,old2,new2,1)

old= ['FRAUD - ILLEGAL USE CREDIT CARDS','COUNTERFEITING','FORGERY OF CHECKS','FORGERY - PASS FORGED','FORGERY OF OTHER','FORGERY (DESCRIBE OFFENSE)','COUNTERFEITING - POSS COUNTERFEITED','COUNTERFEITING (DESCRIBE OFFENSE)','COUNTERFEITING - PASS COUNTERFEITED','FORGERY - POSSESS FORGED','IDENTITY THEFT','FRAUD - IDENTITY THEFT','FRAUD - CONFIDENCE GAME','FRAUD - SWINDLE','FRAUD (DESCRIBE OFFENSE)','FRAUD AND ABUSE - COMPUTER','FRAUD - FAILURE TO PAY','FRAUD - FALSE STATEMENT','FRAUD - MAIL','FRAUD - IMPERSONATION','FRAUD BY WIRE','FRAUD - HACKING/COMPUTER INVASION','FRAUD - WELFARE']
new= ['ILLEGAL USE OF CREDIT CARDS','COUNTERFEITING','FORGERY OF CHECKS','PASSING FORGED','FORGERY','FORGERY','POSSESS COUNTERFEIT','COUNTERFEITING','PASSING COUNTERFEIT','POSSESS FORGED','IDENTITY THEFT','IDENTITY THEFT','CONFIDENCE GAME','SWINDLE','UNDESCRIBED','COMPUTER','FAILURE TO PAY','FALSE STATEMENT','MAIL','IMPERSONATION','WIRE','HACKING','WELFARE']
old2=['Credit Card/Automatic Teller Machine Fraud','Counterfeiting/Forgery','Identity Theft','Impersonation','Wire Fraud','Hacking/Computer Invasion','Welfare Fraud','False Pretenses/Swindle/Confidence Game']
new2='Fraud'

recat(old,new,old2,new2,1)

old= ['EMBEZZLE (DESCRIBE OFFENSE)','EMBEZZLE - BANKING-TYPE INST','EMBEZZLE - BUSINESS PROP','EMBEZZLE - INTERSTATE SHIPMENT','EMBEZZLE - POSTAL','EMBEZZLE - PUBLIC PROP']
new= ['UNDESCRIBED','BANKING INSTITUTION','BUSINESS PROP','INTERSTATE SHIPMENT','POSTAL','PUBLIC PROPERTY']
old2=['Embezzlement']
new2='Embezzlement'

recat(old,new,old2,new2,1)

old= ['BURGLARY - FORCED ENTRY-RESIDENTIAL','BURGLARY - FORCED ENTRY-NONRESIDENTIAL','BURGLARY - NO FORCED ENTRY-NONRESIDENTIAL','BURGLARY - NO FORCED ENTRY-RESIDENTIAL','BURGLARY (DESCRIBE OFFENSE)','BURGLARY - BANKING-TYPE INST','BURGLARY - SAFE-VAULT']
new= ['RESIDENTIAL','NONRESIDENTIAL','NONRESIDENTIAL','RESIDENTIAL','UNDESCRIBED','BANKING INSTITUTION','SAFE VAULT']
old2=['Burglary/Breaking and Entering']
new2='Burglary'

recat(old,new,old2,new2,1)

old= ['ROBBERY - STREET-STRONG-ARM','ROBBERY - STRONG ARM','ROBBERY - STREET-GUN','ROBBERY - BUSINESS-STRONG-ARM','ROBBERY - KNIFE','ROBBERY - DOMESTIC','ROBBERY - OTHER WEAPON','ROBBERY - GUN','ROBBERY - BUSINESS-GUN','ROBBERY - CARJACKING - ARMED','ROBBERY (DESCRIBE OFFENSE)','ROBBERY - CARJACKING - STRONG-ARM','ROBBERY - RESIDENTIAL-GUN','ROBBERY - STREET-OTHER WEAPON','ROBBERY - RESIDENTIAL-STRONG-ARM','ROBBERY - FORCIBLE PURSE SNATCHING','ROBBERY - RESIDENTIAL-OTHER WEAPON','ROBBERY - BUSINESS-OTHER WEAPON','ROBBERY - BANKING-TYPE INST']
new= ['STREET','STRONG ARM','STREET','BUSINESS','KNIFE','DOMESTIC','OTHER WEAPON','GUN','BUSINESS','CARJACKING','UNDESCRIBE','CARJACKING','RESIDENTIAL','STREET','RESIDENTIAL','PURSE SNATCHING','RESIDENTIAL','BUSINESS','BANKING INSTITUTION']
old2=['Robbery']
new2='Robbery'

recat(old,new,old2,new2,1)

old= ['ARSON - BUSINESS','ARSON (DESCRIBE OFFENSE)','ARSON - RESIDENTIAL-ENDANGERED LIFE','ARSON - BURNING OF - (IDENTIFY OBJECT)','ARSON - RESIDENTIAL','ARSON - BUSINESS-ENDANGERED LIFE','ARSON - PUB-BLDG','ARSON - PUB-BLDG-ENDANGERED LIFE']
new= ['BUSINESS','UNDESCRIBE','RESIDENTIAL','OBJECT','RESIDENTIAL','BUSINESS','PUBLIC BUILDING','PUBLIC BUILDING']
old2=['Arson']
new2='Arson'

recat(old,new,old2,new2,1)

old= ['EXTORTION (DESCRIBE OFFENSE)','EXTORT - THREAT INJURE REPUTATION','EXTORT - THREAT INJURE PERSON','EXTORT - THREAT ACCUSE PERSON OF CRIME','EXTORT - THREAT OF INFORMING OF VIOLENCE','EXTORT - THREAT DAMAGE PROP']
new= ['UNDESCRIBED','THREAT TO INJURE REPUTATION','THREAT TO INJURE PERSON','THREAT TO ACCUSE PERSON OF CRIME','THREAT TO VIOLENCE','THREAT TO DAMAGE PROPERTY']
old2=['Extortion/Blackmail']
new2='Extortion'

recat(old,new,old2,new2,1)

old= ['STOLEN PROPERTY (DESCRIBE OFFENSE)','STOLEN PROPERTY - POSSESS','RECEIVE STOLEN VEHICLE','AUTO THEFT - POSSESS STOLEN VEHICLE','STOLEN PROPERTY - CONCEAL','STOLEN PROPERTY - POSSESS STOLEN VEHICLE','STOLEN PROPERTY - SALE OF','STOLEN PROPERTY - RECEIVE']
new= ['UNDESCRIBED','POSSESS','RECEIVE VEHICLE','POSSESS VEHICLE','CONCEAL','POSSESS VEHICLE','SELL','RECEIVE']
old2=['Stolen Property Offenses']
new2='Stolen Property Offenses'

recat(old,new,old2,new2,1)

old= ['BRIBERY (DESCRIBE OFFENSE)']
new= ['BRIBERY']
old2=['Bribery']
new2='Bribery'

recat(old,new,old2,new2,1)

"""# **CRIME AGAINST SOCIETY REORGANIZATION**"""

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Property'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

drug_list = ["BARBITURATE","MARIJUANA","COCAINE","MARIJUANA","MARIJUANA","COCAINE","OPIUM OR DERIVATIVE","AMPHETAMINE","SYNTHETIC NARCOTIC","MARIJUANA","HEROIN","COCAINE","HEROIN","OPIUM OR DERIVATIVE","MARIJUANA","HEROIN","SYNTHETIC NARCOTIC","SYNTHETIC NARCOTIC","HALLUCINOGEN","DANGEROUS","HALLUCINOGEN","AMPHETAMINE","BARBITURATE","HALLUCINOGEN","HALLUCINOGEN","OPIUM OR DERIVATIVE","AMPHETAMINE","OPIUM OR DERIVATIVE","HALLUCINOGEN","HEROIN","SYNTHETIC NARCOTIC","BARBITURATE","COCAINE","BARBITURATE"]

old= df['Crime Name3'][df['Crime Name2']=='Drug/Narcotic Violations'].unique()
old = np.append(old, 'DRUGS - NARCOTIC EQUIP - POSSESS')
new= drug_list
new.append('NARCOTIC EQUIPMENT')
old2=['Drug/Narcotic Violations','Drug Equipment Violations']
new2='Drug/Narcotic Violations'

recat(old,new,old2,new2,1)

old= []
new= []
old2=['Trespass of Real Property']
new2='Trespassing'

recat(old,new,old2,new2,1,False)

old= df['Crime Name3'][df['Crime Name2']=='Weapon Law Violations'].unique()
new= ["POSSESSION", "POSSESSION", "UNDESCRIBED", "USAGE", "POSSESSION", "POSSESSION", "POSSESSION", "USAGE", "USAGE", "ALTERING IDENTIFICATION", "SELLING", "TRAFFICKING/TRANSPORTING", "TRAFFICKING/TRANSPORTING"]
old2=['Weapon Law Violations']
new2='Weapon Law Violations'

recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='Disorderly Conduct'].unique()
old= np.append(old, 'SEX OFFENSE - PEEPING TOM')
new = ["DISTURBING PUBLIC PEACE", "INDECENT EXPOSURE", "DISTURBING PUBLIC PEACE", "INDECENT EXPOSURE", "INDECENT EXPOSURE", "INDECENT EXPOSURE", "INDECENT EXPOSURE", "INDECENT EXPOSURE","PEEPING TOM"]
old2=['Disorderly Conduct', 'Peeping Tom']
new2='Disorderly Conduct'

recat(old,new,old2,new2,1)

old= np.concatenate((df['Crime Name3'][df['Crime Name2']=='Prostitution'].unique(),df['Crime Name3'][df['Crime Name2']=='Assisting or Promoting Prostitution'].unique()))
new= ['PROSTITUTION', 'PIMPING', 'PURCHASE PROSTITUTE', 'PROSTITUTION',  'PURCHASE PROSTITUTE', 'UNDESCRIBED',  'PIMPING', 'TRANSPORT FEMALE INTERSTATE FOR IMM', ' HOUSE OF ILL FAME']
old2=['Prostitution','Assisting or Promoting Prostitution']
new2='Prostitution'

recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='Family Offenses, NonViolent'].unique()
new= ['NEGLECT CHILD','CRUELTY TOWARD CHILD','NEGLECT FAMILY', 'UNDESCRIBED']
old2=['Family Offenses, NonViolent']
new2='Family Offenses'

recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='Pornography/Obscene Material'].unique()
new= ['OBSCENE MATERIAL','DISTRIBUTION','POSSESSION','MANUFACTURING','OBSCENE MATERIAL']
old2=['Pornography/Obscene Material']
new2='Pornography'


recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='Liquor Law Violations'].unique()
new= ['POSSESS','UNDESCRIBED','SELL','TRANSPORT']
old2=['Liquor Law Violations']
new2='Liquor Law Violations'

recat(old,new,old2,new2,1)

old= df['Crime Name3'][df['Crime Name2']=='All Other Offenses'].unique()
new= ['POLICE INFORMATION','MISSING PERSON','MENTAL ILLNESS','MENTAL ILLNESS','LOST PROPERTY','RECOVERED PROPERTY','RECOVERED PROPERTY','OVERDOSE','SUDDEN DEATH','HARASSING COMMUNICATION','SUICIDE','FUGITIVE','MENTAL TRANSPORT','ALL OTHER OFFENSES','UNAUTHORIZED USE OF VEHICLE','SUICIDE ATTEMPT','VIOLATION OF A COURT ORDER','MAKING FALSE REPORT','PEEPING TOM','POSSESS BURGLARY TOOLS','FUGITIVE','FIRE','OBSTRUCT POLICE','TERROR THREAT','RESISTING OFFICER','VIOLATION OF EMERGENCY ORDER','TRAFFIC OFFENSES','ESCAPE FROM CUSTODY','OBSTRUCT CRIMINAL INVEST','PUBLIC ORDER CRIMES','OBSTRUCTING COURT ORDER','OBSCENE COMMUNICATION','DRUNKENNESS','HIT AND RUN','LITTERING','JUVENILE','INSUFFICIENT FUNDS CHECK']
old2=['Liquor Law Violations']
new2='Liquor Law Violations'

recat(old,new,old2,new2,1)

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Society'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

"""# **Crime Against Not a Crime**"""

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Not a Crime'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

old= ['JUVENILE - RUNAWAY']
new= ['JUVENILE']
old2=['Crime Against Not a Crime']
new2='Crime Against Not a Crime'

recat(old,new,old2,new2,1)

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Not a Crime'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

"""# **Crime Against Person, Property, or Society**"""

for j in df['Crime Name2'][df['Crime Name1']=='Crime Against Person, Property, or Society'].unique():
  print(j)
  count=0
  for i in df['Crime Name3'][df['Crime Name1']=='Crime Against Person, Property, or Society'][df['Crime Name2']==j].unique():
    print(i)
    count=count+1
  print(count)
  print('\n')

#remove columns not required for EDA and Prediction and list them as well
#24
for i in [0,12,19,20,22,29,30,31,32,33,34,35,36,37]:
  print(df.columns[i])
df.drop(df.columns[[0,12,19,20,22,29,30,31,32,33,34,35,36,37]], axis=1, inplace=True)
df.reset_index(drop=True,inplace=True)
df.head(5)

#df.iloc[0:2,0:7]

#df.iloc[0:2,7:13]

#df.iloc[0:2,13:]

print("cloumns that need to be converted to int")
for i in [0,1,4,11,16]:
  print(df.columns[i])

print("\ncloumns that need to be converted to float")
for i in [21,22]:
  print(df.columns[i])

print("\ncloumns that need to be converted to timestamp")
for i in [2,19]:
  print(df.columns[i])

inte=0
for j in [0,1,4,11,16]:
  for i in range(df.shape[0]):
     if df.iloc[i,j] == '0':
      inte=inte+1
print(inte)

#Replacing missing or unknown values with '0' AND '0.00' for easy conversion of columns to integer/float from string
for j in [0,1,4,11,16]:
  for i in range(df.shape[0]):
     if df.iloc[i,j] == '':
      df.iloc[i,j] = '0'
     elif df.iloc[i,j] == 'Unknown':
      df.iloc[i,j] = '0'

for j in [21,22]:
  for i in range(df.shape[0]):
    if df.iloc[i,j] == '':
      df.iloc[i,j] = '0.00'
    elif df.iloc[i,j] == 'Unknown':
      df.iloc[i,j] = '0.00'

df.columns

#Converting required columns to integer type
for i in [0,1,4,11,16]:
    df[df.columns[i]] = df[df.columns[i]].astype(int)
    print(df[df.columns[i]].dtype)

#Converting required columns to float type
for i in [21,22]:
    df[df.columns[i]] = df[df.columns[i]].astype(float)
    print(df[df.columns[i]].dtype)

df.replace('', np.nan, inplace=True)
df.isnull().sum()

#replace empty stings with 'None'
#check None values
#for j in range(df.shape[1]):
#  for i in range(df.shape[0]):
#    if df.iloc[i,j] == '':
#      df.iloc[i,j] = None
#    elif df.iloc[i,j] == 'Unknown':
#      df.iloc[i,j] = None
#df.isnull().sum()

for i in range(len(df.columns)):
#while df.iloc[j,i]=='':
  print(f'{df.columns[i]} is of {type(df.iloc[1,i])}')

"""# **TIME DATA WRANGLING**"""

date_list = []
time_list = []
year_list = []
year_month = []
month_list = []
day_list=[]
for i in df['Start_Date_Time']:
  try:
    date_time = datetime.datetime.strptime(i, "%m/%d/%Y  %I:%M:%S %p")

    year = date_time.strftime("%Y")
    year_list.append(year)

    month = date_time.strftime("%m")
    month_list.append(month)

    day = date_time.strftime("%d")
    day_list.append(day)

    month_year = date_time.strftime("%m/%Y")
    year_month.append(month_year)

    date = date_time.strftime("%m/%d/%Y")
    date_list.append(date)

    hour = date_time.strftime("%I:%M:%S %p")
    time_list.append(hour)
  except:
    z=i
    e=e+1
    date_list.append('')
    time_list.append('')
    continue

df['Year'] = year_list
df['Year'] = df['Year'].astype(int)

df['Month'] = month_list
df['Month'] = df['Month'].astype(int)

df['Day'] = day_list
df['Day'] = df['Day'].astype(int)

df['Year_Month'] = year_month
df['Date'] = date_list
df['Time'] = time_list

"""# **FINALIZING DATASET**"""

#resctricting the dataset to cities inside Montgomery County Maryland
city = ['ASHTON', 'BARNESVILLE', 'BEALLSVILLE', 'BETHESDA', 'BOYDS',
       'BRINKLOW', 'BROOKEVILLE', 'BURTONSVILLE', 'CABIN JOHN',
       'CHEVY CHASE', 'CLARKSBURG', 'DAMASCUS', 'DERWOOD', 'DICKERSON',
       'GAITHERSBURG', 'GARRETT PARK', 'GERMANTOWN', 'GLEN ECHO',
       'KENSINGTON', 'MONTGOMERY VILLAGE', 'OLNEY', 'POOLESVILLE',
       'POTOMAC', 'ROCKVILLE', 'SANDY SPRING', 'SILVER SPRING',
       'SPENCERVILLE', 'TAKOMA PARK', 'WASHINGTON GROVE']

df = df.loc[df['City'].isin(city)]
df.reset_index(drop=True,inplace=True)

df_final = df[['Victims','Crime Name1','Crime Name2','Crime Name3','Police District Name','City','Year','Month','Day','Year_Month','Date','Time','Latitude','Longitude']]
df_final = df_final.sort_values(by=["Year",	"Month",	"Day","Time"])
df_final

column = ['Victims','Crime Category','Crime Name','Crime Detail','Police District','City','Year','Month','Day','Year_Month','Date','Time','Latitude','Longitude']
df_final.set_axis(column, axis=1, inplace=True)
df_final.replace('', np.nan, inplace=True)
df_final.dropna(inplace=True)
#df_final['Year_Month']=pd.to_datetime(df_final['Year_Month'], format="%m/%Y")
#df_final['Date']=pd.to_datetime(df_final['Date'], format="%m/%d/%Y")
#df_final['Time']=pd.to_datetime(df_final['Time'], format="%I:%M:%S %p")
#df_final.sort_values(by=['Date','Time'], ascending=False, inplace=True)
df_final.reset_index(drop=True,inplace=True)
df_final

i=0
for j in df_final.columns:
  print(f'{j} HAS {len(df_final.iloc[:,i].unique())} UNIQUE VALUES')
  i=i+1

"""# **EDA**"""

count=0
for i in range(100):
  if df_final.loc[df_final['Victims'].astype(int)>i].count()[0] == 0:
    break
  else:
    count=count+1
print(count)

# Extract the data from the loop
victims = []
incidents = []
for i in range(1,count+1):
  victims.append(i)
  incidents.append(df_final.loc[df_final['Victims'].astype(int) == i].count()[0])

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(victims, incidents, color='blue')

# Add labels and title
plt.xlabel("Number of Victims")
plt.ylabel("Number of Incidents")
plt.title("Number of Incidents by Number of Victims")

# Add grid and show the plot
plt.grid(True)

# Add numbers on top of each bar
for i, v in enumerate(victims):
  plt.text(v, incidents[i], str(incidents[i]), ha='center', va='bottom')

plt.show()

# Initialize variables
r = 0
so = 0
se = 0

# Loop through the 'Crime Detail' column of df_final
for i in df_final['Crime Detail']:
    if 'RAPE' in i:
        r += 1
    elif 'SODOMY' in i:
        so += 1
    elif 'SEX' in i:
        se += 1

# Print the counts
print(f"Rape: {r}")
print(f"Sodomy: {so}")
print(f"Sexual Offence: {se}")

# Create a pie chart
labels = ['Rape ('+str(r)+')', 'Sodomy('+str(so)+')', 'Sexual Offence('+str(se)+')']
sizes = [r, so, se]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

ax.axis('equal')  # Equal aspect ratio ensures a circular pie chart

# Show the pie chart
plt.show()

data = {'Year': list(df_final['Year'].value_counts().index),
        'Count': list(df_final['Year'].value_counts())}
dff = pd.DataFrame(data)
dff.sort_values(by='Year',inplace = True)

x = dff['Year']
y = dff['Count']
plt.figure(figsize=(15,6))
plt.plot(x,y)
plt.xticks(rotation=90)

import seaborn as sns

# Set the Seaborn style
sns.set_style("whitegrid")

# Define the data
x = df_final['Crime Name'].value_counts().head(15).index
y = df_final['Crime Name'].value_counts().head(15)

# Create the bar plot
plt.figure(figsize=(15,6))
sns.barplot(x=x, y=y)
plt.xticks(rotation=90)

# Add a title and labels
plt.title("Most Common Crimes")
plt.xlabel("Crime Name")
plt.ylabel("Number of Crimes")

# Show the plot
plt.show()

# Set the Seaborn style
sns.set_style("whitegrid")

# Define the data
x = df_final['Crime Detail'].value_counts().head(15).index
y = df_final['Crime Detail'].value_counts().head(15)

# Create the bar plot
plt.figure(figsize=(15,6))
sns.barplot(x=x, y=y, palette="hls")
plt.xticks(rotation=90)

# Add a title and labels
plt.title("Most Common Crimes")
plt.xlabel("Crime Name")
plt.ylabel("Number of Crimes")

# Show the plot
plt.show()

x = df_final['City'].value_counts().index
y = df_final['City'].value_counts()

# Create a DataFrame from the data
dff = pd.DataFrame({
    "City": x,
    "Count": y
})

# Sort the data by count
dff = dff.sort_values(by="Count", ascending=False)

# Create the horizontal bar plot
plt.figure(figsize=(40, 10))
sns.barplot(data=dff, x="Count", y="City", palette="hls")

# Add a title and labels
plt.title("Number of Crimes by City")
plt.xlabel("Count")
plt.ylabel("City")

# Show the plot
plt.show()

zz = df_final['Month'].value_counts()
data = {'Month': list(df_final['Month'].value_counts().index),
        'Count': list(df_final['Month'].value_counts())}
dff = pd.DataFrame(data)
dff.sort_values(by='Month',inplace = True)
plt.figure(figsize=(20,12))
plt.bar(dff['Month'],dff['Count'])

df_try['Year'].unique()

df_try=df_final
df_try.drop(df_try.loc[df_try['Year'] == 2016].index, inplace=True)
df_try.drop(df_try.loc[df_try['Year'] == 2017].index, inplace=True)
df_try.drop(df_try.loc[df_try['Year'] == 2018].index, inplace=True)

y=[]
x=[1,2,3,4,5,6,7,8,9,10,11,12]
for i in df_try['Year'].unique():
  zz = df_try.loc[df_try['Year'] == i]

  data = {'Year': list(zz['Year_Month'].value_counts().index),
        'Count': list(zz['Year_Month'].value_counts())}
  dff = pd.DataFrame(data)
  dff.sort_values(by='Year',inplace = True)

  y.append(dff['Count'])

plt.figure(figsize=(20,12))
plt.plot(x,y[0],label='2019')
plt.plot(x,y[1],label='2020')
plt.plot(x,y[2],label='2021')
plt.plot(x,y[3],label='2022')
plt.plot(x,y[4],label='2023')
plt.plot([1,2,3,4],y[5],label='2024')
plt.legend()
plt.xticks(rotation=90)

pivot_table = df_final.pivot_table(values='Victims', index='Police District', aggfunc='count').sort_values(by='Victims', ascending=False)

plt.figure(figsize=(20, 12))
sns.heatmap(pivot_table, cmap='PuBuGn')
plt.xlabel("Police District")
plt.ylabel("Count")

"""# **TEMPORAL ANAYSIS AND PREDICTION**"""

df_try=df_final
df_try.drop(df_try.loc[df_try['Year'] == 2016].index, inplace=True)
df_try.drop(df_try.loc[df_try['Year'] == 2017].index, inplace=True)
df_try.drop(df_try.loc[df_try['Year'] == 2018].index, inplace=True)

data_ml = {'Date': list(df_try['Date'].value_counts().index),
        'Count': list(df_try['Date'].value_counts())}
df_ml = pd.DataFrame(data_ml)
df_ml.dropna(inplace=True)
df_ml.sort_values(by='Date',inplace = True)
df_ml.reset_index(drop=True,inplace=True)
df_ml = pd.DataFrame(df_ml)

df_ml['Date'] = pd.to_datetime(df_ml['Date'])
df_ml = df_ml.sort_values(by='Date')
df_ml = df_ml.reset_index(drop=True)
df_ml.drop(df_ml.index[-1],inplace=True)
df_ml.set_axis(df_ml['Date'], axis=0, inplace=True)
df_ml.drop(columns=['Date'],inplace=True)

df_ml

df_ml_train=df_ml.iloc[:-15,:]
df_ml_test =df_ml.iloc[-15:-1,:]

#Determine rolling statistics
df_ml["rolling_avg"] = df_ml["Count"].rolling(window=7).mean() #window size 12 denotes 12 months, giving rolling mean at yearly level
df_ml["rolling_std"] = df_ml["Count"].rolling(window=7).std()
df_ml.dropna(inplace=True)

#Plot rolling statistics
plt.figure(figsize=(15,7))
plt.plot(df_ml["Count"], color='#379BDB', label='Original')
plt.plot(df_ml["rolling_avg"], color='#D22A0D', label='Rolling Mean')
plt.plot(df_ml["rolling_std"], color='#142039', label='Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block=False)

#Augmented Dickey–Fuller test:
print('Results of Dickey Fuller Test:')
dftest = adfuller(df_ml_train['Count'], autolag='AIC')

dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value

print(dfoutput)

#Standard ARIMA Model
ARIMA_model = pm.auto_arima(list(df_ml_train['Count']),
                        start_p=20,
                        start_q=20,
                        test='adf', # use adftest to find optimal 'd'
                        max_p=35, max_q=35, # maximum p and q
                        m=7, # frequency of series (if m==1, seasonal is set to FALSE automatically)
                        d=None,# let model determine 'd'
                        seasonal=True, # No Seasonality for standard ARIMA
                        trace=False, #logs
                        error_action='warn', #shows errors ('ignore' silences these)
                        suppress_warnings=True,
                        stepwise=True)

ARIMA_model.plot_diagnostics(figsize=(15,12))
plt.show()

def forecast(ARIMA_model, periods=14):
    # Forecast
    n_periods = periods
    fitted, confint = ARIMA_model.predict(n_periods=n_periods, return_conf_int=True)
    index_of_fc = pd.date_range(df_ml_train.index[-1] + pd.DateOffset(days=1), periods = n_periods, freq='D')

    # make series for plotting purpose
    fitted_series = pd.Series(fitted, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)


    # Plot
    plt.figure(figsize=(25,7))
    plt.plot(df_ml.iloc[-40:-1,0], color='red',label='Actual CrimeRate')
    plt.plot(fitted_series, color='blue', label = 'Predicted CrimeRate')
    plt.fill_between(lower_series.index,
                  lower_series,
                  upper_series,
                  color='k', alpha=.15)

    plt.title("ARIMA - Forecast of CrimeRate in Montegomery County, MD")
    plt.legend()
    plt.show()
    return fitted_series


z=forecast(ARIMA_model)

from sklearn.metrics import mean_squared_error, r2_score
print('Mean Squared Error =',mean_squared_error(df_ml.iloc[-15:-1,0],z))
print('Root Mean Square =',r2_score(df_ml.iloc[-15:-1,0],z))

def MAPE(Y_actual,Y_Predicted):
    mape = np.mean(np.abs((Y_actual - Y_Predicted)/Y_actual))*100
    return mape
MAPE(df_ml.iloc[-15:-1,0],z)

"""# **GEO-SPACIAL ANALYSIS**"""

!pip install contextily

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Prepare your location data
locations = gpd.GeoDataFrame({
    'Latitude': df_final['Latitude'][df_final['Latitude']!=0],
    'Longitude':df_final['Longitude'][df_final['Longitude']!=0],
    'geometry': gpd.points_from_xy(df_final['Longitude'][df_final['Longitude']!=0],df_final['Latitude'][df_final['Latitude']!=0]),
})

# Set the CRS for the locations GeoDataFrame to EPSG:4326
locations.crs = "EPSG:4326"

# Create a simple scatter plot for your locations
fig, ax = plt.subplots(figsize=(15, 15))
locations.plot(ax=ax, markersize=0.5, color='red', label='Crime Locations')

# Fetch and plot the basemap using OpenStreetMap data
ctx.add_basemap(ax, crs=locations.crs, source=ctx.providers.OpenStreetMap.Mapnik)

ax.set_title('Crime Locations on the Map of Montgomery County, Maryland')
plt.legend()
plt.show()